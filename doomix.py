#! /usr/bin/env python3
#
#   doomix.py   WJ121
#

'''DOOM launcher'''

import sys
import os
import inspect

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QUrl, QDirIterator
from PyQt5.QtWidgets import (QApplication, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QLineEdit, QPushButton, QToolButton, QFileDialog, QSizePolicy)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent


DEBUG = False
DEBUG_COLOR = True


def debug(msg: str) -> None:
    '''print debug message (if in debug mode)'''

    if not DEBUG:
        return

    funcname = inspect.stack()[1][3]

    if DEBUG_COLOR:
        print('\x1b[32m% {}():\x1b[0m {}'.format(funcname, msg))
    else:
        print('% {}(): {}'.format(funcname, msg))



class MainWindow(QDialog):
    '''main window'''

    APP_TITLE = 'Doomix'
    APP_ICON = '/usr/share/doomix/doomix.png'
    IMAGE = 'doom_logo.png'
    WIDTH = 600

    def __init__(self, parent=None):
        '''initialize instance'''

        super().__init__()

        self.setWindowTitle(MainWindow.APP_TITLE)
        self.setWindowIcon(QIcon(MainWindow.APP_ICON))
        self.setFixedWidth(MainWindow.WIDTH)

        self.exe_line = self.exe_browse_button = None
        self.addons_line = self.addons_browse_button = None
        self.args_line = None
        self.about_button = self.launch_button = None

        self.add_widgets()

        self.show()

    def add_widgets(self):
        '''add widgets; make the user interface'''

        layout = QGridLayout()

        # DOOM logo
        img_label = QLabel(self)
        img = QPixmap(MainWindow.IMAGE)
        img_label.setPixmap(img)
        layout.addWidget(img_label, 0, 0, 1, 3)

        # DOOM exe edit line + browse button
        exe_label = QLabel(self)
        exe_label.setText('DOOM exe:')
        layout.addWidget(exe_label, 1, 0)

        self.exe_line = QLineEdit(self)
        self.exe_line.setText(self.find_doom())
        layout.addWidget(self.exe_line, 1, 1)

        self.exe_browse_button = QPushButton('...', self)
        layout.addWidget(self.exe_browse_button, 1, 2)

        # add-ons edit line + browse button
        addons_label = QLabel(self)
        addons_label.setText('Add-ons:')
        layout.addWidget(addons_label, 2, 0)

        self.addons_line = QLineEdit(self)
        layout.addWidget(self.addons_line, 2, 1)

        self.addons_browse_button = QPushButton('...', self)
        layout.addWidget(self.addons_browse_button, 2, 2)

        # extra arguments line (without browse button)
        args_label = QLabel(self)
        args_label.setText('Extra args:')
        layout.addWidget(args_label, 3, 0)

        self.args_line = QLineEdit(self)
        layout.addWidget(self.args_line, 3, 1)

        buttonbar = self.make_buttonbar()
        layout.addWidget(buttonbar, 4, 0, 1, 3)

        self.setLayout(layout)

    @staticmethod
    def find_doom():
        '''Returns path to DOOM executable'''

        for doom in ('gzdoom', 'lxdoom', 'boom'):
            for location in ('/usr/bin', '/usr/local/bin', '/usr/games'):
                path = os.path.join(location, doom)
                if os.path.exists(path):
                    return path
        # not found
        return ''

    def make_buttonbar(self):
        '''Returns bottom buttonbar widget'''

        widget = QWidget()
        layout = QHBoxLayout()

        self.about_button = QPushButton('About')
        layout.addWidget(self.about_button)

        layout.addSpacing(int(MainWindow.WIDTH * 0.5))

        self.launch_button = QPushButton('Launch')
        layout.addWidget(self.launch_button)

        widget.setLayout(layout)
        return widget



if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        DEBUG = True

    app_ = QApplication(sys.argv)
    main_window_ = MainWindow()
    sys.exit(app_.exec_())


# EOB
