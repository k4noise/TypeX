from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication, QFont, QFontDatabase
from PyQt5.QtQml import QQmlApplicationEngine

from model.words_model import WordsModel
from viewmodel.words_viewmodel import WordsViewModel

if __name__ == "__main__":
    import sys

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    data = [
        [{"text": "printed text", "type": "printed"}],
        [
            {"text": "This i", "type": "printed"},
            {"text": "i", "type": "wrong"},
            {"text": "s", "type": "active"},
            {"text": " a sample unprinted text about", "type": "unprinted"},
        ],
        [{"text": "unprinted text unprinted text unprinted", "type": "unprinted"}],
        [{"text": "unprinted text unprinted text ", "type": "unprinted"}],
    ]
    words_model_instance = WordsModel(data)
    words_viewmodel_instance = WordsViewModel(words_model_instance)
    engine.rootContext().setContextProperty("wordsViewModel", words_viewmodel_instance)

    font_id = QFontDatabase.addApplicationFont("view/font/PTMono-Regular.ttf")
    loaded_font_families = QFontDatabase.applicationFontFamilies(font_id)
    if loaded_font_families:
        defaultFont = QFont(loaded_font_families[0], 12)
        app.setFont(defaultFont)

    engine.load(QUrl("view/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())