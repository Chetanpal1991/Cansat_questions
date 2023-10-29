import sys
import pandas as pd
import pyqtgraph as pg
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                                QVBoxLayout, QLabel, QScrollArea)
from PyQt6.QtCore import QTimer,Qt
from PyQt6.QtGui import QIcon,QPixmap,QPainter,QPalette,QBrush



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Telemetry analysis software")
        self.resize(1525,775)

        logo_image = QPixmap("GUI for kalpana software\Add Ons\Team Kalpana Logo.png").scaledToWidth(120, Qt.TransformationMode.SmoothTransformation)
        logo_label = QLabel(self)
        logo_label.setPixmap(logo_image)
        logo_label.setGeometry(20, 20, logo_image.width(), logo_image.height())


       
        background_image = QPixmap("GUI for kalpana software\Add Ons\Team Kalpana Logo background1.png")
        central_widget = QLabel(self)
        central_widget.setPixmap(background_image)
        central_widget.setGeometry(0, 0, background_image.width(), background_image.height())
        self.setCentralWidget(central_widget)

        
        painter = QPainter(logo_image)
        painter.drawText(0, 0, logo_image.width(), logo_image.height(), Qt.AlignmentFlag.AlignCenter, "My App")
        painter.end()

        
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(background_image))
        self.setPalette(palette)

        self.label1 = QLabel("MISSION TIME", self)
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label1.setGeometry(125,220,250,100)                 #75,300,350,250
        self.label1.setStyleSheet("font-size: 35px; font-weight: bold; font-family: Berlin Sans FB;")

        self.label4 = QLabel("RAW TELEMETRY DATA FROM CSV FILE", self)
        self.label4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label4.setGeometry(735,0,300,100)
        self.label4.setStyleSheet("font-size: 15px; font-weight: bold;font-family: Berlin Sans FB;")

        self.label5 = QLabel("TEMPERATURE", self)
        self.label5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label5.setGeometry(625,180,150,100)
        self.label5.setStyleSheet("font-size: 15px; font-weight: bold;font-family: Berlin Sans FB;")

        self.label6 = QLabel("VOLTAGE", self)
        self.label6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label6.setGeometry(623,500,150,100)        
        self.label6.setStyleSheet("font-size: 15px; font-weight: bold;font-family: Berlin Sans FB;")

        self.label7 = QLabel("ALTITUDE", self)
        self.label7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label7.setGeometry(623,350,150,100)
        self.label7.setStyleSheet("font-size: 15px; font-weight: bold;font-family: Berlin Sans FB;")

        self.label8 = QLabel("TEAM KALPANA", self)
        self.label8.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label8.setGeometry(150,48,155,25)
        self.label8.setStyleSheet("font-family: Algerian; font-size: 20px; font-weight: bold; font-style: italic; text-decoration: underline;")

        self.label9 = QLabel("TEAM ID: #abc", self)
        self.label9.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label9.setGeometry(150,75,150,50)
        self.label9.setStyleSheet("font-size: 15px; font-weight: bold;")

        self.label11 = QLabel("", self)
        self.label11.setGeometry(850,200,650,545)
        self.label11.setStyleSheet("background-color: black")



        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        

        self.altitude_graph = MainWindow1(self)
        self.telemetry_data = MainWindow2(self)
        self.temperature_graph = MainWindow3(self)
        self.voltage_graph = MainWindow4(self)
        self.mission_time = mission_time(self)
        self.temperature = temperature(self)      
        self.voltage = voltage(self)              
        self.altitude = altitude(self)

        
        self.altitude_graph.setParent(self.centralWidget())
        self.telemetry_data.setParent(self.centralWidget())
        self.temperature_graph.setParent(self.centralWidget())
        self.voltage_graph.setParent(self.centralWidget())
        self.mission_time.setParent(self.centralWidget())
        self.temperature.setParent(self.centralWidget())             
        self.voltage.setParent(self.centralWidget())                 
        self.altitude.setParent(self.centralWidget())
        
        
        # Set the geometry of the sub windows
        self.telemetry_data.setGeometry(400, 65, 1000, 100)  
        self.temperature_graph.setGeometry(850, 200, 650, 150)         #temperature
        self.voltage_graph.setGeometry(850, 500, 650, 200)             #voltage                               
        self.altitude_graph.setGeometry(850, 350, 650, 150)            #altitude          
        self.mission_time.setGeometry(75,300,350,250)
        self.temperature.setGeometry(600,250,200,70)
        self.voltage.setGeometry(600,570,200,70)            
        self.altitude.setGeometry(600,420,200,70)

