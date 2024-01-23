from enum import Enum
import time
from PyQt5.QtCore import Qt, QAbstractListModel, pyqtSlot, QModelIndex, QVariant, pyqtSignal, pyqtProperty

MINUTE = 60

class CharType(Enum):
   RIGHT = "right"
   WRONG = "wrong"
   ACTIVE = "active"
   UNPRINTED = "unprinted"
   PRINTED = "printed"

class WordsViewModel(QAbstractListModel):
  _pause_toggled = pyqtSignal()
  _char_typed = pyqtSignal()

  _default_active_row = 1
  _active_row = 0
  _active_char = 0

  _is_paused = False
  _paused_time = 0

  _start_typing_time = 0
  _right_chars_typed = 0
  _wrong_chars_typed = 0

  def __init__(self, model):
    super().__init__()
    self._model = model
    self._max_rows_count = model.default_rows_count
    self._words = self._convert(model._words)
    self._change_active_char_data(CharType.ACTIVE.value)


  def rowCount(self, parent=QModelIndex()):
     return len(self._words)

  def data(self, index, role=Qt.DisplayRole):
    row = index.row()
    value = self._words[row]
    return value if value else QVariant()

  def insertRows(self, rows, parent=QModelIndex(), row=None):
    if row is None:
       row = self._max_rows_count - 1

    is_full = len(self._words) == self._max_rows_count
    if is_full: self.removeRow()

    self.beginInsertRows(parent, row, row)
    self._words.extend(self._convert(rows))
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
    if value == str(Qt.Key_Escape):
      self._toggle_pause()

    elif not self._is_paused:
      if self._start_typing_time == 0:
        self._start_typing_time = time.time()
      if value == str(Qt.Key_Backspace):
        self._remove_active_char()
      else: self._change_active_char(value)
      self._char_typed.emit()

  @pyqtSlot(str)
  def changeLanguage(self, lang):
    self._reset()
    self._model.change_language(lang)
    self._words.extend(self._convert(self._model._words))
    self._change_active_char_data(CharType.ACTIVE.value)
    self.layoutChanged.emit()

  @pyqtSlot()
  def startOver(self):
     self._toggle_pause()
     self._reset()
     self._model.start_over()
     self._words = self._convert(self._model._words)
     self._change_active_char_data(CharType.ACTIVE.value)
     self.layoutChanged.emit()

  @pyqtProperty(int, notify=_char_typed)
  def typingSpeed(self):
    time_elapsed = time.time() - self._start_typing_time - self._paused_time
    time_elapsed /= MINUTE
    return int(self._right_chars_typed // time_elapsed)

  @pyqtProperty(int, notify=_char_typed)
  def mistakePercentage(self):
    percentage = 0
    if self._wrong_chars_typed > 0:
      percentage = self._wrong_chars_typed / (self._wrong_chars_typed + self._right_chars_typed)
    return int(percentage * 100)

  @pyqtProperty(bool, notify=_pause_toggled)
  def isPaused(self):
     return self._is_paused


  def _convert(self, rows):
    return [[{"type": CharType.UNPRINTED.value, "text": char} for char in row] for row in rows]

  def _get_active_char(self):
    return self._words[self._active_row][self._active_char]

  def _change_active_char(self, value):
    old_char_text = self._get_active_char()["text"]
    if old_char_text == value:
       self._right_chars_typed += 1
       old_char_type = CharType.PRINTED.value
    else:
       self._wrong_chars_typed += 1
       old_char_type = CharType.WRONG.value
    self._change_active_char_data(old_char_type, value)

    self._shift_active_char(1)
    self._change_active_char_data(CharType.ACTIVE.value)

  def _change_active_char_data(self, char_type, value=None):
    index = self.index(self._active_row, 0)
    self._get_active_char()["type"] = char_type
    if value:
       self._get_active_char()["text"] = value
    self.dataChanged.emit(index, index)

  def _remove_active_char(self):
    self._change_active_char_data(CharType.UNPRINTED.value)
    self._shift_active_char(-1)
    right_char = self._model._words[self._active_row][self._active_char]
    self._change_active_char_data(CharType.ACTIVE.value, right_char)

  def _shift_active_char(self, direction):
    current_row_length = len(self._words[self._active_row])

    if direction < 0 and self._active_char == 0:
        if self._active_row > 0:
            self._active_row -= 1
            self._active_char = len(self._words[self._active_row]) - 1
    elif direction > 0 and self._active_char == current_row_length - 1:
        if self._active_row == self._default_active_row:
            self.insertRows(self._model.generate_rows(1))
        else:
            self._active_row = min(self._max_rows_count - 1, self._active_row + 1)
        self._active_char = 0
    else:
        self._active_char += direction

  def _toggle_pause(self):
    if not self._is_paused:
      self._last_paused_time = time.time()
    else:
       self._paused_time += time.time() - self._last_paused_time

    self._is_paused = not self._is_paused
    self._pause_toggled.emit()

  def _reset(self):
    self._words.clear()
    self._active_char = 0
    self._active_row = 0
    self._start_typing_time = 0
    self._paused_time = 0
    self._right_chars_typed = 0
    self._wrong_chars_typed = 0
    self._char_typed.emit()