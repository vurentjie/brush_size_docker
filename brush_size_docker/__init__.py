from builtins import Krita
from krita import DockWidgetFactory, DockWidgetFactoryBase
from .brush_size_docker import BrushSizeDocker
from .brush_size_actions import BrushSizeActions

Krita.addDockWidgetFactory(
    DockWidgetFactory(
        "brush_size_docker",
        getattr(
            DockWidgetFactoryBase, "DockPosition", DockWidgetFactoryBase
        ).DockRight,
        BrushSizeDocker,
    )
)

Krita.addExtension(BrushSizeActions(Krita))
