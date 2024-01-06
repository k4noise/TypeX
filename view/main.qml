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
                ListElement { icon: "keyboard"; screen: "Trainer"; tooltip: "Тренажер" }
                ListElement { icon: "stats"; screen: "Stats"; tooltip: "Статистика" }
            }

            delegate: Image {
                width: dockItemsWidth
                source: `icons/${model.icon}.png`
                fillMode: Image.PreserveAspectFit
                layer.enabled: true
                layer.effect: ColorOverlay {
                    color: textColor
                }

                ToolTip {
                    x: windowPadding + dockItemsWidth
                    y: 0
                    visible: dockItemArea.containsMouse
                    delay: 500
                    contentItem: Text {
                        color: textColor
                        text: qsTr(model.tooltip)
                    }
                    background: Rectangle {
                        color: backgroundColor
                        border.color: textColor
                        radius: 5
                    }
                }

                MouseArea {
                    id: dockItemArea
                    hoverEnabled: true
                    anchors.fill: parent
                    onClicked: {
                        if (model.screen === navigation.activeScreen)
                            return;

                        const component = Qt.createComponent(`screens/${model.screen}.qml`);
                        if (component.status === Component.Ready) {
                            const newScreen = component.createObject(navigation);
                            navigation.pop();
                            navigation.push(newScreen);
                            navigation.activeScreen = model.screen
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
                property string activeScreen: "Trainer"
                id: navigation
                anchors.fill: parent
                initialItem: Component {
                    Trainer {}
                }
            }
        }
    }
}