#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from krita import Extension

try:
    from PyQt6.QtCore import (
        pyqtSlot,
        QPointF,
        Qt,
        QTimer,
    )
    from PyQt6.QtGui import (
        QBrush,
        QColor,
        QFont,
        QIcon,
        QImage,
        QPainter,
        QPalette,
        QPen,
        QPixmap,
        QStandardItem,
        QStandardItemModel,
    )
    from PyQt6.QtWidgets import (
        QApplication,
        QListView,
        QSizePolicy,
        QTabWidget,
        QVBoxLayout,
        QWidget,
    )

except:
    from PyQt5.QtCore import (
        pyqtSlot,
        QPointF,
        Qt,
        QTimer,
    )
    from PyQt5.QtGui import (
        QBrush,
        QColor,
        QFont,
        QIcon,
        QImage,
        QPainter,
        QPalette,
        QPen,
        QPixmap,
        QStandardItem,
        QStandardItemModel,
    )
    from PyQt5.QtWidgets import (
        QApplication,
        QListView,
        QSizePolicy,
        QTabWidget,
        QVBoxLayout,
        QWidget,
    )


class BrushSizeActions(Extension):

    def __init__(self, parent):
        super().__init__(parent)
        self._toolbarActions = []

    def setup(self):
        pass

    def createActions(self, window):
        for dock in window.dockers():
            if dock.objectName() == "brush_size_docker" and not dock.property(
                "brush_size_actions"
            ):
                dock.setProperty("brush_size_actions", "1")
                action = window.createAction(
                    "decreaseBrushSizeDocker", "Decrease brush size docker", ""
                )
                action.script = None
                action.triggered.connect(lambda: dock.decreaseBrushSize())
                action.setCheckable(False)

                action = window.createAction(
                    "increaseBrushSizeDocker", "Increase brush size docker", ""
                )
                action.script = None
                action.triggered.connect(lambda: dock.increaseBrushSize())
                action.setCheckable(False)
                break
