from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot

class WordsViewModel(QObject):
  dataChanged = pyqtSignal()
  active_row = 0
  active_char = 0

  def __init__(self, model):
    super().__init__()
    self._words = self._convert(model._words)
    self._words[self.active_row][self.active_char]["type"] = "active"

  @pyqtSlot(list)
  def updateData(self, value):
      self._words.append(value)
      print(self.data)
      self.dataChanged.emit()

  @pyqtProperty(list, notify=dataChanged)
  def data(self):
    return self._words

  def _convert(self, rows):
    return [[{"type": "unprinted", "text": char} for char in row] for row in rows]
