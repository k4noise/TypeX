from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty

class StatsViewModel(QObject):
  stats_changed = pyqtSignal()

  def __init__(self, model, parent=None):
    super().__init__(parent)
    self._model = model
    self.languages = model.languages
    self._stats = []

    for language in self._model.languages:
      self._stats.append(self._calculate_stats(language, self._model.get_typing_data(language)))

  @pyqtProperty(list, notify=stats_changed)
  def get_stats(self):
    return self._stats

  @pyqtSlot(str, int, int)
  def addTypingData(self, language, speed, errors_percentage):
    self._model.set_typing_data(language, speed, errors_percentage)
    current_state = self._find_state(language)

    current_state["sum_speed"] += speed
    current_state["count_speed"] += 1
    if speed > current_state["max_speed"]:
      current_state["max_speed"] = speed
    if current_state["sum_speed"] > 0:
      current_state["avg_speed"] = current_state["sum_speed"] / current_state["count_speed"]

    current_state["sum_errors"] += errors_percentage
    current_state["count_errors"] += 1
    if current_state["sum_errors"] > 0:
      current_state["avg_errors"] = current_state["sum_errors"] / current_state["count_errors"]

    self.stats_changed.emit()

  def _calculate_stats(self, language, data):
    stats = {
      "language": language,
      "max_speed": 0,
      "sum_speed": 0,
      "count_speed": 0,
      "avg_speed": 0,
      "sum_errors": 0,
      "count_errors": 0,
      "avg_errors": 0
    }

    for speed in data["speed"]:
      stats["sum_speed"] += speed
      if speed > stats["max_speed"]:
        stats["max_speed"] = speed

    stats["count_speed"] = len(data["speed"])
    stats["count_errors"] = len(data["errors"])
    stats["sum_errors"] = sum(data["errors"])

    if stats["sum_speed"] > 0:
      stats["avg_speed"] = stats["sum_speed"] / stats["count_speed"]

    if stats["sum_errors"] > 0:
      stats["avg_errors"] = stats["sum_errors"] / stats["count_errors"]

    return stats

  def _find_state(self, language):
    for state in self._stats:
      if state["language"] == language:
        return state

    return None