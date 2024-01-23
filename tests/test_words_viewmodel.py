import unittest
from unittest.mock import patch
from model.words_model import WordsModel
from viewmodel.words_viewmodel import WordsViewModel

class TestWordsViewModel(unittest.TestCase):
  def setUp(self):
    self.data = [["a", "b"], ["c", "d"], ["e", "f"]]
    words_model = WordsModel(self.data)
    self.words_viewmodel = WordsViewModel(words_model)

  def test_convert(self):
    expected_data = [[{"type": "unprinted", "text": char} for char in row] for row in self.data]
    converted_data = self.words_viewmodel._convert(self.data)

    self.assertListEqual(expected_data, converted_data)

  def test_row_count(self):
    self.assertEqual(self.words_viewmodel.rowCount(), len(self.words_viewmodel._words))

  def test_get_data(self):
    row_index = 0
    index = self.words_viewmodel.index(row_index,0)
    self.assertEqual(self.words_viewmodel.data(index), self.words_viewmodel._words[row_index])

  def test_delete_row(self):
    old_rows_length = len(self.words_viewmodel._words)
    row_index_to_delete = 0
    deleted_row = self.words_viewmodel._words[row_index_to_delete]
    self.words_viewmodel.removeRow(row_index_to_delete)

    self.assertEqual(len(self.words_viewmodel._words), old_rows_length - 1)
    self.assertNotIn(deleted_row, self.words_viewmodel._words)

  def test_insert_row_normal(self):
    old_rows_length = len(self.words_viewmodel._words)
    row_to_insert = [["a", "b", "c"]]
    self.words_viewmodel.insertRows(row_to_insert)

    self.assertEqual(len(self.words_viewmodel._words), old_rows_length + 1)
    self.assertIn(self.words_viewmodel._convert(row_to_insert)[0], self.words_viewmodel._words)

  def test_insert_row_overflow(self):
    first_row = self.words_viewmodel._words[0]
    row_to_insert = [["h", "n"]]
    self.words_viewmodel.insertRows(row_to_insert)
    self.words_viewmodel.insertRows(row_to_insert)

    self.assertEqual(len(self.words_viewmodel._words), self.words_viewmodel._max_rows_count)
    self.assertNotIn(first_row, self.words_viewmodel._words)
    self.assertIn(self.words_viewmodel._convert(row_to_insert)[0], self.words_viewmodel._words)

  def test_change_language(self):
    old_words = self.words_viewmodel._words.copy()
    self.words_viewmodel.changeLanguage("en")
    self.assertNotEqual(old_words, self.words_viewmodel._words)

  def test_start_over(self):
    old_words = self.words_viewmodel._words.copy()
    self.words_viewmodel.changeLanguage("en")
    self.assertNotEqual(old_words, self.words_viewmodel._words)


  def test_get_active_char(self):
    active_char = self.words_viewmodel._words[self.words_viewmodel._active_row][self.words_viewmodel._active_char]
    expected_char = self.words_viewmodel._get_active_char()
    self.assertEqual(active_char, expected_char)

  def test_change_active_char_data(self):
    char_type = "unprinted"
    char = "d"
    self.words_viewmodel._change_active_char_data(char_type, char)
    self.assertEqual(self.words_viewmodel._get_active_char()["type"], char_type)
    self.assertEqual(self.words_viewmodel._get_active_char()["text"], char)


  def test_change_active_char_type(self):
    char_type = "wrong"
    self.words_viewmodel._change_active_char_data(char_type)
    self.assertEqual(self.words_viewmodel._get_active_char()["type"], char_type)

  def test_shift_active_char_normal(self):
    self.words_viewmodel._active_char = 0
    self.words_viewmodel._shift_active_char(1)
    self.assertEqual(self.words_viewmodel._active_char, 1)

    self.words_viewmodel._shift_active_char(-1)
    self.assertEqual(self.words_viewmodel._active_char, 0)

  def test_shift_active_char_overflow(self):
    last_row_char_index = len(self.words_viewmodel._words[0]) - 1
    self.words_viewmodel._active_char = last_row_char_index
    old_row = 0
    self.words_viewmodel._shift_active_char(1)
    self.assertEqual(self.words_viewmodel._active_char, 0)
    self.assertEqual(self.words_viewmodel._active_row, old_row + 1)

    self.words_viewmodel._shift_active_char(-1)
    self.assertEqual(self.words_viewmodel._active_char, last_row_char_index)
    self.assertEqual(self.words_viewmodel._active_row, old_row)

  def test_remove_active_char(self):
    self.words_viewmodel._active_char = 1
    old_active_char_position = self.words_viewmodel._active_char
    self.words_viewmodel._shift_active_char(-1)
    old_active_char_type = self.words_viewmodel._words[self.
    words_viewmodel._active_row][old_active_char_position]["type"]

    self.assertEqual(old_active_char_type, "unprinted")
    self.assertEqual(self.words_viewmodel._get_active_char()["type"], "active")

  def test_change_active_char_to_printed(self):
    old_printed_chars_count = self.words_viewmodel._right_chars_typed
    old_wrong_chars_count = self.words_viewmodel._wrong_chars_typed
    old_active_char_position = self.words_viewmodel._active_char
    right_char = self.words_viewmodel._get_active_char()["text"]
    self.words_viewmodel._change_active_char(right_char)
    old_active_char_type = self.words_viewmodel._words[self.
    words_viewmodel._active_row][old_active_char_position]["type"]

    self.assertEqual(self.words_viewmodel._get_active_char()["type"], "active")
    self.assertEqual(old_active_char_type, "printed")
    self.assertEqual(old_printed_chars_count + 1, self.words_viewmodel._right_chars_typed)
    self.assertEqual(old_wrong_chars_count, self.words_viewmodel._wrong_chars_typed)

  def test_change_active_char_to_wrong(self):
    old_printed_chars_count = self.words_viewmodel._right_chars_typed
    old_wrong_chars_count = self.words_viewmodel._wrong_chars_typed
    old_active_char_position = self.words_viewmodel._active_char
    wrong_char = "`"
    self.words_viewmodel._change_active_char(wrong_char)
    old_active_char_type = self.words_viewmodel._words[self.    words_viewmodel._active_row][old_active_char_position]["type"]

    self.assertEqual(self.words_viewmodel._get_active_char()["type"], "active")
    self.assertEqual(old_active_char_type, "wrong")
    self.assertEqual(old_printed_chars_count, self.words_viewmodel._right_chars_typed)
    self.assertEqual(old_wrong_chars_count + 1, self.words_viewmodel._wrong_chars_typed)

  def test_change_language(self):
    new_language = "en"
    self.words_viewmodel.changeLanguage(new_language)

    self.assertEqual(self.words_viewmodel._active_char, 0)
    self.assertEqual(self.words_viewmodel._active_row, 0)
    self.assertEqual(self.words_viewmodel._start_typing_time, 0)
    self.assertEqual(self.words_viewmodel._paused_time, 0)
    self.assertEqual(self.words_viewmodel._right_chars_typed, 0)
    self.assertEqual(self.words_viewmodel._wrong_chars_typed, 0)

  def test_typing_speed(self):
    MINUTE = 60
    typing_time = 2
    typed_chars = 5
    self.words_viewmodel._right_chars_typed = typed_chars
    with patch('time.time', return_value=typing_time):
      typing_speed = self.words_viewmodel.typingSpeed
      self.assertEqual(typing_speed, typed_chars / (typing_time / MINUTE))

  def test_mistake_percentage(self):
    wrong_chars = 2
    right_chars = 3
    self.words_viewmodel._wrong_chars_typed = wrong_chars
    self.words_viewmodel._right_chars_typed = right_chars
    percentage = self.words_viewmodel.mistakePercentage
    self.assertEqual(percentage, 100 * wrong_chars / (wrong_chars + right_chars))

  def test_is_paused(self):
    self.assertEqual(self.words_viewmodel.isPaused, self.words_viewmodel._is_paused)

  def test_toggle_pause(self):
    is_paused = self.words_viewmodel._is_paused
    self.words_viewmodel._toggle_pause()
    self.assertNotEqual(self.words_viewmodel._is_paused, is_paused)

  def test_reset(self):
    value = 10
    self.words_viewmodel._active_char = value
    self.words_viewmodel._active_row = value
    self.words_viewmodel._start_typing_time = value
    self.words_viewmodel._paused_time = value
    self.words_viewmodel._right_chars_typed = value
    self.words_viewmodel._wrong_chars_typed = value

    self.words_viewmodel._reset()

    self.assertEqual(self.words_viewmodel._active_char, 0)
    self.assertEqual(self.words_viewmodel._active_row, 0)
    self.assertEqual(self.words_viewmodel._start_typing_time, 0)
    self.assertEqual(self.words_viewmodel._paused_time, 0)
    self.assertEqual(self.words_viewmodel._right_chars_typed, 0)
    self.assertEqual(self.words_viewmodel._wrong_chars_typed, 0)


if __name__ == '__main__':
  unittest.main()