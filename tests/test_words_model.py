import unittest
from model.words_model import WordsModel

class TestWordsModel(unittest.TestCase):
  def setUp(self):
    self.words_model = WordsModel()

  def test_creating_with_data(self):
    data = ["A", "B", "C"]
    model = WordsModel(data)
    self.assertListEqual(model._words, data)

  def test_generated_data(self):
    self.assertEqual(len(self.words_model._words), self.words_model.default_rows_count)
    self.assertLess(self.words_model._unused_words.qsize(), self.words_model.default_row_length)

    for sentence in self.words_model._words:
      self.assertLessEqual(len(sentence), self.words_model.default_row_length)

  def test_row_count(self):
    self.assertEqual(self.words_model.rowCount(), len(self.words_model._words))

  def test_generate_sentences(self):
    self.words_model._unused_words.queue.clear()
    self.words_model._generate_sentences(self.words_model.default_row_length)
    sentence = self.words_model._unused_words.queue

    self.assertLessEqual(len(sentence), self.words_model.default_row_length)

  def test_generate_row(self):
    self.words_model._generate_sentences(self.words_model.default_row_length)
    sentence = self.words_model._generate_row()

    self.assertLessEqual(self.words_model.rowCount(), self.words_model.default_row_length)
    self.assertEqual(sentence[-1], " ")
    self.assertNotIn(sentence, self.words_model._words)

  def test_generate_rows(self):
    rows_to_generate = 4
    old_rows = self.words_model._words.copy()
    self.words_model._generate_rows(rows_to_generate)

    self.assertNotEqual(len(old_rows), len(self.words_model._words))
    self.assertEqual(len(old_rows) + rows_to_generate, len(self.words_model._words))


if __name__ == '__main__':
    unittest.main()