import sys
import numpy as np
import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the pyqtgraph widget
        self.widget = gl.GLViewWidget(self)

        # Set the camera position
        self.widget.opts['distance'] = 20
        self.widget.opts['elevation'] = 30
        self.widget.opts['azimuth'] = 30

        # Add some data to plot
        x = [1, 2, 3, 4]
        y = [5, 6, 7, 8]
        z = [9, 10, 11, 12]
        scatter = gl.GLScatterPlotItem(pos=np.column_stack((x, y, z)), size=0.5, color=(1, 0, 0, 1))

        # Add the scatter plot item to the widget
        self.widget.addItem(scatter)

        # Add an interactive plane
        self.plane = gl.GLGridItem()
        self.plane.rotate(90, 0, 1, 0)
        self.widget.addItem(self.plane)

        # Set the widget as the central widget of the main window
        self.setCentralWidget(self.widget)

        # Set the main window properties
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Interactive 3D Plot with Plane')

        # Show the main window
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
