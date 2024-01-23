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
    self.assertLess(self.words_model._unused_words.qsize(), self.words_model._default_row_length)

    for sentence in self.words_model._words:
      self.assertLessEqual(len(sentence), self.words_model._default_row_length)

  def test_create_generator(self):
    language = self.words_model._supported_languages[0]
    generator = self.words_model._create_generator(language)
    sentence = generator.make_sentence(tries=100)
    self.assertTrue(bool(sentence))

  def test_generate_sentences(self):
    self.words_model._unused_words.queue.clear()
    self.words_model._generate_sentences(self.words_model._default_row_length)
    sentence = self.words_model._unused_words.queue

    self.assertLessEqual(len(sentence), self.words_model._default_row_length)

  def test_generate_row(self):
    self.words_model._generate_sentences(self.words_model._default_row_length)
    sentence = self.words_model._generate_row()

    self.assertLessEqual(len(self.words_model._words), self.words_model._default_row_length)
    self.assertEqual(sentence[-1], " ")
    self.assertNotIn(sentence, self.words_model._words)

  def test_generate_rows_normal(self):
    rows_to_generate = 4
    self.words_model._words.clear()
    self.words_model.generate_rows(rows_to_generate)
    self.assertEqual(rows_to_generate, len(self.words_model._words))

  def test_generate_rows_overflow(self):
    rows_to_generate = 4
    old_rows = self.words_model._words.copy()
    self.words_model.generate_rows(rows_to_generate)
    self.assertEqual(len(old_rows), len(self.words_model._words))

  def test_change_language(self):
    current_language = self.words_model._active_language
    with self.assertRaises(ValueError):
      self.words_model.change_language("1")

    old_words_length = self.words_model._unused_words.qsize()
    self.assertGreaterEqual(old_words_length, 0)

    new_language = "en"
    self.words_model.change_language(new_language)
    self.assertNotEqual(current_language, self.words_model._active_language)
    self.assertEqual(new_language, self.words_model._active_language)
    self.assertNotEqual(old_words_length, self.words_model._unused_words.qsize())


  def test_generate_words(self):
    self.words_model._unused_words.queue.clear()
    self.words_model._generate_words()
    self.assertGreater(self.words_model._unused_words.qsize(), 0)

  def test_start_over(self):
    old_words = self.words_model._words.copy()
    self.words_model.start_over()
    self.assertNotEqual(old_words, self.words_model._words)


if __name__ == '__main__':
    unittest.main()