import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt.labs.qmlmodels 1.0

import "../components"

Item {
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
            property int nextRowYPosition: 0

            id: textContainer
            width: parent.width
            height: visibleRowsCount * maxTextHeight
            model: wordsViewModel.data
            clip: true
            interactive: false
            delegate: TextRow {
                rowModel: modelData
            }

            SmoothedAnimation on contentY {
                id: slideRow
                running: false
                from: textContainer.contentY
                to: textContainer.nextRowYPosition
                duration: 1500
            }

            function slideToNextRow() {
                console.log(textContainer.nextRowYPosition)
                textContainer.nextRowYPosition += maxTextHeight
                slideRow.running = true;
            }
        }
    }
}