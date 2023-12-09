import QtQuick 2.15

Rectangle {
    property string textColor: "#BFD7EA"

    id: stats
    width: parent.width
    height: parent.height

    Text {
        text: "Stats screen"
        font.pointSize: 20
        color: textColor
    }
}