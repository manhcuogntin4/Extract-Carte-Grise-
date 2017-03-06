# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'annotation.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

import numpy
import cv2
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PIL import Image
import glob
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
IMAGES_FOLDER="nomEpouse/"
ANNOTAIONS_FILE="nomepouse.txt"

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog, image_list, images_annotation, start_position, strFolderName, parent=None):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(630, 534)
        #Init values for 
        self.images=image_list
        self.i=start_position
        self.annotations=images_annotation
        self.strFolderName=strFolderName

        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(270, 480, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.labe_image = QtGui.QLabel(Dialog)
        self.labe_image.setGeometry(QtCore.QRect(90, 120, 341, 151))
        self.labe_image.setObjectName(_fromUtf8("labe_image"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(90, 100, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        
        self.AnnotationText = QtGui.QLineEdit(Dialog)
        self.AnnotationText.setGeometry(QtCore.QRect(90, 380, 350, 27))
        self.AnnotationText.setObjectName(_fromUtf8("AnnotationText"))
        self.AnnotationText.editingFinished.connect(self.saveFileAnnotation)

        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(450, 384, 200, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.AnnotationTextPrefix = QtGui.QLineEdit(Dialog)
        self.AnnotationTextPrefix.setGeometry(QtCore.QRect(90, 340, 200, 27))
        self.AnnotationTextPrefix.setObjectName(_fromUtf8("AnnotationText"))
        
        self.label_prefix=QtGui.QLabel(Dialog)
        self.label_prefix.setGeometry(QtCore.QRect(300, 344, 130, 20))
        self.label_prefix.setObjectName(_fromUtf8("label_prefix"))

        
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(90, 300, 81, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_image = QtGui.QLabel(Dialog)
        self.label_image.setGeometry(QtCore.QRect(190, 300, 68, 17))
        self.label_image.setObjectName(_fromUtf8("label_image"))
        self.Next = QtGui.QPushButton(Dialog)
        self.Next.setGeometry(QtCore.QRect(90, 420, 99, 27))
        self.Next.setObjectName(_fromUtf8("Next"))
        self.Next.clicked.connect(self.nextImage)
        self.Previous = QtGui.QPushButton(Dialog)
        self.Previous.setGeometry(QtCore.QRect(210, 420, 99, 27))
        self.Previous.setObjectName(_fromUtf8("Previous"))
        self.Previous.clicked.connect(self.previousImage)
        self.Delete = QtGui.QPushButton(Dialog)
        self.Delete.setGeometry(QtCore.QRect(330, 420, 99, 27))
        self.Delete.setObjectName(_fromUtf8("Delete"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.savePosition)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.labe_image.setPixmap(QtGui.QPixmap(self.strFolderName+str(self.i+1)+".bin.png"))
        self.AnnotationText.setFocus()
        self.label_image.setText(str(self.i+1))

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "AnnotationTool", None))
        self.labe_image.setText(_translate("Dialog", "TextLabel", None))
        self.label_2.setText(_translate("Dialog", "Image to Annotation", None))
        self.label_3.setText(_translate("Dialog", "Annotation Text", None))
        self.label_prefix.setText(_translate("Dialog", "Prefix", None))
        self.label_4.setText(_translate("Dialog", "# of image:", None))
        self.label_image.setText(_translate("Dialog", "TextLabel", None))
        self.Next.setText(_translate("Dialog", "Next", None))
        self.Next.setShortcut(_translate("Dialog", "Ctrl+N", None))
        self.Previous.setText(_translate("Dialog", "Previous", None))
        self.Previous.setShortcut(_translate("Dialog", "Ctrl+P", None))
        self.Delete.setText(_translate("Dialog", "Delete", None))
        self.Delete.setShortcut(_translate("Dialog", "Ctrl+D", None))


    def nextImage(self):
        if(self.i<len(self.images) and(self.AnnotationText.text()!="") ):
                self.i=self.i+1
                self.AnnotationText.setFocus()
                self.labe_image.setPixmap(QtGui.QPixmap(self.strFolderName+str(self.i+1)+".bin.png"))
                self.label_image.setText(str(self.i+1))
                annotationText=self.AnnotationText.text()
                annotationTextPrefix=self.AnnotationTextPrefix.text()
                filename=self.strFolderName+str(self.i)+".gt.txt"
                writeFileAnnotation(filename,annotationTextPrefix+" "+annotationText)
                self.AnnotationText.setText("")
        else:
            warningMessage("You must enter the annotation Text")
            self.AnnotationText.setFocus()


              
    def previousImage(self):
        if(self.i<len(self.images) and self.i>=1):
                self.i=self.i-1
                self.AnnotationText.setFocus()
                self.labe_image.setPixmap(QtGui.QPixmap(self.strFolderName+str(self.i+1)+".bin.png"))
                self.label_image.setText(str(self.i+1))
                filename=self.strFolderName + str(self.i+1)+".gt.txt"
                prefix, text= readFileAnnotation(filename)
                self.AnnotationText.setText(text)
                self.AnnotationTextPrefix.setText(prefix)
                annotationText=self.AnnotationText.text()
                annotationTextPrefix=self.AnnotationTextPrefix.text()
                writeFileAnnotation(filename,annotationTextPrefix+" "+annotationText)
                #self.AnnotationText.setText("")
        else:
            warningMessage("You must enter the annotation Text")
            self.AnnotationText.setFocus()

    def saveFileAnnotation(self):
        annotationText=self.AnnotationText.text()
        annotationTextPrefix=self.AnnotationTextPrefix.text()
        if(annotationText!=""):
            filename=self.strFolderName+str(self.i+1)+".gt.txt"
            writeFileAnnotation(filename,annotationTextPrefix+" "+annotationText)
            self.Next.setFocus()
    def getPosition(self):
        return self.i
    def savePosition(self):
        f=open("init.txt","w")
        f.write(str(self.i))
        f.close()
        sys.exit()


def warningMessage(strWarning):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(strWarning)
    msg.setWindowTitle("Value not correct")
    retval = msg.exec_()



def readFileAnnotations(strFileName):
    print strFileName
    f = open(strFileName, 'r')
    annotations=[]
    for line in f:
        annotations.append(line)
    f.close()
    return annotations

def readFileAnnotation(strFileName):
    try:
        f=open(strFileName,'r')
        annotationText=f.read(50)
        f.close()
        index=annotationText.find(":")
        return annotationText[0:index+1], annotationText[index+2:]
    except IOError:
        warningMessage("File not Found")


def readFileImages(strFolderName):
    print strFolderName
    image_list = []
    st=strFolderName+"*.png"
    for filename in glob.glob(st): #assuming gif
        image_list.append(filename)
    return image_list


def writeFileAnnotation(strFileName, strContent):
	f=open(strFileName,'w')
	if(strContent!=""):
		f.write(strContent)
		f.close()
	else:
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setText("Annotation value is not set")
		msg.setInformativeText("This is additional information")
		msg.setWindowTitle("Value not correct")
	


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    strFileName=ANNOTAIONS_FILE
    strFolderName=IMAGES_FOLDER
    image_list=readFileImages(strFolderName)
    images_annotation=readFileAnnotations(strFolderName+strFileName)
    f=open("init.txt",'r')
    start=int(f.read())
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog, image_list,images_annotation,start, strFolderName)
    Dialog.show()
    sys.exit(app.exec_())

