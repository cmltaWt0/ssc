#! /usr/bin/env python3
# coding=utf-8

import sys
import os
import socket

from PyQt4 import QtGui, QtCore


class QtDeleter(QtGui.QWidget):

    """ Main Client Window. """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 200, 550, 150)
        self.setWindowTitle("SSC session deleter")
        self.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.realpath(__file__)) +
                                       '/ssc.png'))
        self.button = QtGui.QPushButton('DelSession', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(20, 20)
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.sendRequest)
        self.setFocus()

        self.edit = QtGui.QLineEdit(self)
        self.edit.setGeometry(130, 22, 400, 25)
        self.edit.move(130, 22)

        self.label = QtGui.QLabel('Input LOGIN-NAME into edit box above.', self)
        self.label.setMinimumWidth(400)
        self.label.move(130, 82)

        self.name = None
        self.show()

    def sendRequest(self):
        s = socket.socket()
        host = '127.0.0.1'  # TODO Add config for server ip and port
        port = 0000

        try:
            s.connect((host, port))
        except Exception as e:
            self.label.setText(str(e))
        else:
            while self.name is None:
                self.showDialog()

            user = bytes(self.name, 'UTF-8')
            s.send(user)
            response = s.recv(64)

            if response == b'ok':
                login_name = bytes(self.edit.text(), 'UTF-8')
                if login_name != b'':  # prevent forever wait when sending empty string
                    s.send(login_name)
                    response = s.recv(24)
                    if response == b'ok':
                        s.send(b'del')
                        msg = s.recv(1024)
                        self.label.setText(msg.decode('UTF-8'))
                    else:
                        self.label.setText(response.decode('UTF-8'))
            else:
                self.label.setText(response.decode('UTF-8'))
        finally:
            s.close()

    def showDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
        if ok:
            if text == '':
                self.name = None
            else:
                self.name = text

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Close window?\n",
            QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No,
            QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = QtDeleter()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