class MainWindow1(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()

        # Create a central widget and a layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', 'Altitude')
        self.plot_widget.setLabel('bottom', 'Time')
        layout.addWidget(self.plot_widget)

        # Read data from the Excel file
        self.df = pd.read_excel("GUI for kalpana software\Add Ons\Sample Data - Software Task.xlsx",usecols=['ALTITUDE'])


        # Initialize the data and time index
        self.time_index = 0
        self.data_index = 0

        # Create a timer that updates the plot every second
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1 data packet per second
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.plot_widget.setLimits(xMin=-1)

    def update_plot(self):
        # Check if all data has been displayed
        if self.data_index >= len(self.df):
            self.timer.stop()
            return

        # Get the next data packet and increment the data index
        

        # Extract the data for plotting
        x_data = range(self.data_index + 1)
        y_data = self.df['ALTITUDE'][:self.data_index+1]
        self.plot_widget.plot(x_data, y_data, clear=True)

        # Increment the time index
        self.data_index += 1
        self.time_index += 1


class MainWindow2(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()

        # Set up the widget and layout
        self.widget = QWidget()
        
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setStyleSheet(''' 
            border: 2px solid black; ''')

        # Read the Excel file using pandas
        self.data = pd.read_excel("GUI for kalpana software\Add Ons\Sample Data - Software Task.xlsx")

        # Initialize the row index and label
        self.row = 0
        self.rows = []
        headers = self.data.columns.values.tolist()
        headers_connected1 = "\t".join([headers[0],headers[1]])
        headers_connected2 = "\t        ".join([headers_connected1,headers[2]])
        headers_connected3 = "\t     ".join([headers_connected2,headers[3]])
        headers_connected4 = "\t            ".join([headers_connected3,headers[4]])
        headers_connected5 = "\t           ".join([headers_connected4,headers[5]])
        headers_connected6 = "\t        ".join([headers_connected5,headers[6]])
        headers_connected7 = "\t            ".join([headers_connected6,headers[7]])
        headers_connected8 = "\t       ".join([headers_connected7,headers[8]])
        self.rows.append(headers_connected8)
        

        self.label = QLabel()
        self.label.setWordWrap(True)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.label)
        self.layout.addWidget(self.scrollArea)

        # Set up the timer to display the rows
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayRow)
        self.timer.start(1000)  # 1 second interval
        
        

    def displayRow(self):
        # Get the row data and append it to the list
        
        if self.row < len(self.data):
            row_data = self.data.iloc[self.row]
            row_text =  "\t                   ".join([row_data[0],str(row_data[1])])
            row_text1 = "\t                    ".join([row_text,str(row_data[2])])
            row_text2 = "\t                            ".join([row_text1,str(row_data[3])])
            row_text3 = "\t                ".join([row_text2,str(row_data[4])])
            row_text4 = "\t                          ".join([row_text3,str(row_data[5])])
            row_text5 = "\t                         ".join([row_text4,str(row_data[6])])
            row_text6 = "\t              ".join([row_text5,str(row_data[7])])
            row_text7 = "\t            ".join([row_text6,str(row_data[8])])
            self.rows.append(row_text7)
            label = QLabel(row_text)
            label.setWordWrap(True)  
            
            
            self.row += 1
        else:
            self.timer.stop()

        # Update the label with all rows in the list
        
        self.label.setText("\n".join(self.rows))
        scroll_bar = self.scrollArea.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())


