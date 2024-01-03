import QtQuick 2.15

Rectangle {
    property string backgroundActiveChar: '';
    property string activeCharColor: ''
    color: backgroundActiveChar
    width: 20
    height: textSize

    Text {
        id: activeText
        text: activeChar
        color: activeCharColor
        font.pixelSize: textSize
        Timer {
            id: blinkTimer
            interval: 500
            running: true
            repeat: true
            onTriggered: {
                [backgroundActiveChar, activeCharColor] = [ activeCharColor, backgroundActiveChar]
            }
        }
    }
}