from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot

class WordsViewModel(QObject):
  dataChanged = pyqtSignal()

  def __init__(self, model):
    super().__init__()
    self._words_model = model

  @pyqtSlot(list)
  def updateData(self, value):
      self._words_model.data.append(value)
      print(self.data)
      self.dataChanged.emit()

  @pyqtProperty(list, notify=dataChanged)
  def data(self):
    return self._words_model._words
