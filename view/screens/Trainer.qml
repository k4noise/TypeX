import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt.labs.qmlmodels 1.0

import "../components"

Item {
    property string printedCharColor: main.textColor
    property string unprintedCharColor: "#FFC857"
    property string wrongCharColor: "#DB3A34"

    property string printedText: 'This i'
    property string wrongChar: 'i'
    property string activeChar: 's'
    property string unprintedText: ' a sample unprinted text about'
    property int textSize: Math.min(parent.width * 0.03, 36)

    id: trainer

    Rectangle {
        width: parent.width * 0.7
        height: parent.height * 0.6
        color: main.backgroundColor
        anchors.centerIn: parent

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

                Repeater {
                    model: [
                        {text: printedText, type: 'printed'},
                        {text: wrongChar, type: 'wrong'},
                        {text: activeChar, type: 'active'},
                        {text: unprintedText, type: 'unprinted'},
                    ]

                    delegate: textTypeChooser

                    DelegateChooser {
                        id: textTypeChooser
                        role: "type"

                        DelegateChoice {
                            roleValue: 'active'
                            ActiveRowText {
                                backgroundActiveChar: backgroundColor
                                activeCharColor: unprintedCharColor
                            }
                        }

                        DelegateChoice {
                            roleValue: 'printed'
                            Text {
                                text: modelData.text
                                font.pixelSize: trainer.textSize
                                color: printedCharColor
                            }
                        }

                        DelegateChoice {
                            roleValue: 'unprinted'
                            Text {
                                text: modelData.text
                                font.pixelSize: trainer.textSize
                                color: unprintedCharColor
                            }
                        }

                        DelegateChoice {
                            roleValue: 'wrong'
                            Text {
                                text: modelData.text
                                font.pixelSize: trainer.textSize
                                color: wrongCharColor
                            }
                        }
                    }
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
            height: textSize * 1.1
            y: unvisibleText.y
            color: main.backgroundColor
        }
    }
}