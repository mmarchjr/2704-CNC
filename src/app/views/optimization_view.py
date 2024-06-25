"""
Author: nagan319
Date: 2024/06/13
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from .view_template import ViewTemplate
from PyQt6.QtGui import QPixmap

from sqlalchemy.orm import Session

from ..logging import logger

class OptimizationView(ViewTemplate):
    """
    View for displaying placement optimization. 
    """
    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self._setup_ui()
        logger.debug("Successfully initialized OptimizationView.")

    def _setup_ui(self):
        """ Initialize widget ui. """
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.__init_template_gui__("Generate Layout", main_widget)


