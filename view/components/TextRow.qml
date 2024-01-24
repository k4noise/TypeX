import QtQuick 2.15
import Qt.labs.qmlmodels 1.0

Row {
    property var rowModel: []

    anchors.horizontalCenter: parent ? parent.horizontalCenter : undefined

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
                }
            }

            DelegateChoice {
                roleValue: "printed"

                Text {
                    text: modelData.text
                    font.pixelSize: main.textSize
                    color: printedCharColor
                }
            }

            DelegateChoice {
                roleValue: "unprinted"

                Text {
                    text: modelData.text
                    font.pixelSize: main.textSize
                    color: unprintedCharColor
                }
            }

            DelegateChoice {
                roleValue: "wrong"

                Text {
                    text: modelData.text
                    font.pixelSize: main.textSize
                    color: wrongCharColor
                }
            }
        }
    }
}