class MainWindow3(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

       
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', 'Temperature')
        self.plot_widget.setLabel('bottom', 'Time')
        layout.addWidget(self.plot_widget)


        self.df = pd.read_excel("GUI for kalpana software\Add Ons\Sample Data - Software Task.xlsx",usecols=['TEMP'])


 
        self.time_index = 0
        self.data_index = 0


        self.timer = QTimer()
        self.timer.setInterval(1000)  
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.plot_widget.setLimits(xMin=-1)

    def update_plot(self):
        
        if self.data_index >= len(self.df):
            self.timer.stop()
            return

      
        x_data = range(self.data_index + 1)
        y_data = self.df['TEMP'][:self.data_index+1]
        self.plot_widget.plot(x_data, y_data, clear=True)

        self.data_index += 1
        self.time_index += 1


class MainWindow4(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

       
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', 'Voltage')
        self.plot_widget.setLabel('bottom', 'Time')
        layout.addWidget(self.plot_widget)


        self.df = pd.read_excel("GUI for kalpana software\Add Ons\Sample Data - Software Task.xlsx",usecols=['VOLTAGE'])


 
        self.time_index = 0
        self.data_index = 0


        self.timer = QTimer()
        self.timer.setInterval(1000)  
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.plot_widget.setLimits(xMin=-1)

    def update_plot(self):
        
        if self.data_index >= len(self.df):
            self.timer.stop()
            return

      
        x_data = range(self.data_index + 1)
        y_data = self.df['VOLTAGE'][:self.data_index+1]
        self.plot_widget.plot(x_data, y_data, clear=True)

        self.data_index += 1
        self.time_index += 1

class mission_time(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()

        # Set up the widget and layout
        self.widget = QWidget()

        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setStyleSheet(''' 
            border: 2px solid black''')

        # Read the Excel file using pandas
        self.data = pd.read_excel("GUI for kalpana software\Add Ons\Sample Data - Software Task.xlsx")

        # Initialize the row index and label
        self.row = 0
        self.rows = ["MISSION_TIME"]
        
        self.label = QLabel()
        self.label.setWordWrap(True)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.label)
        self.layout.addWidget(self.scrollArea)

        # Set up the timer to display the rows
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayRow)
        self.timer.start(1000)  # 1 second interval

    def displayRow(self):
        # Get the row data and append it to the list
        if self.row < len(self.data):
            row_data = self.data.iloc[self.row]['MISSION_TIME']
            self.rows[-1] = (str(row_data))
            self.row += 1
        else:
            self.timer.stop()

        # Update the label with all rows in the list
        self.label.setText("\n".join(self.rows))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 66px; font-weight: bold;")






class temperature(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()

        # Set up the widget and layout
        self.widget = QWidget()

        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setStyleSheet(''' 
            border: 2px solid black''')

        # Read the Excel file using pandas
        self.data = pd.read_excel("GUI for kalpana software\Add Ons\Sample Data - Software Task.xlsx")

        # Initialize the row index and label
        self.row = 0
        self.rows = ["TEMP"]
        
        self.label = QLabel()
        self.label.setWordWrap(True)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.label)
        self.layout.addWidget(self.scrollArea)

        # Set up the timer to display the rows
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayRow)
        self.timer.start(1000)  # 1 second interval

    def displayRow(self):
        # Get the row data and append it to the list
        if self.row < len(self.data):
            row_data = self.data.iloc[self.row]['TEMP']
            self.rows[-1] = (str(row_data))
            self.row += 1
        else:
            self.timer.stop()

        # Update the label with all rows in the list
        self.label.setText("\n".join(self.rows))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 30px; font-weight: bold;")

class voltage(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()

        # Set up the widget and layout
        self.widget = QWidget()

        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setStyleSheet(''' 
            border: 2px solid black''')

        # Read the Excel file using pandas
        self.data = pd.read_excel("GUI for kalpana software\Add Ons\Sample Data - Software Task.xlsx")

        # Initialize the row index and label
        self.row = 0
        self.rows = ["VOLTAGE"]
        
        self.label = QLabel()
        self.label.setWordWrap(True)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.label)
        self.layout.addWidget(self.scrollArea)

        # Set up the timer to display the rows
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayRow)
        self.timer.start(1000)  # 1 second interval

    def displayRow(self):
        # Get the row data and append it to the list
        if self.row < len(self.data):
            row_data = self.data.iloc[self.row]['VOLTAGE']
            self.rows[-1] = (str(row_data))
            self.row += 1
        else:
            self.timer.stop()

        # Update the label with all rows in the list
        self.label.setText("\n".join(self.rows))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 30px; font-weight: bold;")

class altitude(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()

        # Set up the widget and layout
        self.widget = QWidget()

        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setStyleSheet(''' 
            border: 2px solid black''')

        # Read the Excel file using pandas
        self.data = pd.read_excel("GUI for kalpana software\Add Ons\Sample Data - Software Task.xlsx")

        # Initialize the row index and label
        self.row = 0
        self.rows = ["ALTITUDE"]
        
        self.label = QLabel()
        self.label.setWordWrap(True)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.label)
        self.layout.addWidget(self.scrollArea)

        # Set up the timer to display the rows
        self.timer = QTimer()
        self.timer.timeout.connect(self.displayRow)
        self.timer.start(1000)  # 1 second interval

    def displayRow(self):
        # Get the row data and append it to the list
        if self.row < len(self.data):
            row_data = self.data.iloc[self.row]['ALTITUDE']
            self.rows[-1] = (str(row_data))
            self.row += 1
        else:
            self.timer.stop()

        # Update the label with all rows in the list
        self.label.setText("\n".join(self.rows))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 30px; font-weight: bold;")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon("Add Ons\Team Kalpana Logo.png"))

    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec())
