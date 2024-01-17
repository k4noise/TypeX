import unittest
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

  def test_get_active_char(self):
    active_char = self.words_viewmodel._words[self.words_viewmodel._active_row][self.words_viewmodel._active_char]
    expected_char = self.words_viewmodel._get_active_char()
    self.assertEqual(active_char, expected_char)

  def test_change_char_type(self):
    char_type = "wrong"
    self.words_viewmodel._change_char_type(char_type)
    self.assertEqual(self.words_viewmodel._get_active_char(), self.words_viewmodel._get_active_char())

  def test_shift_active_char_normal(self):
    self.words_viewmodel._active_char = 0
    self.words_viewmodel._shift_active_char(1)
    self.assertEqual(self.words_viewmodel._active_char, 1)

    self.words_viewmodel._shift_active_char(-1)
    self.assertEqual(self.words_viewmodel._active_char, 0)

  def test_shift_active_char_extreme(self):
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
    old_active_char_position = self.words_viewmodel._active_char
    right_char = self.words_viewmodel._get_active_char()["text"]
    self.words_viewmodel._change_active_char(right_char)
    old_active_char_type = self.words_viewmodel._words[self.
    words_viewmodel._active_row][old_active_char_position]["type"]

    self.assertEqual(self.words_viewmodel._get_active_char()["type"], "active")
    self.assertEqual(old_active_char_type, "printed")

  def test_change_active_char_to_wrong(self):
    old_active_char_position = self.words_viewmodel._active_char
    wrong_char = "`"
    self.words_viewmodel._change_active_char(wrong_char)
    old_active_char_type = self.words_viewmodel._words[self.    words_viewmodel._active_row][old_active_char_position]["type"]

    self.assertEqual(self.words_viewmodel._get_active_char()["type"], "active")
    self.assertEqual(old_active_char_type, "wrong")


if __name__ == '__main__':
  unittest.main()