import QtQuick 2.15

Rectangle {
    property string backgroundCharColor: ""
    property string charColor: ""
    property string activeChar: ""

    color: charColor
    width: textSize * 0.6
    height: textSize

    Text {
        id: activeText
        text: activeChar
        color: backgroundCharColor
        font.pixelSize: textSize
        Timer {
            interval: 500
            running: true
            repeat: true
            onTriggered: {
                [backgroundCharColor, charColor] = [charColor, backgroundCharColor]
            }
        }
    }
}