import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt.labs.qmlmodels 1.0

import "../components"

FocusScope {
    property string printedCharColor: main.textColor
    property string unprintedCharColor: main.accentTextColor
    property string wrongCharColor: "#DB3A34"

    property int visibleRowsCount: 3
    property int textSize: Math.min(parent.width * 0.03, 36)
    property int maxTextHeight: textSize * 1.15

    id: trainer

    Column {
        x: parent.width * 0.8
        spacing: 10

        SpeedInfo {
            iconSrc: "speed"
            tooltip: "Скорость"
            info: wordsViewModel ? wordsViewModel.typingSpeed : 0
        }

        SpeedInfo {
            iconSrc: "errors"
            tooltip: "Ошибки"
            info: `${wordsViewModel ? wordsViewModel.mistakePercentage : 0}%`
            infoColor: wrongCharColor
        }
    }

    Rectangle {
        width: parent.width * 0.7
        height: parent.height * 0.6
        color: main.backgroundColor
        anchors.centerIn: parent

        ListView {
            id: textContainer
            width: parent.width
            height: visibleRowsCount * maxTextHeight
            model: wordsViewModel
            clip: true
            interactive: false
            focus: true

            delegate: TextRow {
                rowModel: display
            }

            function updateData(data) {
                wordsViewModel.updateData(data)
            }

            Keys.onPressed: {
                const textRegex = /^[ЁёА-я\w ,.!?;:_\-\+=№#'"`]*$/i

                if (event.key == Qt.Key_Backspace) {
                    updateData(Qt.Key_Backspace)
                } else if (event.key == Qt.Key_Escape) {
                    updateData(Qt.Key_Escape)
                } else if (event.text.length > 0 && textRegex.test(event.text)) {
                    updateData(event.text)
                }
            }

            displaced: Transition {
                NumberAnimation { properties: "y"; duration: 400; }
            }

            remove: Transition {
                NumberAnimation { properties: "y"; from: 0; to: -maxTextHeight; duration: 400 }
            }
        }
    }

    Rectangle {
        visible: wordsViewModel? wordsViewModel.isPaused : false
        width: parent.width
        height: parent.height
        color: main.backgroundColor
        z: 1

        Text {
            width: parent.width
            horizontalAlignment: Text.AlignHCenter
            y: 20
            text: qsTr("Пауза")
            color: printedCharColor
            font.pixelSize: textSize
        }

        PauseMenuButton {
            y: parent.height * 0.35
            label: "Возобновить"

            onClicked: {
                wordsViewModel.updateData(Qt.Key_Escape)
                textContainer.forceActiveFocus()
            }
        }

        PauseMenuButton {
            y: parent.height * 0.4
            label: "Начать заново"

            onClicked: {
                wordsViewModel.startOver()
                textContainer.forceActiveFocus()
            }
        }
    }
}