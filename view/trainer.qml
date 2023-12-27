import QtQuick 2.15

Item {
    property string backgroundColor: "#323031"
    property string printedCharColor: "#BFD7EA"
    property string unprintedCharColor: "#FFC857"
    property string wrongCharColor: "#DB3A34"
    property string printedText: 'This i'
    property string wrongChar: 'i'
    property string activeChar: 's'
    property string unprintedText: ' a sample unprinted text about'
    property int textSize: Math.min(parent.width * 0.03, 36)

    id: trainer

    anchors.fill: parent

    Rectangle {
        width: parent.width * 0.7
        height: parent.height * 0.6
        anchors.centerIn: parent
        color: backgroundColor

        Column {
            width: parent.width

            Text {
                text: 'printed text'
                font.pixelSize: textSize
                color: printedCharColor
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Row {
                anchors.horizontalCenter: parent.horizontalCenter
                Text {
                    text: printedText
                    color: printedCharColor
                    font.pixelSize: textSize

                }

                Text {
                    text: activeChar
                    color: wrongCharColor
                    font.pixelSize: textSize
                }

                Text {
                    text: activeChar
                    color: unprintedCharColor
                    font.pixelSize: textSize
                }

                Text {
                    text: unprintedText
                    color: unprintedCharColor
                    font.pixelSize: textSize
                }
            }

            Text {
                text: 'unprinted text unprinted text unprinted'
                font.pixelSize: textSize
                color: unprintedCharColor
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                id: unvisibleText
                text: 'unprinted text unprinted text '
                font.pixelSize: textSize
                color: unprintedCharColor
                anchors.horizontalCenter: parent.horizontalCenter
            }

        }
        Rectangle {
            width: parent.width
            height: textSize * 1.2
            y: unvisibleText.y
            color: backgroundColor
        }
    }
}