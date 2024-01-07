import QtQuick 2.15
import Qt.labs.qmlmodels 1.0

Row {
    property var rowModel: []
    anchors.horizontalCenter: parent.horizontalCenter

    Repeater {
        model: rowModel
        delegate: textTypeChooser

        DelegateChooser {
            id: textTypeChooser
            role: "type"

            DelegateChoice {
                roleValue: "active"
                ActiveChar {
                    activeChar: modelData.text
                    backgroundCharColor: backgroundColor
                    charColor: unprintedCharColor
                }
            }

            DelegateChoice {
                roleValue: "printed"
                Text {
                    text: modelData.text
                    font.pixelSize: trainer.textSize
                    color: printedCharColor
                }
            }

            DelegateChoice {
                roleValue: "unprinted"
                Text {
                    text: modelData.text
                    font.pixelSize: trainer.textSize
                    color: unprintedCharColor
                }
            }

            DelegateChoice {
                roleValue: "wrong"
                Text {
                    text: modelData.text
                    font.pixelSize: trainer.textSize
                    color: wrongCharColor
                }
            }
        }
    }
}