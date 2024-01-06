from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication, QFont, QFontDatabase
from PyQt5.QtQml import QQmlApplicationEngine

if __name__ == "__main__":
    import sys

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(QUrl("view/main.qml"))

    font_id = QFontDatabase.addApplicationFont("view/font/PTMono-Regular.ttf")
    loaded_font_families = QFontDatabase.applicationFontFamilies(font_id)
    if loaded_font_families:
        defaultFont = QFont(loaded_font_families[0], 12)
        app.setFont(defaultFont)

    engine = QQmlApplicationEngine()
    engine.load(QUrl("view/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())