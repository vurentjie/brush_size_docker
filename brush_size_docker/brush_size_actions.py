#
#  SPDX-License-Identifier: GPL-3.0-or-later
#

from krita import Extension

class BrushSizeActions(Extension):
    def setup(self):
        pass

    def createActions(self, window):
        for dock in window.dockers():
            if dock.objectName() == "brush_size_docker" and not dock.property("brush_size_actions"):
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
