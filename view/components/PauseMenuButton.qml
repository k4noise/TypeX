import QtQuick 2.15
import QtQuick.Controls 2.15

Button {
    property string label: ""
    y: parent.height * 0.3
    focus: false
    font.pixelSize: textSize
    anchors.horizontalCenter: parent.horizontalCenter

    background: Rectangle {
        color: main.backgroundColor
    }

    contentItem: Text {
        text: `> ${label}`
        font.pixelSize: textSize * 0.8
        color: printedCharColor
    }
}