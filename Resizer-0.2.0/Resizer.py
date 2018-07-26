#!/home/aoba/miniconda3/bin/python
# Coding:   utf-8
# Author:   881O
# Created:  2018-07-25 15:50:18

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from Resizer_ui import Ui_MainWindow
from PIL import Image
import threading
import os
import sys


class Events(object):
    def __init__(self):
        self.home = os.path.expanduser("~")

    def Button_thread(self, func):
        handler = threading.Thread(target=func)
        handler.start()

    def Exit(self):
        reply = QMessageBox.question(None, "Message", "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            sys.exit(0)
        else:
            pass

    def inputDialog(self):
        if self.ui.folderRadio.isChecked():
            fname = QFileDialog.getExistingDirectory(
                None, "Open Folder", self.home)
        else:
            fname = QFileDialog.getOpenFileName(None, "Open File", self.home)
            fname = fname[0]
        self.ui.inputEdit.setText(fname)

    def outputDialog(self):
        fname = QFileDialog.getExistingDirectory(
            None, "Open Folder", self.home)
        self.ui.outputEdit.setText(fname)

    def Resize(self, root, ext, width, height, input_folder, output_folder):
        image = root + ext
        try:
            img = Image.open(os.path.join(input_folder, image))
            if self.ui.constantRadio.isChecked():
                if width/height >= img.size[0]/img.size[1]:
                    x, y = round(img.size[0]*height/img.size[1]), height
                else:
                    x, y = width, round(img.size[1]*width/img.size[0])
            else:
                x, y = width, height

            img_resize = img.resize((x, y), Image.ANTIALIAS)
            size = "(" + str(x) + "x" + str(y) + ")"
            img_resize.save(os.path.join(output_folder, root +
                                         size+ext), quality=100, optimaize=True)
            return ""
        except:
            self.ui.statusbar.showMessage("Filed to load!")
            f = open(os.path.join(output_folder, "Message.txt"), "a")
            f.write(image + " was failed.\n")
            f.close()
            return (image+"\n")

    def getImage(self):
        def makeSaveFolder(files, input_path):
            dir_name = "resizer"
            dir_num = 1
            if dir_name in files:
                while True:
                    dir_name = "resizer" + "("+str(dir_num)+")"
                    if dir_name in files:
                        if len(os.listdir(os.path.join(input_path, dir_name))) == 0:
                            return
                        dir_num += 1
                    else:
                        break
            return dir_name

        try:
            width = int(self.ui.widthEdit.text())
            height = int(self.ui.heightEdit.text())
        except ValueError:
            self.ui.statusbar.showMessage("Size must be int(), not str()")
            return -1

        broken_file = ""
        input_path = self.ui.inputEdit.text()

        output_path = self.ui.outputEdit.text()
        if (len(output_path) > 0) and not os.path.exists(output_path):
            self.ui.statusbar.showMessage(
                "Wrong Output input_path!  Not this directry.")
            return -1

        if self.ui.folderRadio.isChecked():
            images = []
            all, number = 0, 0
            try:
                files = os.listdir(input_path)
            except NameError:
                self.ui.statusbar.showMessage(
                    "Wrong Input input_path!  Not this directry.")
                return -1

            for file in files:
                root, ext = os.path.splitext(file)
                if ext in [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG",
                           ".gif", ".GIF", ".tiff", ".TIFF", ".bmp", ".BMP"]:
                    all += 1
                    images.append(file)
                    if all == 1 and len(output_path) == 0:
                        dir_name = makeSaveFolder(files, input_path)  # input_path is Folder
                        if dir_name is not None:
                            output_path = os.path.join(input_path, dir_name)
                            os.mkdir(output_path)

            for image in images:
                root, ext = os.path.splitext(image)
                number += 1
                broken_file += self.Resize(root, ext, width, height, input_path, output_path)
                self.ui.statusbar.showMessage(str(number)+" / "+str(all))

        else:  # File
            all, number = 1, 1
            if not os.path.exists(input_path):
                self.ui.statusbar.showMessage(
                    "Wrong Input input_path!  Not this directry.")
                return -1

            root, ext = os.path.splitext(os.path.basename(input_path))
            if ext in [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG",
                       ".gif", ".GIF", ".tiff", ".TIFF", ".bmp", ".BMP"]:
                input_path = input_path.rstrip(root+ext)  # input_path: File -> Folder
                if len(output_path) == 0:
                    files = os.listdir(input_path)
                    dir_name = makeSaveFolder(files, input_path)
                    output_path = os.path.join(input_path, dir_name)
                    os.mkdir(output_path)
                broken_file += self.resize(root, ext,
                                           width, height, input_path, output_path)

        if len(broken_file) > 0:
            QMessageBox.warning(None, "Broken Files", broken_file)

        self.ui.statusbar.showMessage(str(number)+"/"+str(all)+"  Finished!")


class Resizer(QMainWindow, Events):
    def __init__(self, parent=None):
        super(Resizer, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionExit.triggered.connect(self.Exit)
        self.ui.inputButton.clicked.connect(self.inputDialog)
        self.ui.outputButton.clicked.connect(self.outputDialog)
        self.ui.resizeButton.clicked.connect(lambda: self.Button_thread(self.getImage))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Message", "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Resizer()
    window.show()
    sys.exit(app.exec_())
