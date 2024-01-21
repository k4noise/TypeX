from PyQt5.QtCore import Qt, QAbstractListModel, pyqtSlot, QModelIndex, QVariant

class WordsViewModel(QAbstractListModel):
  default_active_row = 1
  _active_row = 0
  _active_char = 0

  def __init__(self, model):
    super().__init__()
    self._model = model
    self._words = self._convert(model._words)
    self._max_rows_count = model.default_rows_count
    self._get_active_char()["type"] = "active"


  def rowCount(self, parent=QModelIndex()):
     return len(self._words)

  def data(self, index, role=Qt.DisplayRole):
    row = index.row()
    value = self._words[row]
    return value if value else QVariant()

  def insertRow(self, value, parent=QModelIndex(), row=None,):
    if row is None:
       row = self._max_rows_count - 1

    is_full = len(self._words) == self._max_rows_count
    if is_full: self.removeRow()

    self.beginInsertRows(parent, row, row)
    self._words.extend(self._convert(value))
    self.endInsertRows()

    # dataChanged тут не отправляется, потому что вставленная строка не должна отображаться сразу же
    return True

  def removeRow(self, row=0, parent=QModelIndex()):
    self.beginRemoveRows(parent, row, row)
    del(self._words[0])
    self.endRemoveRows()

    index = self.index(row, 0)
    self.dataChanged.emit(index, index)
    return True

  @pyqtSlot(str)
  def updateData(self, value):
    if value == "-1":
      self._remove_active_char()
    else:
      self._change_active_char(value)

  def _convert(self, rows):
    return [[{"type": "unprinted", "text": char} for char in row] for row in rows]

  def _get_active_char(self):
    return self._words[self._active_row][self._active_char]

  def _change_char_type(self, char_type):
    index = self.index(self._active_row, 0)
    self._get_active_char()["type"] = char_type
    self.dataChanged.emit(index, index)

  def _change_active_char(self, value):
    old_char_text = self._get_active_char()["text"]
    old_char_type = "printed" if old_char_text == value else "wrong"
    self._change_char_type(old_char_type)

    self._shift_active_char(1)
    self._change_char_type("active")

  def _remove_active_char(self):
    self._change_char_type("unprinted")
    self._shift_active_char(-1)
    self._change_char_type("active")

  def _shift_active_char(self, direction):
    current_row_length = len(self._words[self._active_row])

    if direction < 0 and self._active_char == 0:
        if self._active_row > 0:
            self._active_row -= 1
            self._active_char = len(self._words[self._active_row]) - 1
    elif direction > 0 and self._active_char == current_row_length - 1:
        if self._active_row == self.default_active_row:
            self.insertRow(self._model._generate_rows(1))
        else:
            self._active_row = min(self._max_rows_count - 1, self._active_row + 1)
        self._active_char = 0
    else:
        self._active_char += direction
