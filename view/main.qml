import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtGraphicalEffects 1.15

import "screens"

Window {
    property string backgroundColor: "#323031"
    property string textColor: "#BFD7EA"

    property int windowPadding: 20
    property int dockItemsWidth: 30
    property int dockItemsSpacing: 20

    id: main
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
            width: dockItemsWidth
            height: 2 * dockItemsWidth
            spacing: dockItemsSpacing

            model: ListModel {
                ListElement { icon: "keyboard"; screen: "Trainer" }
                ListElement { icon: "stats"; screen: "Stats" }
            }

            delegate: Image {
                width: dockItemsWidth
                source: `icons/${icon}.png`
                fillMode: Image.PreserveAspectFit
                layer.enabled: true
                layer.effect: ColorOverlay {
                    color: textColor
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        const component = Qt.createComponent(`screens/${model.screen}.qml`);
                        if (component.status === Component.Ready) {
                            const newScreen = component.createObject(navigation);
                            navigation.pop();
                            navigation.push(newScreen);
                        }
                    }
                }
            }
        }

        Rectangle {
            x: dockItemsWidth + windowPadding
            width: parent.width - dockItemsWidth - windowPadding
            height: parent.height
            color: backgroundColor

            StackView {
                id: navigation
                anchors.fill: parent
                initialItem: Component {
                    Trainer {}
                }
            }
        }
    }
}