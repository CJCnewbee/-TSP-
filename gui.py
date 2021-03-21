import sys
import math
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
from PyQt5 import QtWidgets,QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import MyFuncTool as mft
import GAAA
import GAinAnt
import time
def f(x):
    if x==0:
        return 1
    else:
        return math.sin(x)/x
class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = plt.figure()
        #画布分成一行一列在第一块
        self.axes1 = self.figure.add_subplot(121)
        self.axes2 = self.figure.add_subplot(122)
        self.canvas = FigureCanvas(self.figure)

        self.answer = QtWidgets.QLabel('')
        font = QtGui.QFont()
        # 字体
        font.setFamily('微软雅黑')
        # 大小
        font.setPointSize(15)
        font.setWeight(50)
        self.answer.setFont(font)
        #参数输入
        self.file= QtWidgets.QLabel('路径:')
        self.fileqle = QtWidgets.QLineEdit('./data/oliver30.tsp')

        self.Alpha = QtWidgets.QLabel('α:')
        self.Alphaqle = QtWidgets.QLineEdit('1.5')

        self.Beta = QtWidgets.QLabel('β:')
        self.Betaqle = QtWidgets.QLineEdit('2.5')

        self.Rho = QtWidgets.QLabel('ρ:')
        self.Rhoqle = QtWidgets.QLineEdit('0.2')

        self.Q = QtWidgets.QLabel('Q:')
        self.Qqle = QtWidgets.QLineEdit('100')

        self.Pc = QtWidgets.QLabel('Pc:')
        self.Pcqle = QtWidgets.QLineEdit('0.6')

        self.Pm = QtWidgets.QLabel('Pm:')
        self.Pmqle = QtWidgets.QLineEdit('0.08')

        self.Ncmax = QtWidgets.QLabel('NCmax:')
        self.Ncmaxqle = QtWidgets.QLineEdit('50')

        self.Ngmax = QtWidgets.QLabel('NGmax:')
        self.Ngmaxqle = QtWidgets.QLineEdit('50')
        #按钮设置
        self.buttonAlgori1 = QtWidgets.QPushButton('优化算法一')
        self.buttonAlgori1.clicked.connect(self.Algori1)

        self.buttonAlgori2 = QtWidgets.QPushButton('优化算法二')
        self.buttonAlgori2.clicked.connect(self.Algori2)

        #设置布局
        layoutqle = QtWidgets.QHBoxLayout()
        layoutqle.addWidget(self.file)
        layoutqle.addWidget(self.fileqle)
        Loq = QtWidgets.QWidget(self)
        Loq.setLayout(layoutqle)

        layoutqle1 = QtWidgets.QHBoxLayout()
        layoutqle1.addWidget(self.Alpha)
        layoutqle1.addWidget(self.Alphaqle)
        Loq1 = QtWidgets.QWidget(self)
        Loq1.setLayout(layoutqle1)

        layoutqle2 = QtWidgets.QHBoxLayout()
        layoutqle2.addWidget(self.Beta)
        layoutqle2.addWidget(self.Betaqle)
        Loq2 = QtWidgets.QWidget(self)
        Loq2.setLayout(layoutqle2)

        layoutqle3 = QtWidgets.QHBoxLayout()
        layoutqle3.addWidget(self.Rho)
        layoutqle3.addWidget(self.Rhoqle)
        Loq3 = QtWidgets.QWidget(self)
        Loq3.setLayout(layoutqle3)

        layoutqle4 = QtWidgets.QHBoxLayout()
        layoutqle4.addWidget(self.Q)
        layoutqle4.addWidget(self.Qqle)
        Loq4 = QtWidgets.QWidget(self)
        Loq4.setLayout(layoutqle4)

        layoutqle5 = QtWidgets.QHBoxLayout()
        layoutqle5.addWidget(self.Pc)
        layoutqle5.addWidget(self.Pcqle)
        Loq5 = QtWidgets.QWidget(self)
        Loq5.setLayout(layoutqle5)

        layoutqle6 = QtWidgets.QHBoxLayout()
        layoutqle6.addWidget(self.Pm)
        layoutqle6.addWidget(self.Pmqle)
        Loq6 = QtWidgets.QWidget(self)
        Loq6.setLayout(layoutqle6)

        layoutqle7 = QtWidgets.QHBoxLayout()
        layoutqle7.addWidget(self.Ncmax)
        layoutqle7.addWidget(self.Ncmaxqle)
        Loq7 = QtWidgets.QWidget(self)
        Loq7.setLayout(layoutqle7)

        layoutqle8 = QtWidgets.QHBoxLayout()
        layoutqle8.addWidget(self.Ngmax)
        layoutqle8.addWidget(self.Ngmaxqle)
        Loq8 = QtWidgets.QWidget(self)
        Loq8.setLayout(layoutqle8)

        #图像列
        layoutFigure=QtWidgets.QVBoxLayout()
        #layoutFigure.addWidget(self.toolbar)

        layoutFigure.addWidget(self.canvas)
        layoutFigure.addWidget(self.answer)
        #layoutFigure.setStretchFactor(self.toolbar, 1)
        layoutFigure.setStretchFactor(self.answer, 1)
        layoutFigure.setStretchFactor(self.canvas, 4)

        # 列布局
        layoutColumn= QtWidgets.QVBoxLayout()
        #拉伸
        layoutColumn.addStretch(1)
        layoutColumn.addWidget(Loq)
        layoutColumn.addStretch(1)
        layoutColumn.addWidget(Loq1)
        layoutColumn.addStretch(1)
        layoutColumn.addWidget(Loq2)
        layoutColumn.addStretch(1)
        layoutColumn.addWidget(Loq3)
        layoutColumn.addStretch(1)
        layoutColumn.addWidget(Loq4)
        layoutColumn.addStretch(1)
        layoutColumn.addWidget(Loq5)
        layoutColumn.addStretch(1)
        layoutColumn.addWidget(Loq6)
        layoutColumn.addStretch(1)
        layoutColumn.addWidget(Loq7)
        layoutColumn.addStretch(1)
        layoutColumn.addWidget(Loq8)
        layoutColumn.addStretch(1)
        layoutColumn.addWidget(self.buttonAlgori1)
        layoutColumn.addStretch(1)
        layoutColumn.addWidget(self.buttonAlgori2)
        layoutColumn.addStretch(1)
        # 总布局
        layout = QtWidgets.QHBoxLayout()
        LoF= QtWidgets.QWidget(self)
        LoF.setLayout(layoutFigure)
        layout.addWidget(LoF)
        LoB = QtWidgets.QWidget(self)
        LoB.setLayout(layoutColumn)
        layout.addWidget(LoB)
        layout.setStretchFactor(LoB,1)
        layout.setStretchFactor(LoF,4)
        #self.toolbar.hide()
        self.setLayout(layout)

    def Algori1(self):
        self.axes1.cla()
        self.axes2.cla()
        datafile=self.fileqle.text()
        Position, CityNum, Dist = GAAA.GetData(datafile)
        start = GAAA.time.clock() # 程序计时开始
        tsp = GAAA.TSP(Position, Dist, CityNum, float(self.Alphaqle.text()), float(self.Betaqle.text()), float(self.Rhoqle.text()), float(self.Qqle.text()), float(self.Pcqle.text()),float(self.Pmqle.text()), 100)
        generate_ant = float(self.Ncmaxqle.text())
        generate_ga = float(self.Ngmaxqle.text())
        Min_Path, BestPath, distance_list = tsp.run(generate_ant, generate_ga)
        end = GAAA.time.clock()  # 程序计时结束
        time = end - start  # 运行时间
        #print(time)
        # 结果打印
        BestPath.append(BestPath[0])
        Str="time:"
        Str+=str(time)
        Str+='\n'
        Str+=GAAA.ResultShow(Min_Path, BestPath, CityNum, "遗传-蚁群算法")
        self.answer.adjustSize()
        self.answer.setWordWrap(True)
        self.answer.setText(Str)

        BestPath, Position=BestPath,Position
        self.axes1.plot(Position[:, 0], Position[:, 1], 'bo')
        for i, city in enumerate(Position):
            self.axes1.text(city[0], city[1], str(i))
        self.axes1.plot(Position[BestPath, 0], Position[BestPath, 1], color='red')
        self.axes2.plot(range(len(distance_list)), distance_list, 'red')
        self.canvas.draw()
    def Algori2(self):
        self.axes1.cla()
        self.axes2.cla()
        datafile = self.fileqle.text()
        Position, CityNum, Dist = GAinAnt.GetData(datafile)
        start = GAinAnt.time.clock()  # 程序计时开始
        tsp = GAinAnt.TSP(Position, Dist, CityNum, float(self.Alphaqle.text()), float(self.Betaqle.text()),
                       float(self.Rhoqle.text()), float(self.Qqle.text()), float(self.Pcqle.text()),
                       float(self.Pmqle.text()))
        generate_ant = float(self.Ncmaxqle.text())
        Min_Path, BestPath, distance_list = tsp.run(generate_ant)
        end = GAinAnt.time.clock()  # 程序计时结束
        time = end - start  # 运行时间
        #print(time)
        # 结果打印
        BestPath.append(BestPath[0])
        Str = "time:"
        Str += str(time)
        Str += '\n'
        Str += GAinAnt.ResultShow(Min_Path, BestPath, CityNum, "融合蚁群算法")
        self.answer.adjustSize()
        self.answer.setWordWrap(True)
        self.answer.setText(Str)
        BestPath, Position = BestPath, Position
        self.axes1.plot(Position[:, 0], Position[:, 1], 'bo')
        for i, city in enumerate(Position):
            self.axes1.text(city[0], city[1], str(i))
        self.axes1.plot(Position[BestPath, 0], Position[BestPath, 1], color='red')
        self.axes2.plot(range(len(distance_list)), distance_list, 'red')
        self.canvas.draw()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    main = Window()
    main.setWindowTitle('毕业设计')
    main.setFixedSize(1440,900)
    main.show()
    sys.exit(app.exec_())