import os
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from .panorama_navigator import PanoramaNavigator

class PanoramaPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.panorama_navigator = None
        self.action = None
        self.active = False

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
        self.action = QAction(QIcon(icon_path), "Panoramatická navigace", self.iface.mainWindow())
        self.action.setCheckable(True)
        self.action.triggered.connect(self.toggle_plugin)

        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Panoramatická navigace", self.action)

    def unload(self):
        if self.action:
            self.iface.removeToolBarIcon(self.action)
            self.iface.removePluginMenu("&Panoramatická navigace", self.action)
            self.action = None

        if self.panorama_navigator:
            self.panorama_navigator.deactivate()
            self.panorama_navigator = None

    def toggle_plugin(self):
        if self.active:
            self.deactivate_plugin()
        else:
            self.activate_plugin()

    def activate_plugin(self):
        self.panorama_navigator = PanoramaNavigator(self.iface)
        if self.panorama_navigator.layer:
            self.panorama_navigator.activate()
            self.iface.messageBar().pushMessage("Panoramatická navigace", "Plugin byl aktivován", level=0, duration=3)
            self.action.setChecked(True)
            self.active = True
        else:
            self.iface.messageBar().pushMessage("Panoramatická navigace", "Žádná platná vektorová vrstva není aktivní", level=2, duration=5)
            self.action.setChecked(False)
            self.panorama_navigator = None

    def deactivate_plugin(self):
        if self.panorama_navigator:
            self.panorama_navigator.deactivate()
            self.panorama_navigator = None
        self.iface.messageBar().pushMessage("Panoramatická navigace", "Plugin byl deaktivován", level=0, duration=3)
        self.action.setChecked(False)
        self.active = False

def classFactory(iface):
    return PanoramaPlugin(iface)
