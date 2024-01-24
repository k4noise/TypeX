import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Row {
    property string iconSrc: ""
    property string tooltip: ""
    property string info: ""
    property string infoColor: trainer.unprintedCharColor
    anchors.centerIn: Qt.AlignVTop

    Image {
        width: dockItemsWidth
        source: `../icons/${iconSrc}.png`
        fillMode: Image.PreserveAspectFit
        layer.enabled: true
        layer.effect: ColorOverlay {
            color: infoColor
        }

        ToolTip {
            x: 0
            visible: infoArea.containsMouse
            delay: 500
            contentItem: Text {
                color: infoColor
                text: qsTr(tooltip)
            }
            background: Rectangle {
                color: backgroundColor
                border.color: infoColor
                radius: 5
            }
        }

        MouseArea {
            id: infoArea
            hoverEnabled: true
            anchors.fill: parent
        }
    }

    Text {
        leftPadding: 10
        color: infoColor
        font.pixelSize: main.textSize
        text: info
    }
}