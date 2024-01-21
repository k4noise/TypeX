import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt.labs.qmlmodels 1.0

import "../components"

FocusScope {
    property string printedCharColor: main.textColor
    property string unprintedCharColor: "#FFC857"
    property string wrongCharColor: "#DB3A34"

    property int visibleRowsCount: 3
    property int textSize: Math.min(parent.width * 0.03, 36)
    property int maxTextHeight: textSize * 1.15

    id: trainer

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
                if (event.key == Qt.Key_Backspace) {
                    updateData(-1)
                } else if (event.text.length > 0) {
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
}