from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication, QFont, QColor
from PyQt6.QtQml import QQmlApplicationEngine

if __name__ == "__main__":
    import sys

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(QUrl("view/main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())