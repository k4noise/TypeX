import QtQuick 2.15
import QtQuick.Controls 2.15

Button {
    property string label: ""

    focus: false
    y: parent.height * 0.3
    anchors.horizontalCenter: parent.horizontalCenter
    font.pixelSize: textSize

    background: Rectangle {
        color: main.backgroundColor
    }

    contentItem: Text {
        text: `> ${label}`
        font.pixelSize: textSize * 0.8
        color: printedCharColor
    }
}