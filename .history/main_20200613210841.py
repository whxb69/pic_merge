import PIL.Image as Image
from ui import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cgitb
import math
from xml.etree import ElementTree as ET
import time
import os
import PyQt5.sip
import sip

cgitb.enable()

class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.setupUi(self)
        self.setMouseTracking(True)
        self.rlist = rlist(self)
        # self.rlist.setMouseTracking(True)
        self.rlist.setGeometry(0.45*self.screenWidth+50,0.15*self.screenHeight,
                                0.42*self.screenWidth,0.42*self.screenWidth)
        self.setpics()
    
    def mouseMoveEvnet(self, event):
        super().mouseMoveEvnet(event)
        print(event.x())
        
    def setpics(self):
        #判断是否为图片
        def is_img(ext):
            ext = ext.lower()
            if ext in ['.jpg','.png','.jepg']:
                return True
            else:
                return False
        pic= []
        #将图片加入工作列表
        for item in os.listdir(os.getcwd()):
            if is_img(os.path.splitext(item)[1]):
                pic = QPixmap(item)
                pitem = QListWidgetItem(QtGui.QIcon(pic.scaled(QtCore.QSize(120,120))),os.path.splitext(item)[0])
                pitem.setSizeHint(QtCore.QSize(100,100))
                self.plist.addItem(pitem)
                # self.rlist.addItem(pitem)
        

    def merge(self):
        # basedir = ''
        p1dir = '1.jpg'
        p1 = Image.open(p1dir,'r')
        print(p1.size)
        p2dir = '2.jpg'
        p2 = Image.open(p2dir,'r')
        print(p2.size)
        res = Image.new('RGB', (p1.size[0], p1.size[1]*2))
        res.paste(p1,(0,0))
        res.paste(p2,(0,p1.size[1]))
        print(res.size)
        res.save('new.jpg')

class rlist(QTableWidget):
    def __init__(self,parent=None):
        super().__init__(parent) 
        self.setAcceptDrops(True)
        # self.setDragEnabled(True)
        self.setRowCount(3)#设置表格的行数
        self.setColumnCount(3)#设置表格的列数
       
    def dragEnterEvent(self, event):
        print(1)
        # 接受事件 将事件转到dropevent
        event.accept()
    
    def dropEvent(self, event):
        source_Widget=event.source()#获取拖入元素的父组件
        items=source_Widget.selectedItems()
        print(items)
        for i in items:
            source_Widget.takeItem(source_Widget.indexFromItem(i).row())#通过实时计算选中的item的索引来删除listItem
            self.addItem(i)
        print('有东西拖入')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tagw = 180 * math.sqrt(app.desktop().width() / 3840)
    tagh = 50 * math.sqrt(app.desktop().height() / 2160)
    win = Mainwindow()
    win.show()
    sys.exit(app.exec_())