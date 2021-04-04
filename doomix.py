#! /usr/bin/env python3
#
#   doomix.py   WJ121
#

'''DOOM launcher'''

import sys
import os
import shlex

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QUrl, QDirIterator
from PyQt5.QtWidgets import (QApplication, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QLineEdit, QPushButton, QToolButton, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent


class MainWindow(QDialog):
    '''main window'''

    APP_TITLE = 'DOOMix'
    APP_ICON = '/usr/share/doomix/doomix.png'
    IMAGE = 'doomix_logo.png'
    ABOUT_ICON = 'skull_icon.png'
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
        self.exe_browse_button.clicked.connect(self.onclick_exe_browse_button)
        layout.addWidget(self.exe_browse_button, 1, 2)

        # add-ons edit line + browse button
        addons_label = QLabel(self)
        addons_label.setText('Add-ons:')
        layout.addWidget(addons_label, 2, 0)

        self.addons_line = QLineEdit(self)
        layout.addWidget(self.addons_line, 2, 1)

        self.addons_browse_button = QPushButton('...', self)
        self.addons_browse_button.clicked.connect(self.onclick_addons_browse_button)
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
        self.about_button.clicked.connect(self.onclick_about)
        layout.addWidget(self.about_button)

        layout.addSpacing(int(MainWindow.WIDTH * 0.5))

        self.launch_button = QPushButton('Launch')
        self.launch_button.clicked.connect(self.onclick_launch)
        layout.addWidget(self.launch_button)

        widget.setLayout(layout)
        return widget

    def onclick_exe_browse_button(self):
        '''browse for executable'''

        filename, _ = QFileDialog.getOpenFileName(self, 'Select DOOM executable', '/')
        if not filename:
            # cancel
            return

        if not (os.path.isfile(filename) and os.access(filename, os.X_OK)):
            self.alertbox('{}: not executable'.format(filename))
            return

        # put selected filename into the edit line
        self.exe_line.setText(filename)

    def alertbox(self, msg):
        '''display an alert'''

        QMessageBox.warning(self, 'DOOMix', msg, QMessageBox.Ok)

    def onclick_addons_browse_button(self):
        '''browse for addons'''

        filenames, _ = QFileDialog.getOpenFileNames(self, 'Select add-ons', '~', 'WAD files (*.WAD *.wad *.PK3 *.pk3)')
        if not filenames:
            # cancel
            return

        # add selected add-ons to the edit line
        filenames.insert(0, '')
        line = self.addons_line.text()
        line += ' -file '.join(filenames)
        self.addons_line.setText(line)

    def onclick_about(self):
        '''show about box'''

        about = QMessageBox(QMessageBox.Information, 'About DOOMix',
                            'DOOMix is a launcher for the DOOM game, '
                            'made for use with (but not limited to) gzdoom.\n\n'
                            'This is FREE software provided AS IS WITHOUT WARRANTY '
                            'of any kind whatsoever.\n\n'
                            'Copyright 2021 by Walter de Jong <walter@heiho.net>', QMessageBox.Ok)
        icon = QPixmap(MainWindow.ABOUT_ICON)
        about.setIconPixmap(icon)
        about.exec()

    def onclick_launch(self):
        '''launch the executable'''

        prog = self.exe_line.text()
        if not prog:
            self.alertbox('First select the DOOM executable!'.format(filename))
            return

        if not (os.path.isfile(prog) and os.access(prog, os.X_OK)):
            self.alertbox('{}: not executable'.format(prog))
            return

        addons = self.addons_line.text().strip()
        if addons:
            prog += ' ' + addons

        args = self.args_line.text().strip()
        if args:
            prog += ' ' + args

        cmd_arr = shlex.split(prog)
        # launch executable!
        try:
            os.execv(cmd_arr[0], cmd_arr)
        except OSError as err:
            self.alertbox('{}: {}'.format(cmd_arr[0], err.strerror))



if __name__ == '__main__':
    app_ = QApplication(sys.argv)
    main_window_ = MainWindow()
    sys.exit(app_.exec_())


# EOB
