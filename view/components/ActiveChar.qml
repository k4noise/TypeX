import QtQuick 2.15

Rectangle {
    property string backgroundCharColor: "";
    property string charColor: ""
    color: backgroundCharColor
    width: textSize * 0.6
    height: textSize

    Text {
        id: activeText
        text: activeChar
        color: charColor
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