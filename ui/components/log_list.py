from datetime import datetime

from PyQt5.QtWidgets import QListWidget, QListWidgetItem

from ui.constants import MessageType


class LogList(QListWidget):
    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)
        self.setTextElideMode(3)
        self.setWordWrap(True)

    def addMessage(self, text: str, mtype: MessageType):
        time = datetime.now()
        message = QListWidgetItem(f'{time.hour}:{time.minute} {text}')
        message.setForeground(mtype.value)
        self.addItem(message)
        self.scrollToBottom()
