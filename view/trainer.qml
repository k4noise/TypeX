import QtQuick 2.15

Item {
    property string backgroundColor: "#323031"
    property string printedCharColor: "#BFD7EA"
    property string unprintedCharColor: "#FFC857"
    property string wrongCharColor: "#DB3A34"
    property string printedText: 'This i'
    property string activeChar: 's'
    property string unprintedText: ' a sample unprinted text about'
    property int textSize: parent.width * 0.03

    id: trainer

    Rectangle {
        width: Window.width * 0.7
        height: Window.height * 0.7
        anchors.centerIn: parent
        color: backgroundColor

        Column {

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
                text: 'unprinted text unprinted text '
                font.pixelSize: textSize
                color: unprintedCharColor
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
    }
}