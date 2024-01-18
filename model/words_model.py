from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex, QVariant, QTimer
import sys
from queue import Queue
import markovify

class WordsModel(QAbstractListModel):
  default_rows_count = 4
  default_row_length = 38
  supported_languages = ["ru", "en"]
  _words_generators = {}

  def __init__(self, words=None, parent=None) -> None:
    super().__init__(parent)
    self._words = words if words is not None else []
    self._unused_words = Queue()

    for language in self.supported_languages:
      self._words_generators[language] = self._create_generator(language)

    self._current_words_generator = self._words_generators["ru"]

    if len(self._words) == 0:
      self._generate_rows(self.default_rows_count)

  def rowCount(self, parent=None) -> int:
    return len(self._words)

  def data(self, model_index: QModelIndex, role=Qt.DisplayRole):
    index = model_index.row()
    return self._words[index] if index else QVariant()

  def _create_generator(self, language):
    with open(f"assets/text/multitext_{language}.txt", encoding='utf-8') as text:
        readed_text = text.read()
    return markovify.Text(readed_text)

  def _generate_rows(self, rows_count):
    self._generate_sentences(rows_count * self.default_row_length)
    for _ in range(rows_count):
      self._words.append(self._generate_row())

  def _generate_row(self):
    words_length = 0
    words = []

    while not self._unused_words.empty():
      next_word = self._unused_words.queue[0]

      if words_length + len(next_word) + 1 > self.default_row_length:
          break

      word = self._unused_words.get()
      words_length += len(word) + 1
      words.append(word)

    return " ".join(words) + " "

  def _generate_sentences(self, min_length):
    sentences_length = 0;

    while sentences_length < min_length:
      sentence = self._current_words_generator.make_sentence();
      if sentence is None: continue
      sentences_length += len(sentence) + bool(sentences_length > 0)

      for word in sentence.split():
        self._unused_words.put(word)
