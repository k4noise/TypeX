import unittest
from model.words_model import WordsModel
from viewmodel.words_viewmodel import WordsViewModel

class TestWordsViewModel(unittest.TestCase):
  def setUp(self):
    self.data = ["A", "B", "C"]
    words_model = WordsModel(self.data)
    self.words_viewmodel = WordsViewModel(words_model)

  def test_convert(self):
    expected_data = [[{"type": "unprinted", "text": char} for char in row] for row in self.data]
    coverted_data = self.words_viewmodel._convert(self.data)

    self.assertListEqual(expected_data, coverted_data)


if __name__ == '__main__':
  unittest.main()