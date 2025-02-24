"""This module contains custom PyQt widgets for Image Marker."""
from .pyqt import Qt, QLabel, QWidget, QHBoxLayout, QLineEdit, QFrame, QLineEdit, QSizePolicy, QFileDialog
import os

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setLineWidth(0)
        self.setMidLineWidth(1)
        self.setMinimumHeight(1)

class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setLineWidth(0)
        self.setMidLineWidth(1)
        self.setMinimumHeight(1)

class PosWidget(QWidget):
    """
    Shows coordinates
    """
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.sep = QVLine()
       
        # pix text 
        self.x_text = QLineEdit()
        self._text_setup(self.x_text)
        self.y_text = QLineEdit()
        self._text_setup(self.y_text)
        
        self.x_label = QLabel()
        self._label_setup(self.x_label,'X:')
        self.y_label = QLabel()
        self._label_setup(self.y_label,'Y:')

        # wcs text 
        self.ra_text = QLineEdit()
        self._text_setup(self.ra_text)
        self.dec_text = QLineEdit()
        self._text_setup(self.dec_text)

        self.ra_label = QLabel()
        self._label_setup(self.ra_label,'RA:')
        self.dec_label = QLabel()
        self._label_setup(self.dec_label,'DEC:')

        # Add widgets to layout
        layout.addStretch(1)
        layout.addWidget(self.x_label)
        layout.addWidget(self.x_text)
        layout.addWidget(self.y_label)
        layout.addWidget(self.y_text)
        layout.addWidget(self.sep)
        layout.addWidget(self.ra_label)
        layout.addWidget(self.ra_text)
        layout.addWidget(self.dec_label)
        layout.addWidget(self.dec_text)
        layout.addStretch(1)

    def _text_setup(self,widget:QLineEdit):
        font = widget.font()
        font.setPointSizeF(font.pointSizeF()*0.75)
        widget.setFont(font)

        widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widget.setReadOnly(True)
        widget.setFixedHeight(20)
        widget.setFixedWidth(90)
        widget.setSizePolicy(*[QSizePolicy.Policy.Fixed]*2)

    def _label_setup(self,label:QLabel,text:str):
        font = label.font()
        font.setPointSizeF(font.pointSizeF()*0.75)
        label.setFont(font)

        label.setText(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        label.setFixedHeight(20)

    def cleartext(self):
        self.x_text.setText('')
        self.y_text.setText('')
        self.ra_text.setText('')
        self.dec_text.setText('')

    def hidewcs(self):
        self.ra_label.hide()
        self.dec_label.hide()
        self.ra_text.hide()
        self.dec_text.hide()
        self.sep.hide()

    def showwcs(self):
        self.ra_label.show()
        self.dec_label.show()
        self.ra_text.show()
        self.dec_text.show()
        self.sep.show()
        
class RestrictedLineEdit(QLineEdit):
    def __init__(self,forbidden_keys:list=[]):
        super().__init__()
        self.forbidden_keys = forbidden_keys

    def keyPressEvent(self, a0):
        if not a0.key() in self.forbidden_keys: 
            return super().keyPressEvent(a0)
        
    def focusOutEvent(self, a0):
        if self.text() == '': self.setText(self.placeholderText())
        return super().focusOutEvent(a0)
    
class DefaultDialog(QFileDialog):
    def __init__(self,directory=os.path.expanduser('~')):
        #make this work with file dialog names on MacOS
        #default to user's home directory if a path isn't given. 
        # Create a QFileDialog instance
        super().__init__()
        self.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        self.setFileMode(QFileDialog.FileMode.Directory)
        self.setDirectory(directory)
        self.closed = False

    def closeEvent(self, a0):
        self.closed = True
        return super().closeEvent(a0)
    
    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key.Key_Escape: self.close()
        else: return super().keyPressEvent(a0)

    def selectedFiles(self):
        if self.closed: return None
        else: return super().selectedFiles()