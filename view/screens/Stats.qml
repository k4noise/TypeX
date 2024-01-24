import QtQuick 2.15
import QtQuick.Controls 2.15


Rectangle {
    id: stats
    width: parent.width
    height: parent.height
    color: main.backgroundColor

    Text {
        topPadding: main.windowPadding
        id: statsHeader
        width: parent.width
        horizontalAlignment: Text.AlignHCenter
        text: qsTr("Статистика")
        font.pixelSize: main.textSize * 0.9
        color: textColor
    }

    ListView {
        anchors.horizontalCenter: parent.horizontalCenter
        y: statsHeader.y + statsHeader.height + 50
        height: parent.height
        width: parent.width * 0.7
        model: statsViewModel.get_stats
        spacing: 30

        delegate: Column {
            Text {
                text: qsTr(`Статистика по ${modelData.language} языку`)
                font.pixelSize: main.textSize * 0.9
                color: textColor
            }

            Text {
                text: qsTr(`Максимальная скорость: ${modelData["max_speed"]}`)
                font.pixelSize: main.textSize * 0.8
                color: textColor
            }

             Text {
                text: qsTr(`Средняя скорость: ${modelData["avg_speed"]}`)
                font.pixelSize: main.textSize * 0.8
                color: textColor
            }

            Text {
                text: qsTr(`Среднее колличество ошибок: ${modelData["avg_errors"]}`)
                font.pixelSize: main.textSize * 0.8
                color: textColor
            }
        }
    }
}