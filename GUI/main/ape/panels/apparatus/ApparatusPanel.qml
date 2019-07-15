import QtQuick 2.0
import QtQuick.Controls 2.2
import QtQuick.Controls 1.4 as C1
import QtQuick.Layouts 1.3
import ape.core 1.0
import ape.controls 1.0
import ape.apparatus 1.0

Item {
  id: root

  AppImageTreeModel {
    id: treeModel
    appInterface: nodeHandler.appInterface
  }

  RowLayout {
    anchors.fill: parent
    anchors.margins: Style.singleMargin

    ColumnLayout {
      RowLayout {
        Button {
          text: qsTr("Template")
          onClicked: nodeHandler.appInterface.startTemplate(false)
        }
        Button {
          text: qsTr("Refresh")
          onClicked: nodeHandler.appInterface.refresh()
        }
      }

      AppImageTreeView {
        id: treeView
        Layout.fillWidth: true
        Layout.fillHeight: true
        model: treeModel
      }
    }

    ColumnLayout {
      Layout.fillWidth: false

      GroupBox {
        title: qsTr("Find and Replace")
        GridLayout {
          columns: 2

          Label {
            text: qsTr("Find")
          }

          Label {
            text: qsTr("Replace")
          }

          TextField {
            id: findTextField
            selectByMouse: true
          }

          TextField {
            id: replaceTextField
          }

          Button {
            Layout.columnSpan: 2
            Layout.fillWidth: true
            enabled: findTextField.text && replaceTextField.text
            text: qsTr("Execute")
            onClicked: {
              appInterface.findAndReplace(findTextField.text,
                                          replaceTextField.text)
              findTextField.text = ""
              replaceTextField.text = ""
            }
          }
        }
      }

      RowLayout {
        Button {
          Layout.fillWidth: true
          text: qsTr("Connect All Devices")
          onClicked: {
            nodeHandler.appInterface.connectAll(true)
            nodeHandler.appInterface.refreshEprocs()
          }
        }

        Button {
          Layout.fillWidth: true
          text: qsTr("Disconnect All Devices")
          onClicked: nodeHandler.appInterface.disconnectAll()
        }
      }

      GroupBox {
        title: qsTr("Save")
        RowLayout {
          Layout.fillWidth: true
          Text {
            text: qsTr("Path:")
          }
          TextField {
            Layout.fillWidth: true
          }
          Button {
            Layout.fillWidth: false
            text: "..."
          }
          Button {
            text: qsTr("Save")
          }
        }
      }

      GroupBox {
        Layout.fillWidth: true
        title: qsTr("Watches")

        C1.TableView {
          id: tableView
          anchors.fill: parent
          model: treeModel.watched

          C1.TableViewColumn {
            title: qsTr("Key")
            role: "key"
            width: tableView.width / 2
            resizable: true
          }

          C1.TableViewColumn {
            title: qsTr("Value")
            role: "value"
            width: tableView.width / 2 - 2
            resizable: true
          }
        }
      }

      VerticalFiller {
      }
    }
  }
}
