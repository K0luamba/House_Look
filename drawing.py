import sys
import random as r
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QColorDialog, QAction, QSlider, QLabel, QComboBox, QCheckBox
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QFont, QIcon, QPolygonF
from PyQt5.QtCore import Qt, QSize, QPointF

sldStyle = """
            QSlider::groove:horizontal {  
                height: 10px;
                margin: 0px;
                border-radius: 5px;
                background: #B0AEB1;
            }
            QSlider::handle:horizontal {
                background: #fff;
                border: 1px solid #3B99FC;
                width: 20px;
                margin: -5px 0; 
                border-radius: 9px;
            }
            QSlider::sub-page:qlineargradient {
                background: #3B99FC;
                border-radius: 5px;
            }
        """

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):      
        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Drawing home')
        self.width = 175 #default settings
        self.height = 100
        self.roofHeight = 50
        self.mainColor1 = QColor(255, 255, 127)
        self.mainColor2 = QColor(255, 85, 0)
        self.roofColor = QColor(199, 250, 252)
        self.doorColor = QColor(255, 255, 255)
        self.lightColor = QColor(255, 219, 41)
        self.windowStyle = "Round window"
        self.roomNumber = 1
        
        drawButton = QPushButton("Move cursor here to update the object, if it was not happened", self)
        drawButton.setFont(QFont("Comic Sans MS", 11, QFont.Normal))
        drawButton.move(40,60)
        drawButton.adjustSize()
        #sliders etc.
        self.changeWidth = QSlider(Qt.Horizontal, self)
        self.changeWidth.setFocusPolicy(Qt.NoFocus)
        self.changeWidth.setStyleSheet(sldStyle) #use our own style!
        self.changeWidth.setGeometry(30, 150, 100, 30)
        self.changeWidth.valueChanged[int].connect(self.changeWidthF)
        self.changeHeight = QSlider(Qt.Horizontal, self)
        self.changeHeight.setFocusPolicy(Qt.NoFocus)
        self.changeHeight.setStyleSheet(sldStyle)
        self.changeHeight.setGeometry(30, 220, 100, 30)
        self.changeHeight.valueChanged[int].connect(self.changeHeightF)
        self.changeRoofHeight = QSlider(Qt.Horizontal, self)
        self.changeRoofHeight.setFocusPolicy(Qt.NoFocus)
        self.changeRoofHeight.setStyleSheet(sldStyle)
        self.changeRoofHeight.setGeometry(30, 290, 100, 30)
        self.changeRoofHeight.valueChanged[int].connect(self.changeRoofHeightF)
        changeWindowStyle = QComboBox(self)
        changeWindowStyle.addItem("Round window")
        changeWindowStyle.addItem("2-part window")
        changeWindowStyle.addItem("No window")
        changeWindowStyle.move(30, 365)
        changeWindowStyle.setFont(QFont("Tahoma", 10, QFont.Normal))
        changeWindowStyle.activated[str].connect(self.changeWindowStyle)
        changeWindowStyle.adjustSize()
        changeIllumination = QCheckBox('Neon Light', self)
        changeIllumination.move(30, 410)
        changeIllumination.setFont(QFont("Segoe Print", 10, QFont.Normal))
        changeIllumination.adjustSize()
        changeIllumination.stateChanged.connect(self.changeIllumination)
        changeRoomNumber = QComboBox(self)
        changeRoomNumber.addItem("1")
        changeRoomNumber.addItem("2")
        changeRoomNumber.move(30, 505)
        changeRoomNumber.setFont(QFont("Tahoma", 10, QFont.Normal))
        changeRoomNumber.activated[int].connect(self.changeRoomNumber)
        #labels
        changeW = QLabel("Width", self)
        changeW.move(30, 120)
        changeW.setFont(QFont("Segoe Print", 10, QFont.Normal))
        changeH = QLabel("Height", self)
        changeH.move(30, 190)
        changeH.setFont(QFont("Segoe Print", 10, QFont.Normal))
        changeRH = QLabel("Roof level", self)
        changeRH.move(30, 260)
        changeRH.setFont(QFont("Segoe Print", 10, QFont.Normal))
        changeWS = QLabel("Window style", self)
        changeWS.move(30, 330)
        changeWS.setFont(QFont("Segoe Print", 10, QFont.Normal))
        changeWS.adjustSize()
        changeRN = QLabel("Number of rooms", self)
        changeRN.move(30, 450)
        changeRN.setFont(QFont("Segoe Print", 10, QFont.Normal))
        changeRN.adjustSize()
        changeRN1 = QLabel("on the 2nd floor", self)
        changeRN1.move(30, 470)
        changeRN1.setFont(QFont("Segoe Print", 10, QFont.Normal))
        changeRN1.adjustSize()
        #toolbar actions
        roofColorAction = QAction(QIcon('colorR.png'), 'Change color of the roof', self)
        roofColorAction.triggered.connect(self.changeRoofColor)
        color1Action = QAction(QIcon('color2.png'), 'Change color of the upper part', self)
        color1Action.triggered.connect(self.changeColor1)
        color2Action = QAction(QIcon('color1.png'), 'Change color of the lower part', self)
        color2Action.triggered.connect(self.changeColor2)
        doorColorAction = QAction(QIcon('colorD.png'), 'Change color of the door', self)
        doorColorAction.triggered.connect(self.changeDoorColor)
        randomizeAction = QAction(QIcon('random.png'), 'Randonize your house', self)
        randomizeAction.triggered.connect(self.randomize)
        toolbar = self.addToolBar('Menu')
        toolbar.setIconSize(QSize(45, 45))
        toolbar.addAction(roofColorAction)
        toolbar.addAction(color2Action)
        toolbar.addAction(color1Action)
        toolbar.addAction(doorColorAction)
        toolbar.addAction(randomizeAction)
        
        self.show()

    def paintEvent(self, e): 
        #print("paint")
        self.qp = QPainter(self)
        
        #self.qp.setPen(QColor(245, 245, 245)) #if you need no black circuit
        triangle = QPolygonF( [QPointF(200,200),
                               QPointF(200 + self.width, 200), 
                               QPointF(200 + self.width/2, 200 - self.roofHeight)] )
        self.qp.setBrush(QBrush(self.roofColor, Qt.SolidPattern))
        self.qp.drawPolygon(triangle) #roof
        self.qp.setBrush(QBrush(self.mainColor1, Qt.SolidPattern))
        self.qp.drawRect(200, 200, self.width, self.height) #upper part
        self.qp.setBrush(QBrush(self.mainColor2, Qt.SolidPattern))
        self.qp.drawRect(200, 200 + self.height, self.width, self.height) #lower part
        #details
        self.qp.setBrush(QBrush(self.doorColor, Qt.SolidPattern))
        self.qp.drawRect(130 + self.width, 115 + 2*self.height, 50, 80) #calculate door       
        self.qp.setBrush(QBrush(self.lightColor, Qt.SolidPattern))
        self.qp.drawRect(140 + self.width, 125 + 2*self.height, 30, 40) #window on the door
        self.qp.setBrush(QBrush(QColor(173, 98, 23), Qt.SolidPattern))
        self.qp.drawEllipse(173 + self.width, 160 + 2*self.height, 4, 4) #door handle
        #variants of the window on the third floor
        self.qp.setBrush(QBrush(self.lightColor, Qt.SolidPattern))
        if self.windowStyle == "Round window":
            diameter = 30 * (self.roofHeight/50) #calculate proportion
            if diameter > 45:
                diameter = 45 #limit for normal design
            self.qp.drawEllipse(200 - diameter/2 + self.width/2, 200 - diameter/2 - self.roofHeight*0.45, diameter, diameter)
            self.qp.setPen(QPen(QColor(173, 98, 23), 3, Qt.SolidLine)) #window planks
            self.qp.drawLine(202 - diameter/2 + self.width/2, 200 - self.roofHeight*0.45, 198 + diameter/2 + self.width/2, 200 - self.roofHeight*0.45)
            self.qp.drawLine(200 + self.width/2, 198 + diameter/2 - self.roofHeight*0.45, 200 + self.width/2, 202 - diameter/2 - self.roofHeight*0.45)
        if self.windowStyle == "2-part window":
            left = QPolygonF( [QPointF(200 + self.width/3, 195),
                               QPointF(197 + self.width/2, 195),
                               QPointF(197 + self.width/2, 210 - self.roofHeight/1.04),
                               QPointF(200 + self.width/3, 210 - self.roofHeight/1.5)] )
            self.qp.drawPolygon(left)
            right =  QPolygonF( [QPointF(200 + self.width*2/3, 195),
                                 QPointF(203 + self.width/2, 195),
                                 QPointF(203 + self.width/2, 210 - self.roofHeight/1.04),
                                 QPointF(200 + self.width*2/3, 210 - self.roofHeight/1.5)] )
            self.qp.drawPolygon(right)
        #window on the first floor
        self.qp.setPen(QPen(Qt.black, 1, Qt.SolidLine)) 
        self.qp.drawRect(210 + 2/5*(self.width - 175), 110 + 2*self.height - 1/5*(self.height - 100), 75 + 2/5*(self.width - 175), 65 + 1/5*(self.height - 100))
        xc = 210 + 2/5*(self.width - 175) + (75 + 2/5*(self.width - 175))/2
        yc = 110 + 2*self.height - 1/5*(self.height - 100) + (65 + 1/5*(self.height - 100))/2
        xr = 208 + 2/5*(self.width - 175) + 75 + 2/5*(self.width - 175)
        yd = 108 + 2*self.height - 1/5*(self.height - 100) + 65 + 1/5*(self.height - 100)
        self.qp.setPen(QPen(QColor(173, 98, 23), 3, Qt.SolidLine))
        self.qp.drawLine(212 + 2/5*(self.width - 175), yc, xr, yc)
        self.qp.drawLine(xc, 112 + 2*self.height - 1/5*(self.height - 100), xc, yd)
        #windows on the second floor
        self.qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        yc = 110 + self.height - 1/5*(self.height - 100)
        yd = 65 + 1/5*(self.height - 100) #use our previous variables to make arguments shorter
        if self.roomNumber == 1:
            self.qp.drawRect(200 + self.width*0.2, yc, self.width*0.6, yd)
            self.qp.setPen(QPen(QColor(173, 98, 23), 3, Qt.SolidLine))
            self.qp.drawLine(200 + self.width*0.4, yc + 2, 200 + self.width*0.4, yc + yd - 2)
            self.qp.drawLine(200 + self.width*0.6, yc + 2, 200 + self.width*0.6, yc + yd - 2)
        if self.roomNumber == 2:
            self.qp.drawRect(200 + self.width*0.1, yc, self.width*0.35, yd)
            self.qp.drawRect(200 + self.width*0.55, yc, self.width*0.35, yd)
            self.qp.setPen(QPen(QColor(173, 98, 23), 3, Qt.SolidLine))
            self.qp.drawLine(200 + self.width*0.275, yc + 2, 200 + self.width*0.275, yc + yd - 2)
            self.qp.drawLine(200 + self.width*0.725, yc + 2, 200 + self.width*0.725, yc + yd - 2)
        
        self.qp.end()
        self.update() #need to draw again our image

    def changeRoofColor(self):
        roofColor = QColorDialog.getColor()
        if roofColor.isValid():
            self.roofColor = roofColor

    def changeColor1(self):
        mainColor1 = QColorDialog.getColor()
        if mainColor1.isValid():
            self.mainColor1 = mainColor1

    def changeColor2(self):
        mainColor2 = QColorDialog.getColor()
        if mainColor2.isValid():
            self.mainColor2 = mainColor2

    def changeDoorColor(self):
        doorColor = QColorDialog.getColor()
        if doorColor.isValid():
            self.doorColor = doorColor

    def changeWidthF(self, value):
        #print("changed to " + str(value + 150))
        self.width = value + 175

    def changeHeightF(self, value):
        self.height = value/2 + 100 #keep in mind max and min value of each characteristic

    def changeRoofHeightF(self,value):
        self.roofHeight = value/2 + 50

    def changeWindowStyle(self, text):
        self.windowStyle = text

    def changeIllumination(self, state):
        if state == Qt.Checked:
            self.lightColor = QColor(229, 101, 157) #purple
        else:
            self.lightColor = QColor(255, 219, 41) #orange

    def changeRoomNumber(self, text):
        self.roomNumber = int(text) + 1

    def randomize(self):
        self.width = r.randint(175, 275)
        self.changeWidth.setValue(self.width - 175)
        self.height = r.randint(100, 150)
        self.changeHeight.setValue(self.height - 100)
        self.roofHeight = r.randint(50, 100)
        self.changeRoofHeight.setValue(self.roofHeight - 50)
        self.mainColor1 = QColor(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
        self.mainColor2 = QColor(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
        self.roofColor = QColor(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
        self.doorColor = QColor(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))

app = QApplication(sys.argv)
ex = Example()
sys.exit(app.exec_())
