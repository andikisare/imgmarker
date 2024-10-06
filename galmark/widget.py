from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout, QLineEdit, QFrame, QLineEdit, QSizePolicy
from PyQt6.QtCore import Qt
from galmark import __dirname__, __icon__, __heart_solid__, __heart_clear__

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Raised)

class PosWidget(QWidget):
    """
    Shows coordinates
    """
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        # pix text 
        self.x_text = QLineEdit()
        self._text_setup(self.x_text)
        self.y_text = QLineEdit()
        self._text_setup(self.y_text)

        self.pix_label = QLabel()
        self._label_setup(self.pix_label,'Pixel:')

        # wcs text 
        self.ra_text = QLineEdit()
        self._text_setup(self.ra_text)
        self.dec_text = QLineEdit()
        self._text_setup(self.dec_text)

        self.wcs_label = QLabel()
        self._label_setup(self.wcs_label,'WCS:')

        # Add widgets to layout
        layout.addStretch(1)
        layout.addWidget(self.pix_label)
        layout.addWidget(self.x_text)
        layout.addWidget(self.y_text)
        layout.addWidget(self.wcs_label)
        layout.addWidget(self.ra_text)
        layout.addWidget(self.dec_text)
        layout.addStretch(1)

    def _text_setup(self,widget:QLineEdit):
        widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widget.setReadOnly(True)
        widget.setFixedHeight(30)
        widget.setFixedWidth(100)
        widget.setSizePolicy(*[QSizePolicy.Policy.Fixed]*2)

    def _label_setup(self,label:QLabel,text:str):
        label.setText(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        label.setFixedHeight(30)