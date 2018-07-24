#!/usr/bin/env python
# coding:utf-8 :
# Author:   881O
# Created:  2017-07-21
#
import sys
import os
from PyQt5.QtWidgets import (QMessageBox, QPushButton, QLabel, QLineEdit,
                             QAction, QMainWindow, QApplication, QFileDialog)
from PyQt5.QtGui import (QIcon, QFont)
from PIL import Image


class Resizer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.file_or_folder = "folder"
        self.initUI()

    def initUI(self):

        sizeLabel = QLabel("< Picture Max Size >", self)
        sizeLabel.setFont(QFont("SansSerif", 13))
        sizeLabel.resize(230, 30)
        sizeLabel.move(40, 60)

        widthLabel = QLabel("width :", self)
        widthLabel.setFont(QFont("SansSerif", 13))
        widthLabel.move(30, 100)

        heightLabel = QLabel("height :", self)
        heightLabel.setFont(QFont("SansSerif", 13))
        heightLabel.move(240, 100)

        self.widthEdit = QLineEdit("1920", self)
        self.widthEdit.resize(90, 27)
        self.widthEdit.move(110, 105)

        self.heightEdit = QLineEdit("1080", self)
        self.heightEdit.resize(90, 27)
        self.heightEdit.move(330, 105)

        self.inputLabel = QLabel("< Folder Path >", self)
        self.inputLabel.setFont(QFont("SansSerif", 13))
        self.inputLabel.resize(200, 30)
        self.inputLabel.move(40, 160)

        self.inputEdit = QLineEdit(None, self)
        self.inputEdit.resize(350, 25)
        self.inputEdit.move(20, 200)

        button_01 = QPushButton("Reference", self)
        button_01.clicked.connect(self.inputDialog)
        button_01.setFont(QFont("SansSerif", 11))
        button_01.resize(100, 35)
        button_01.move(380, 195)

        outputLabel = QLabel("< Output Directory >", self)
        outputLabel.setFont(QFont("SansSerif", 13))
        outputLabel.resize(200, 30)
        outputLabel.move(40, 250)

        self.outputEdit = QLineEdit(None, self)
        self.outputEdit.resize(350, 25)
        self.outputEdit.move(20, 290)

        button_02 = QPushButton("Reference", self)
        button_02.clicked.connect(self.outputDialog)
        button_02.setFont(QFont("SansSerif", 11))
        button_02.resize(100, 35)
        button_02.move(380, 285)

        button_03 = QPushButton("Resize", self)
        button_03.clicked.connect(self.fileResize)
        button_03.setFont(QFont("SansSerif", 14))
        button_03.resize(120, 45)
        button_03.move(170, 340)

        self.statusBar()

        openWindow = QAction(QIcon(""), "Open", self)
        openWindow.setShortcut("Ctrl+O")
        openWindow.setStatusTip("Open New Window")
        openWindow.triggered.connect(self.Open)

        closeWindow = QAction(QIcon(""), "Exit", self)
        closeWindow.setShortcut("Ctrl+Q")
        closeWindow.setStatusTip("Close this Window")
        closeWindow.triggered.connect(self.Exit)

        choiceFile = QAction(QIcon(""), "File", self)
        choiceFile.setShortcut("Alt+F")
        choiceFile.setStatusTip("Choose from File")
        choiceFile.triggered.connect(self.fromFile)

        choiceFolder = QAction(QIcon(""), "Folder", self)
        choiceFolder.setShortcut("Ctrl+F")
        choiceFolder.setStatusTip("Choose from Folder")
        choiceFolder.triggered.connect(self.fromFolder)

        menubar = self.menuBar()

        windowMenu = menubar.addMenu("&Window")
        choiceMenu = menubar.addMenu("&Choice")
        windowMenu.addAction(openWindow)
        windowMenu.addAction(closeWindow)
        choiceMenu.addAction(choiceFile)
        choiceMenu.addAction(choiceFolder)
        self.setGeometry(300, 300, 500, 420)
        self.setMinimumHeight(420)
        self.setMinimumWidth(500)
        self.setMaximumHeight(420)
        self.setMaximumWidth(500)
        self.setWindowTitle("Resizer")
        self.show()

    def Open(self):
        os.system("python resizer.pyw")

    def Exit(self):
        reply = QMessageBox.question(self, "Message", "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            sys.exit(0)
        else:
            pass

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Message", "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def fromFile(self):
        self.inputLabel.setText("< File Path >")
        self.file_or_folder = "file"

    def fromFolder(self):
        self.inputLabel.setText("< Folder Path >")
        self.file_or_folder = "folder"

    def inputDialog(self):
        if self.file_or_folder == "file":
            fname = QFileDialog.getOpenFileName(self, "Open File", "C:/Users")
            fname = fname[0]
        else:
            fname = QFileDialog.getExistingDirectory(self, "Open Folder", "C:/Users")
        self.inputEdit.setText(fname)

    def outputDialog(self):
        fname = QFileDialog.getExistingDirectory(self, "Open Folder", "C:/Users")
        self.outputEdit.setText(fname)

    def fileResize(self):
        pictures = []

        try:
            width = int(self.widthEdit.text())
            height = int(self.heightEdit.text())
        except:
            self.statusBar().showMessage("Size must be int(), not str().")
            return None

        dir_num = 1
        all, number = 0, 0
        broken_file = ""
        Path = self.inputEdit.text()

        if self.file_or_folder == "file":
            all, number = 1, 1
            try:
                root, ext = os.path.splitext(os.path.basename(Path))
                files = os.listdir(Path.rstrip(root+ext))
            except:
                self.statusBar().showMessage("Wrong Path!  Not this directory.")
                return None
            while True:
                if "resizer("+str(dir_num)+")" in files:
                    dir_num += 1
                else:
                    break
            if ext in [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG",
                       ".gif", ".GIF", ".tiff", ".TIFF", ".bmp", ".BMP"]:
                img = Image.open(Path)
                if img.size[0] > width or img.size[1] > height:
                    if width/height >= img.size[0]/img.size[1]:
                        x, y = round(img.size[0]*height/img.size[1]), height
                    else:
                        x, y = width, round(img.size[1]*width/img.size[0])
                    try:
                        img.thumbnail((x, y), Image.ANTIALIAS)
                        size = "(" + str(x) + "x" + str(y) + ")"
                        if len(self.outputEdit.text()) == 0:
                            os.mkdir(Path.rstrip(root+ext)+"/resizer("+str(dir_num)+")")
                            img.save(Path.rstrip(root+ext) +
                                     "resizer("+str(dir_num)+")/"+root+size+ext, "PNG", quality=100, optimaize=True)
                        else:
                            img.save(self.outputEdit.text()+"/"+root+size +
                                     ext, "PNG", quality=100, optimaize=True)
                    except:
                        broken_file += root+ext
                        self.statusBar().showMessage("This is broken data!")
                        if len(self.outputEdit.text()) != 0:
                            f = open(self.outputEdit.text()+"/Message.txt", "a")
                        else:
                            f = open(Path.rstrip(root+ext) +
                                     "/resizer("+str(dir_num)+")/Message.txt", "a")
                        f.write(Path+" is broken.\n")
                        f.close()
                        QMessageBox.warning(self, "Broken Files", broken_file)
        else:
            try:
                files = os.listdir(Path)
            except:
                self.statusBar().showMessage("Wrong Path!  Not this directry.")
                return None
            while True:
                if "resizer("+str(dir_num)+")" in files:
                    dir_num += 1
                else:
                    break
            if len(self.outputEdit.text()) == 0:
                os.mkdir(Path+"/resizer("+str(dir_num)+")")
            for file in files:
                root, ext = os.path.splitext(file)
                if ext in [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG",
                           ".gif", ".GIF", ".tiff", ".TIFF", ".bmp", ".BMP"]:
                    img = Image.open(Path+"/"+file)
                    if img.size[0] > width or img.size[1] > height:
                        all += 1
                        pictures.append(file)
            for picture in pictures:
                root, ext = os.path.splitext(picture)
                img = Image.open(Path+"/"+picture)
                if width/height >= img.size[0]/img.size[1]:
                    x, y = round(img.size[0]*height/img.size[1]), height
                else:
                    x, y = width, round(img.size[1]*width/img.size[0])
                try:
                    img.thumbnail((x, y), Image.ANTIALIAS)
                    size = "(" + str(x) + "x" + str(y) + ")"
                    if len(self.outputEdit.text()) != 0:
                        img.save(self.outputEdit.text()+"/"+root+size +
                                 ext, "PNG", quality=100, optimaize=True)
                    else:
                        img.save(Path+"/resizer("+str(dir_num)+")/"+root +
                                 size+ext, ext.lstrip("."), quality=100, optimaize=True)
                    number += 1
                    self.statusBar().showMessage(str(number)+" / "+str(all))
                except:
                    broken_file += root+ext+"\n"
                    self.statusBar().showMessage("This is broken data!")
                    if len(self.outputEdit.text()) != 0:
                        f = open(self.outputEdit.text()+"/Message.txt", "a")
                    else:
                        f = open(Path+"/resizer("+str(dir_num)+")/Message.txt", "a")
                    f.write(Path+"/"+root+ext+" is broken.\n")
                    f.close()
        if len(broken_file) != 0:
            QMessageBox.warning(self, "Broken Files", broken_file.rstrip("\n"))
        self.statusBar().showMessage(str(number)+"/"+str(all)+"  Finished!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Resizer()
    sys.exit(app.exec_())
