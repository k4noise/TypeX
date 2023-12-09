import QtQuick 2.15

Rectangle {
    property string accentColor: "#4062BB"
    property string textColor: "#BFD7EA"
    property string rightCharColor: "#FFC857"
    property string wrongCharColor: "#DB3A34"

    id: trainer
    width: parent.width
    height: parent.height
    color: "lightblue"

    Text {
        text: "Trainer screen"
        font.pointSize: 20
        color: textColor
    }
}