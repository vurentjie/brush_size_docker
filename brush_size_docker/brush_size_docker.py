#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

# This docker is a more compact version of the
# quick_settings_docker that comes with Krita.
# And it only displays brush sizes.

from krita import DockWidget
import sip

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


class ShrinkableListView(QListView):
    def sizeHint(self):
        return self.minimumSizeHint()


class BrushSizeDocker(DockWidget):

    def __init__(self):
        super(BrushSizeDocker, self).__init__()

        self._selectedIndex = 0
        self._brushSize = 0
        self._sizesList = [
            4,
            5,
            6,
            7,
            8,
            10,
            12,
            14,
            16,
            20,
            24,
            30,
            40,
            50,
            60,
            80,
            100,
            200,
        ]

        self._listView = ShrinkableListView()
        self._listView.setViewMode(QListView.ViewMode.IconMode)
        self._listView.setMovement(QListView.Movement.Static)
        self._listView.setResizeMode(QListView.ResizeMode.Adjust)
        self._listView.setUniformItemSizes(True)
        self._listView.setSelectionMode(
            QListView.SelectionMode.SingleSelection
        )
        self._listView.setMinimumHeight(80)
        self._listView.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored
        )

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setWindowTitle(i18n("Brush Size Docker"))
        tabWidget = QTabWidget()
        layout.addWidget(self._listView)
        self.setWidget(widget)

        self._brushSizeModel = QStandardItemModel()
        self.fillSizesModel()
        self._listView.clicked.connect(self.setBrushSize)

        self._timer = QTimer()
        self._timer.timeout.connect(lambda: self.updateBrush())
        self._timer.start(100)

        self._themeSlotConnected = False

    def canvasChanged(self, canvas):
        if not self._themeSlotConnected:
            view = canvas.view()
            if view:
                win = view.window()
                if win:
                    self._themeSlotConnected = True
                    win.themeChanged.connect(self.fillSizesModel)

    def fillSizesModel(self):
        self._brushSizeModel.clear()
        font = QFont("Arial", 8)

        color = QApplication.palette().color(QPalette.ColorRole.Text).darker(
            140
        ) or QColor(125, 125, 125)

        if color.red() < 34:
            color = QColor(34, 34, 34)

        for s in range(len(self._sizesList)):
            sz = self._sizesList[s]

            item = QStandardItem()
            item.setCheckable(False)
            item.setEditable(False)
            item.setDragEnabled(False)
            item.setFont(font)
            item.setText(str(sz))

            circlePainter = QPainter()
            circlePainter.setRenderHint(QPainter.RenderHint.Antialiasing)

            img = QImage(20, 20, QImage.Format_RGBA8888)
            img.fill(Qt.transparent)

            circlePainter.begin(img)

            brush = QBrush(Qt.SolidPattern)
            brush.setColor(color)

            pen = QPen(color)
            pen.setStyle(Qt.SolidLine)
            pen.setWidth(2)

            circlePainter.setBrush(brush)
            circlePainter.setPen(pen)

            brushSize = (s * 0.5) + 1

            circlePainter.drawEllipse(QPointF(10, 10), brushSize, brushSize)
            circlePainter.end()

            brushImage = QPixmap.fromImage(img)

            item.setIcon(QIcon(brushImage))
            item.setForeground(brush)
            self._brushSizeModel.appendRow(item)

        self._listView.setModel(self._brushSizeModel)

    def decreaseBrushSize(self):
        self.setBrushSizeIndex(max(0, self._selectedIndex - 1))

    def increaseBrushSize(self):
        self.setBrushSizeIndex(
            min(len(self._sizesList) - 1, self._selectedIndex + 1)
        )

    def updateBrush(self):
        if sip.isdeleted(self._listView):
            return

        win = Krita.instance().activeWindow()
        if not win:
            return

        view = win.activeView()
        if not view:
            return

        sz = view.brushSize()
        if sz is None:
            sz = 10.0

        if self._brushSize is None or sz != self._brushSize:
            self._brushSize = sz
            if self._brushSize > 0 and self._brushSize < self._sizesList[0]:
                self._selectedIndex = 0
            else:
                checked = []
                for s in range(len(self._sizesList)):
                    if self._sizesList[s] <= round(self._brushSize, 2):
                        checked.append(self._sizesList[s])
                        self._selectedIndex = s
            item = self._brushSizeModel.item(self._selectedIndex)
            self._listView.setCurrentIndex(
                self._brushSizeModel.indexFromItem(item)
            )

    def setBrushSizeIndex(self, index):
        item = self._brushSizeModel.item(index)
        self._listView.setCurrentIndex(
            self._brushSizeModel.indexFromItem(item)
        )
        self.setBrushSize(index)

    @pyqtSlot("QModelIndex")
    def setBrushSize(self, index):
        if isinstance(index, int):
            i = index
        else:
            i = index.row()
        self._selectedIndex = i
        brushSize = self._sizesList[i]
        view = Krita.instance().activeWindow().activeView()
        if view:
            view.setBrushSize(brushSize)
