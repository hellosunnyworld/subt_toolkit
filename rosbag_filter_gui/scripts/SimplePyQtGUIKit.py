#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import Qt, QBasicTimer
class SimplePyQtGUIKit(QMainWindow):
    def __init__(self):
        super().__init__()
    def QuitApp(self):
        QApplication.quit()

    @classmethod
    def GetFilePath(self,caption="Open File",filefilter="",isApp=False):
        u"""
            "Images (*.png *.xpm *.jpg);;Text files (*.txt);;XML files (*.xml)"
        """

        if not isApp:
          app = QApplication(sys.argv)
        files=QFileDialog.getOpenFileNames(caption=caption,filter=filefilter)

        strlist=[]
        for file in files:
            strlist.append(str(file))

        return strlist


    @classmethod
    def GetCheckButtonSelect(self, selectList, title="Select", msg="",app=None):
        """
        Get selected check button options

        title: Window name
        mag: Label of the check button
        return selected dictionary
            {'sample b': False, 'sample c': False, 'sample a': False}
        """
 
        if app is None:
          app = QApplication(sys.argv)
          
        scroll = QScrollArea() 
        mainWin = QWidget()
        mainLayout = QVBoxLayout()
        
        win = QWidget()
        layout=QVBoxLayout(win)
        layoutIndex=0

        if msg != "":
            label = QLabel(msg)
            layout.addWidget(label)
            layoutIndex=layoutIndex+1

        checkboxs=[]
        for select in selectList:
            checkbox=QCheckBox(select)
            layout.addWidget(checkbox)
            layoutIndex=layoutIndex+1
            checkboxs.append(checkbox)

        btn=QPushButton("OK")
        btn.clicked.connect(app.quit)

        win.setLayout(layout)

        #Scroll Area Properties
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(win)
        
        
        mainLayout.addWidget(scroll)
        mainLayout.addWidget(btn)
        layoutIndex=layoutIndex+1
        mainWin.setLayout(mainLayout)
        mainWin.setWindowTitle(title)
        mainWin.show()
	
        app.exec_()

        result=[]
        for (checkbox, select) in zip(checkboxs, selectList):
            if checkbox.isChecked():
                result.append(select)
        print('Having chosen the following topics:')
        for topic in result:
            print(topic)
        return result

# currently not used
class ProgressBar(QWidget):
    def __init__(self, bagInd, max, app = None):
        QWidget.__init__(self)
        if app is None:
            app = QApplication(sys.argv) 
        self.setGeometry(300, 300, 700, 250)
        self.setWindowTitle('Progress of filtering Bag '+str(bagInd))
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(60, 80, 600, 50)
        
        self.button = QPushButton('Cancel', self)
        self.button.setFocusPolicy(Qt.NoFocus)
        self.button.move(60, 150)   
        self.button.clicked.connect(self.close)

        self.timer = QBasicTimer()
        self.step = 0
        self.max = max
        self.timer.start(100,self)

        self.show()
        app.exec_()
    def timerEvent(self, event):
        if self.step >= self.max:
            self.timer.stop()
            self.close()
            return
        #self.step = self.step + 1
        self.pbar.setValue(self.step)
        
    def onStart(self):
        if self.timer.isActive(): 
            self.timer.stop()
            self.button.setText('Start')
        else:
            self.timer.start(100, self)
            self.button.setText('Stop')

if __name__ == '__main__':
    #  print "GetCheckButtonSelect"
    #  optList=SimplePyQtGUIKit.GetCheckButtonSelect(["sample a","sample b","sample c"], title="Select sample", msg="Please select sample")
    #  print optList
    # filePath=SimplePyQtGUIKit.GetFilePath(caption=u"Select files",filefilter="*py")
    # print(filePath)

    # import sys
    # app = QApplication(sys.argv)
    # qb = ProgressBar(5,100,app)
    # sys.exit()
    from tqdm import tqdm
    from time import sleep
    #LENGTH = 10 # Number of iterations required to fill pbar
    a = range(0,20000,100)
    pbar = tqdm(total=20000) # Init pbar
    for i in a:
        pbar.update(n=1) # Increments counter


