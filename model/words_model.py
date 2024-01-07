from PyQt5.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt

class WordsModel(QAbstractListModel):
  def __init__(self, words=None, parent=None) -> None:
    super().__init__(parent)
    self._words = words if words is not None else []


  def rowCount(self, parent=None) -> int:
    return len(self._words)

  def data(self, model_index: QModelIndex, role=Qt.DisplayRole):
    index = model_index.row()
    return self._words[index] if index else QVariant()
