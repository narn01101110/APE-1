import QtQuick 2.0
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import Qt.labs.platform 1.0
import Qt.labs.settings 1.0

GroupBox {
  title: qsTr("Data")

  FileDialog {
    id: fileDialog
    nameFilters: [qsTr("JSON files (*.json)"), qsTr("All files (*)")]
    title: qsTr("Save File")
    folder: StandardPaths.writableLocation(StandardPaths.HomeLocation)
    property bool openMode: true
    fileMode: openMode ? FileDialog.OpenFile : FileDialog.SaveFile

    onAccepted: {
      settings.file = file
      if (openMode) {
        nodeHandler.appInterface.importFrom(file)
        nodeHandler.refreshAll()
      } else {
        nodeHandler.appInterface.saveAs(file)
      }
    }

    onVisibleChanged: {
      if (visible) {
        currentFile = settings.file
      }
    }
  }

  RowLayout {
    anchors.fill: parent

    Button {
      Layout.fillWidth: true
      text: qsTr("Refresh")
      onClicked: {
        nodeHandler.appInterface.refresh()
        nodeHandler.procInterface.refreshEprocs()
      }
    }

    Button {
      Layout.fillWidth: true
      text: qsTr("New from Template")
      onClicked: nodeHandler.appInterface.startTemplate(false)
    }

    Button {
      Layout.fillWidth: true

      text: qsTr("Import...")
      onClicked: {
        fileDialog.openMode = true
        fileDialog.open()
      }
    }

    Button {
      Layout.fillWidth: true

      text: qsTr("Export...")
      onClicked: {
        fileDialog.openMode = false
        fileDialog.open()
      }
    }
  }

  Settings {
    id: settings
    category: "file"
    property alias folder: fileDialog.folder
    property url file: ""
  }
}
