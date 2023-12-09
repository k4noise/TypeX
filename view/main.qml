import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15

Window {
    property string backgroundColor: "#323031"
    property int windowPadding: 20
    property int dockItemsWidth: 30
    property int dockItemsSpacing: 20

    visible: true
    title: "TypeX"
    width: 1200
    height: 700
    color: backgroundColor

    Item {
        x: windowPadding
        y: windowPadding
        width: parent.width - windowPadding * 2
        height: parent.height - windowPadding * 2

        ListView {
            objectName: "dock"
            width: dockItemsWidth
            height: 2 * dockItemsWidth
            spacing: dockItemsSpacing

            model: ListModel {
                ListElement { iconSrc: "icons/keyboard.png"; screen: "trainer" }
                ListElement { iconSrc: "icons/stats.png"; screen: "stats" }
            }

            delegate: Image {
                property string imageId: model.screen
                objectName: imageId
                width: dockItemsWidth
                source: model.iconSrc
                fillMode: Image.PreserveAspectFit

                MouseArea {
                    anchors.fill: parent
                    onClicked:  loader.source = `${model.screen}.qml`
                }
            }
        }

        Item {
            x: dockItemsWidth + windowPadding
            width: parent.width - dockItemsWidth - windowPadding
            height: parent.height
            Loader {
                id: loader
                objectName: "loader"
                source: "trainer.qml"
            }
        }
    }
}