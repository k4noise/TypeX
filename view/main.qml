import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import QtGraphicalEffects 1.15

import "screens"
import "components"

Window {
    property var themes: ({
        "dark": {
            backgroundColor: "#323031",
            textColor: "#BFD7EA",
            accentTextColor: "#FFC857"
        },
        "light": {
            backgroundColor: "#BFD7EA",
            textColor: "#4062BB",
            accentTextColor: "#323031"
        }
    })
    property string selectedTheme: "dark"
    property string backgroundColor: themes[selectedTheme].backgroundColor
    property string textColor: themes[selectedTheme].textColor
    property string accentTextColor: themes[selectedTheme].accentTextColor

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

            Row {
                height: dockItemsWidth
                width: parent.width
                x: windowPadding + dockItemsWidth
                spacing: 20

                Image {
                    width: dockItemsWidth
                    source: "icons/daynight.png"
                    fillMode: Image.PreserveAspectFit
                    layer.enabled: true
                    layer.effect: ColorOverlay {
                        color: textColor
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            selectedTheme = selectedTheme === "dark" ? "light" : "dark"
                        }
                    }
                }

                ComboBox {
                    id: control
                    focus: false
                    model: ["ru", "en"]
                    width: 70


                    delegate: ItemDelegate {
                        width: parent.width
                        contentItem: Text {
                            text: modelData
                            color: backgroundColor
                            font.pixelSize:20
                        }
                    }

                    background: Rectangle {
                        color: backgroundColor
                    }

                    contentItem: Text {
                        text: control.displayText
                        color: textColor
                        verticalAlignment: Text.AlignVCenter
                        font.pixelSize:20
                    }

                    onActivated: {
                        if (navigation.activeScreen === "Trainer")
                            wordsViewModel.changeLanguage(currentText)
                    }

                    popup.onClosed: {
                        navigation.currentItem.forceActiveFocus()
                    }
                }
            }

            StackView {
                property string activeScreen: "Trainer"
                property bool isPaused: false
                
                id: navigation
                anchors.fill: parent

                initialItem: Component {
                    Trainer {}
                }

                onCurrentItemChanged: {
                    if (activeScreen === "Trainer" && isPaused) {
                        wordsViewModel.updateData(Qt.Key_Escape)
                        isPaused = false
                    } else if (!isPaused && activeScreen !== "Trainer") {
                        isPaused = true
                        wordsViewModel.updateData(Qt.Key_Escape)
                    }
                    currentItem.forceActiveFocus()
                }
            }
        }
    }
}