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
        self.rlist.setObjectName('pintu')
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

        #将图片加入工作列表
        for item in os.listdir('wait-to-merge'):
            if is_img(os.path.splitext(item)[1]):
                pic = QPixmap('wait-to-merge/'+item)
                pitem = QListWidgetItem(QtGui.QIcon(pic.scaled(QtCore.QSize(120,120))), item)
                pitem.setSizeHint(QtCore.QSize(100,100))
                self.plist.addItem(pitem)
                self.waitlist.append(item)
                # self.rlist.addItem(pitem)
        

    def merge(self):   
        rows = 0#有图的行数
        cols = None #暂存上一行的图数量 列数
        
        for i in range(len(self.worklist)):
            if self.worklist[i].count(None) != 3:
                rows+=1
                if not cols:
                    cols = 3-self.worklist[i].count(None)
                else:
                    if 3-self.worklist[i].count(None)!= cols:
                        QMessageBox.about(self,"提示","图片数量不符合要求")
                        return
        
        if rows == 0:
            QMessageBox.about(self,"提示","无图片")
            return
            
                        
        img = Image.open('wait-to-merge/'+self.worklist[0][0],'r')
        format_ = img.format
        width = img.size[0]
        height = img.size[1]

        IMAGES_PATH = 'wait-to-merge\\'
        IMAGE_SAVE_PATH = 'results\\'
        to_image = Image.new('RGB', (cols * width, rows * height))  # 创建一个新图
        # 循环遍历，把每张图片按顺序粘贴到对应位置上
        for x in range(rows):
            for y in range(cols):
                from_image = Image.open(IMAGES_PATH + self.worklist[x][y]).resize(
                    (width, height), Image.ANTIALIAS)
                to_image.paste(from_image, (y * width, x * height))
        
        fileno = len(os.listdir('results'))
        to_image.save(IMAGE_SAVE_PATH + str(fileno) + '.' + format_)  # 保存新图
        print('新图片生成')
        
        self.worklist = [[None,None,None],
                         [None,None,None],
                         [None,None,None]] 
        
        self.rlist.clearContents()
        
class rlist(QTableWidget):
    def __init__(self,parent=None):
        super().__init__(parent) 
        self.window = parent
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setRowCount(3)#设置表格的行数
        self.setColumnCount(3)#设置表格的列数
        
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)#单元格不能被修改

        self.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
       
    def dragEnterEvent(self, event):
        # event.setDropAction(Qt.MoveAction)
        # 接受事件 将事件转到dropevent
        event.accept()
    
    def mouseDoubleClickEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        row,col = self.whichgrid(x, y)
        
        icon = self.window.worklist[row][col]
        self.window.waitlist.insert(0, icon)
        
        pic = QPixmap('wait-to-merge/'+icon)
        pitem = QListWidgetItem(QtGui.QIcon(pic.scaled(QtCore.QSize(120,120))), icon)
        pitem.setSizeHint(QtCore.QSize(100,100))
        self.window.plist.insertItem(0, pitem)
        
        
        empty = QTableWidgetItem('')
        
        self.setItem(row, col, empty)
        
    def dropEvent(self, event):
        source_Widget=event.source()#获取拖入元素的父组件
        items=source_Widget.selectedItems()
        item = items[0]
        icon = item.icon()
        
        #源格子位置
        if source_Widget.objectName() == 'pintu':
            srow = source_Widget.row(source_Widget.selectedItems()[0])
            scol = source_Widget.column(source_Widget.selectedItems()[0])
        
        x = event.pos().x()
        y = event.pos().y()
        
        size = int(self.size().width()/3)
        self.setIconSize(QSize(size, size))
        row,col = self.whichgrid(x, y)
        print(row, col)
        
        newItem = QTableWidgetItem(icon,'')
        self.setItem(row, col, newItem)
        self.window.worklist[row][col] = item.text()
        
        if source_Widget.objectName() == 'yuantu':
            self.window.waitlist.remove(item.text())
            source_Widget.takeItem(source_Widget.currentRow())
        elif source_Widget.objectName() == 'pintu':
            sitem = QTableWidgetItem(self.itemAt(srow, scol).icon(),'')
            titem = QTableWidgetItem(self.itemAt(row, col).icon(),'')
            self.setItem(row, col, sitem)
            self.setItem(srow, scol, titem)
            
        return 
        
        
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
    
    #TODO:设置撤销缓存区 右端图片可换位