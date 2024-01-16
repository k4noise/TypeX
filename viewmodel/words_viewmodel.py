from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot

class WordsViewModel(QObject):
  dataChanged = pyqtSignal()
  active_row = 0
  active_char = 0

  def __init__(self, model):
    super().__init__()
    self._words = self._convert(model._words)
    self._max_rows_count = model.default_rows_count
    self._get_active_char()["type"] = "active"

  @pyqtSlot(str)
  def updateData(self, value):
      if value == "-1":
        self._remove_active_char()
      else:
        self._change_active_char(value)

      self.dataChanged.emit()

  @pyqtProperty(list, notify=dataChanged)
  def data(self):
    return self._words

  def _convert(self, rows):
    return [[{"type": "unprinted", "text": char} for char in row] for row in rows]

  def _get_active_char(self):
    return self._words[self.active_row][self.active_char]

  def _change_char_type(self, type):
    self._get_active_char()["type"] = type

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
    current_row_length = len(self._words[self.active_row])

    if direction < 0 and self.active_char == 0:
        self.active_row = max(0, self.active_row - 1)
        self.active_char = len(self._words[self.active_row])
    elif direction > 0 and self.active_char == current_row_length - 1:
        self.active_row = min(self._max_rows_count, self.active_row + 1)
        self.active_char = 0
    else:
        self.active_char += direction
