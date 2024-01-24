from PyQt5.QtCore import QObject
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class StatsModel(QObject):
  def __init__(self, languages, parent=None):
    super().__init__(parent)
    self.languages = languages
    self.db = QSqlDatabase.addDatabase('QSQLITE')
    self.db.setDatabaseName(':memory:')
    self.db.open()
    for language in languages:
      query = QSqlQuery()
      query.exec_(f'''
          CREATE TABLE IF NOT EXISTS {language} (
              speed INTEGER NOT NULL,
              errors INTEGER NOT NULL
          )
      ''')

  def set_typing_data(self, lang, speed, errors_percentage):
    query = QSqlQuery()
    query.exec_(f"INSERT INTO {lang} VALUES {speed}, {errors_percentage})")

  def get_typing_data(self, lang):
    query = QSqlQuery()
    query.exec_(f"SELECT * FROM {lang}")

    speed = []
    errors = []

    while query.next():
      speed.append(query.value(0))
      errors.append(query.value(1))

    return {"speed": speed, "errors": errors}