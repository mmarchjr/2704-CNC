"""
Author: nagan319
Date: 2024/06/12
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QMessageBox
from .view_template import ViewTemplate
from ..widgets.router_widget import RouterWidget

from ..controllers.router_controller import RouterController

from ..logging import logger

class RouterView(ViewTemplate):
    """
    View for handling CNC routers. 
    """
    def __init__(self, session, part_preview_dir: str):
        super().__init__()

        self.controller = RouterController(session, part_preview_dir)
        self.widget_map = {}

        self._setup_ui()
        self.populate_router_widgets() 
        logger.debug("Successfully initialized RouterView.")

    def _setup_ui(self):
        """ Initialize widget ui. """
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        self.import_button = QPushButton("Add Router")
        self.import_button.pressed.connect(self.add_router)

        import_button_wrapper = QWidget()
        import_button_wrapper_layout = QHBoxLayout()
        import_button_wrapper_layout.addStretch(2)
        import_button_wrapper_layout.addWidget(self.import_button, 1)
        import_button_wrapper_layout.addStretch(2)
        import_button_wrapper.setLayout(import_button_wrapper_layout)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area, 1)
        main_layout.addWidget(import_button_wrapper)  
        main_widget.setLayout(main_layout)

        self.__init_template_gui__("Manage Routers", main_widget)
    
    def populate_router_widgets(self):
        """Populate widgets for all routers already in the database."""
        try:
            routers = self.controller.get_all()
            for router in routers:
                router_widget = RouterWidget(router.id, self.controller._get_preview_image_path(router.id), self.controller)
                router_widget.selectionChanged.connect(self.on_selection_changed)
                router_widget.deleteRequested.connect(self.on_delete_requested)
                self.scroll_layout.addWidget(router_widget)
                self.widget_map[router.id] = router_widget
                logger.debug(f"Router widget added successfully for router ID: {router.id}")
            self._update_button_amount()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while populating router widgets: {e}")
            logger.error(f"Error populating router widgets: {str(e)}")

    def add_router(self) -> None:
        """
        Add a new router.
        """
        try: 
            router = self.controller.add_new()
            if router is not None:
                new_router_widget = RouterWidget(router.id, self.controller._get_preview_image_path(router.id), self.controller)
                new_router_widget.selectionChanged.connect(self.on_selection_changed)
                new_router_widget.deleteRequested.connect(self.on_delete_requested)
                self.scroll_layout.addWidget(new_router_widget)
                self.widget_map[router.id] = new_router_widget
                self._update_button_amount()
                logger.debug(f"New router added successfully.")
            else:
                QMessageBox.warning(self, "Operation Failed", "A new router could not be added.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while adding a new router: {e}")
            logger.error(f"Error adding new router: {str(e)}")

    def on_selection_changed(self) -> None:
        """ Changes selection status of all routers. """
        for router_widget in self.widget_map.values():
            router_widget.update_selection_status()

    def on_delete_requested(self, router_id: str) -> None:
        """ Delete widget from db. """
        try:
            self.controller.remove(router_id)
            widget = self.widget_map.pop(router_id)
            widget.setParent(None) 
            widget.deleteLater()
            self._update_button_amount()
        except Exception as e:
            logger.error(f"Encountered exception while removing router from db: {e}")

    def _update_button_amount(self) -> None:
        """ Update to reflect amount of widgets in db."""
        try:
            self.import_button.setText(f"Add Routers: {self.controller.get_amount()}/{self.controller.MAX_ROUTER_AMOUNT}")
        except Exception as e:
            logger.error(f"Encountered exception while updating amount widget: {e}")
