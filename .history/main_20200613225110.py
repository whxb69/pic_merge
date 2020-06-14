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
        
        self.btn_go = QPushButton(self)
        self.btn_go.setText("合并")
        self.btn_go.clicked.connect(self.merge)
        self.btn_go.move(self.rlist.x()+self.rlist.width()*0.4, self.rlist.y()-50)
        # self.btn_go.move(500, 50)
        self.btn_go.show()
        
        
        
        if not os.path.isdir('merged'):
            os.makedirs('merged')
        
        if not os.path.isdir('wait-to-merge'):
            os.makedirs('wait-to-merge')
        
        if not os.path.isdir('results'):
            os.makedirs('results')
    
    def mouseMoveEvnet(self, event):
        super().mouseMoveEvnet(event)
        print(event.x())
        
    def setpics(self):
        self.worklist = [[None,None,None],
                         [None,None,None],
                         [None,None,None]]
        
        self.waitlist = []
        
        #判断是否为图片
        def is_img(ext):
            ext = ext.lower()
            if ext in ['.jpg','.png','.jepg']:
                return True
            else:
                return False
        pic= []
        #将图片加入工作列表
        for item in os.listdir('wait-to-merge'):
            if is_img(os.path.splitext(item)[1]):
                pic = QPixmap('wait-to-merge/'+item)
                pitem = QListWidgetItem(QtGui.QIcon(pic.scaled(QtCore.QSize(120,120))), item)
                pitem.setSizeHint(QtCore.QSize(100,100))
                self.plist.addItem(pitem)
                self.waitlist.append(os.path.splitext(item)[0])
                # self.rlist.addItem(pitem)
        

    def merge(self):
        # basedir = ''
        # p1dir = '1.jpg'
        # p1 = Image.open(p1dir,'r')
        # print(p1.size)
        # p2dir = '2.jpg'
        # p2 = Image.open(p2dir,'r')
        # print(p2.size)
        # res = Image.new('RGB', (p1.size[0], p1.size[1]*2))
        # res.paste(p1,(0,0))
        # res.paste(p2,(0,p1.size[1]))
        # print(res.size)
        # res.save('new.jpg')
        pass
        
        

class rlist(QTableWidget):
    def __init__(self,parent=None):
        super().__init__(parent) 
        self.window = parent
        self.setAcceptDrops(True)
        # self.setDragEnabled(True)
        self.setRowCount(3)#设置表格的行数
        self.setColumnCount(3)#设置表格的列数
        
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)#单元格不能被修改

        self.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
       
    def dragEnterEvent(self, event):
        event.setDropAction(Qt.MoveAction)
        # 接受事件 将事件转到dropevent
        event.accept()
    
    def mouseDoubleClickEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        row,col = self.whichgrid(x, y)
        
        icon = self.window.worklist[row][col]
        self.window.waitlist.insert(0, icon)
        
        pitem = QListWidgetItem(QtGui.QIcon(pic.scaled(QtCore.QSize(120,120))), icon)
        pitem.setSizeHint(QtCore.QSize(100,100))
        self.plist.insertItem(0, pitem)
        
        
        empty = QTableWidgetItem('')
        
        self.setItem(row, col, empty)
        
        
        
        
    def dropEvent(self, event):
        source_Widget=event.source()#获取拖入元素的父组件
        items=source_Widget.selectedItems()
        icon = items[0].icon()
        
        x = event.pos().x()
        y = event.pos().y()
        
        size = int(self.size().width()/3)
        self.setIconSize(QSize(size, size))
        row,col = self.whichgrid(x, y)
        print(row, col)
        
        newItem = QTableWidgetItem(icon,'')
        self.setItem(row, col, newItem)
        self.window.worklist[row][col] = items[0].text
        self.window.waitlist.remove(items[0].text)
        
    def whichgrid(self, x, y):
        size = int(self.size().width()/3)
        row = y//size
        col = x//size
        return row, col

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tagw = 180 * math.sqrt(app.desktop().width() / 3840)
    tagh = 50 * math.sqrt(app.desktop().height() / 2160)
    win = Mainwindow()
    win.show()
    sys.exit(app.exec_())