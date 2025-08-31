from qgis.core import QgsFeature, QgsVectorLayer
from qgis.gui import QgsMapTool
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWheelEvent, QKeyEvent

class PanoramaNavigator(QgsMapTool):
    def __init__(self, iface):
        super().__init__(iface.mapCanvas())
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.layer = iface.activeLayer()

        if not isinstance(self.layer, QgsVectorLayer) or not self.layer.isValid():
            self.layer = None
            return

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Up:
            self.select_previous_node()
            event.accept()
        elif event.key() == Qt.Key_Down:
            self.select_next_node()
            event.accept()
        else:
            event.ignore()

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.canvas.zoomIn()
            else:
                self.canvas.zoomOut()
        else:
            if event.angleDelta().y() > 0:
                self.select_next_node()
            else:
                self.select_previous_node()
        event.accept()

    def get_selected_node(self):
        selected = self.layer.selectedFeatures()
        return selected[0] if selected else None

    def get_node_index(self, current_node):
        nodes = list(self.layer.getFeatures())
        node_ids = [f.id() for f in nodes]
        try:
            return node_ids.index(current_node.id()), nodes
        except ValueError:
            return None, nodes

    def get_previous_node(self, current_node):
        idx, nodes = self.get_node_index(current_node)
        if idx is not None and idx > 0:
            return nodes[idx - 1]
        return None

    def get_next_node(self, current_node):
        idx, nodes = self.get_node_index(current_node)
        if idx is not None and idx < len(nodes) - 1:
            return nodes[idx + 1]
        return None

    def select_previous_node(self):
        current_node = self.get_selected_node()
        prev_node = self.get_previous_node(current_node) if current_node else None
        if prev_node:
            self.select_node(prev_node)

    def select_next_node(self):
        current_node = self.get_selected_node()
        next_node = self.get_next_node(current_node) if current_node else None
        if next_node:
            self.select_node(next_node)

    def select_node(self, node):
        if node:
            self.layer.selectByIds([node.id()])
            self.canvas.setCenter(node.geometry().asPoint())
            self.canvas.refresh()

    def activate(self):
        self.canvas.setMapTool(self)

    def deactivate(self):
        self.canvas.unsetMapTool(self)
