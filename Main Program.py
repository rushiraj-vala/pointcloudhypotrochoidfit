
import sys
import os

import numpy as np

import open3d 
 
from PyQt5 import QtWidgets
import PyQt5.QtGui as Qgui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QFileDialog, QWidget, QFrame, QToolBar, QAction, QSlider)
import pyqtgraph.opengl as gl
import pyqtgraph.Vector as pgVector

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import axes3d, axis3d

class myWindow(QMainWindow):
    fileInput = []
    pcd = []
    XYZ = []
    fileName = ""

    def __init__(self):
        global fileInput, pcd
        super(myWindow,self).__init__() 
        fileInput = []
        pcd = open3d.geometry.PointCloud()
        self.path = os.getcwd()
        self.setGeometry(100, 50, 700, 700)
        self.setWindowTitle('Hello PyQT')
        self.wid = QtWidgets.QWidget()
        self.setCentralWidget(self.wid)
        self.scp = myCanvas()
        

        self.initUI()

    def initUI(self):

        self.vboxMain= QtWidgets.QVBoxLayout(self)

        #### Create a ToolBar
        self.toolbar = QtWidgets.QToolBar('First ToolBar',self)
        
        ## First tool
        addFile = QAction(Qgui.QIcon(),'Add File',self)
        addFile.triggered.connect(self.load_ply)
        self.toolbar.addAction(addFile)

        ## Second Tool
        scatterPLot = QAction(Qgui.QIcon(),'Scatter Plot',self)
        scatterPLot.triggered.connect(self.pyqtgraph_scatter)
        self.toolbar.addAction(scatterPLot)
        
        ## Third Tool
        downSample = QAction(Qgui.QIcon(),'Down sample',self)
        downSample.triggered.connect(self.down_sample)
        self.toolbar.addAction(downSample)

        ## Fourth Tool
        eraseData = QAction(Qgui.QIcon(),'Reset Plot', self)
        eraseData.triggered.connect(lambda: self.plot_scatter(reset=True))
        self.toolbar.addAction(eraseData)

        ## Fifth tool -> Add a plane 
        addPlane = QAction(Qgui.QIcon(),'Add Plane', self)
        addPlane.triggered.connect(self.add_a_plane)
        self.toolbar.addAction(addPlane)

        ## Sixth tool -> Find intersecting 
        findPoints = QAction(Qgui.QIcon(),'Intersecting Points', self)
        findPoints.triggered.connect(self.find_intersecting_points)
        self.toolbar.addAction(findPoints)
        
        ## Seventh tool -> Projecting t 
        projectPoints = QAction(Qgui.QIcon(),'Project Points', self)
        projectPoints.triggered.connect(self.projecting_points)
        self.toolbar.addAction(projectPoints)

        #### Create a FRAME for displaying matplotlib
        self.frame = QtWidgets.QFrame(self)
        self.frame.setLineWidth(1)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)

        # ### Create a Control handle panel
        # ## First create a right frame

        # self.frame_right = QtWidgets.QFrame(self)
        # self.frame_right.setLineWidth(1)
        # self.frame_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        
        # self.hsliderlabel = QtWidgets.QLabel(self)
        # self.hsliderlabel.setText('Voxel Down Sampling')
        # self.hslidervalue = QtWidgets.QLabel(self)
        # self.hslidervalue.setText('0')
        # self.hslidervalue.setAlignment(Qt.AlignCenter)
        
        # self.hLine = QtWidgets.QLineEdit(self)
        # self.hLine.returnPressed.connect(self.down_sample)
        
        # ## Rotate in Elevation
        # self.elevLabel = QtWidgets.QLabel(self)
        # self.elevLabel.setText('Elevation:')
        # self.elevValue = QtWidgets.QLabel(self)
        # self.elevValue.setText(str(self.scp.get_elev_and_azim()[0]))
        # self.elevValue.setAlignment(Qt.AlignCenter)
        
        # self.elevLine = QtWidgets.QLineEdit(self)
        # self.elevLine.returnPressed.connect(self.rotate_Elev)
        
        # ## Rotate in azimuth
        # self.azimLabel = QtWidgets.QLabel(self)
        # self.azimLabel.setText('Azimuth:')
        # self.azimValue = QtWidgets.QLabel(self)
        # self.azimValue.setText(str(self.scp.get_elev_and_azim()[1]))
        # self.azimValue.setAlignment(Qt.AlignCenter)
        
        # self.azimLine = QtWidgets.QLineEdit(self)
        # self.azimLine.returnPressed.connect(self.rotate_Azim)


        # Adding everything to layout
        self.Hbox = QtWidgets.QHBoxLayout(self.frame)
        
        ### right side controls layout
        # self.Vbox_right = QtWidgets.QVBoxLayout(self.frame_right)

        ###  add the widgets

        # ## for down sample
        # self.Vbox_right.addWidget(self.hsliderlabel)
        # self.Vbox_right.addWidget(self.hslidervalue)
        # self.Vbox_right.addWidget(self.hLine)

        # ## for elev
        # self.Vbox_right.addWidget(self.elevLabel)
        # self.Vbox_right.addWidget(self.elevValue)
        # self.Vbox_right.addWidget(self.elevLine)

        # ## for azim
        # self.Vbox_right.addWidget(self.azimLabel)
        # self.Vbox_right.addWidget(self.azimValue)
        # self.Vbox_right.addWidget(self.azimLine)
        # self.Vbox_right.addStretch()

        # self.Hbox.addWidget(self.scp)
        # self.Hbox.addWidget(self.frame_right)

        self.glwidget = gl.GLViewWidget(self.frame)
        self.Hbox.addWidget(self.glwidget)       

        self.vboxMain.addWidget(self.toolbar)
        self.vboxMain.addWidget(self.frame)

        self.wid.setLayout(self.vboxMain)
    
    ## Function to load the file
    def load_ply(self):
        global pcd, fileName
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self.wid,"Open a Point Cloud", self.path,"PLY Files (*.ply) ")
        if fileName:
            pcd = open3d.io.read_point_cloud(fileName)
        else:
            print('The file does not exist or filename is incorrect')

    ## Function to plot the point when clicked on toolbar
    def plot_scatter(self , reset = False):
        global pcd, fileName
        
        if np.asarray(pcd.points).shape[0]==0 :
            print('No Point Cloud Data Found')
        else:
            XYZ = np.asarray(pcd.points)
            if reset is True:
                pcd = open3d.io.read_point_cloud(fileName)
                XYZ = np.asarray(pcd.points)
                self.hslidervalue.setText('0')
                self.hLine.setText('0')
                self.elevValue.setText(str(self.scp.get_elev_and_azim()[0]))
                self.azimValue.setText(str(self.scp.get_elev_and_azim()[1]))
            self.scp.plot_points(XYZ)
            self.elevValue.setText(str(self.scp.get_elev_and_azim()[0]))
            self.azimValue.setText(str(self.scp.get_elev_and_azim()[1]))
    
    def pyqtgraph_scatter(self):
        global pcd, fileName
        if np.asarray(pcd.points).shape[0]==0 :
            print('No Point Cloud Data Found')
            return
        else:
            XYZ = np.asarray(pcd.points)
            self.scatter = self.scp.scatter_pyqtgraph(XYZ)
            self.glwidget.addItem(self.scatter)
            self.axis = gl.GLAxisItem()
            self.glwidget.addItem(self.axis)

            self.grid_xy = gl.GLGridItem()
            # self.glwidget.addItem(self.grid_xy)

            self.grid_yz = gl.GLGridItem()
            self.grid_yz.rotate(90,1,0,0)
            #self.glwidget.addItem(self.grid_yz)
            
            self.grid_xz = gl.GLGridItem()
            self.grid_xz.rotate(90,0,1,0)
            #self.glwidget.addItem(self.grid_xz)
            
            self.glwidget.setCameraPosition( distance=2)
            self.glwidget.opts['azimuth']=90
            self.glwidget.opts['elevation']=90
        
    def add_a_plane(self):
        self.plane_mesh, self.plane_eq = self.scp.create_a_plane()
        self.glwidget.addItem(self.plane_mesh)

    def find_intersecting_points(self, threshold = 0.05):
        global pcd
        a,b,c,d = self.plane_eq
        self.intersects, self.intersecting_points = self.scp.find_and_plot_the_intersecting_points(a,b,c,d,pcd)
        self.glwidget.addItem(self.intersects)
    
    def down_sample(self):
        global pcd
        # value = self.hLine.text()
        # self.hslidervalue.setText(value)
        if np.asarray(pcd.points).shape[0] == 0:
            print('The point cloud is empty or not properly selected')
        # elif float(value) <= 0:
        #     print('The Voxel Size is less than or equal to zero')
        else:
           pcd = pcd.voxel_down_sample(float(0.01))
           XYZ = pcd.points
           self.glwidget.removeItem(self.scatter)
           self.scatter = self.scp.scatter_pyqtgraph(XYZ,colors=(0,0,1,1))
           self.glwidget.addItem(self.scatter)

    def projecting_points(self, threshold = 0.05):
        global pcd
        a,b,c,d = self.plane_eq
        projections = self.scp.project_points_on_plane(a,b,c,d,self.intersects)
        self.glwidget.addItem(projections)

    # def rotate_Elev(self):
    #     value = self.elevLine.text()
    #     self.scp.rotate_plot(value,'null')
    #     elev,azim = self.scp.get_elev_and_azim()
    #     self.elevValue.setText(str(elev))

    # def rotate_Azim(self):
    #     value = self.azimLine.text()
    #     self.scp.rotate_plot('null',value)
    #     elev,azim = self.scp.get_elev_and_azim()
    #     self.azimValue.setText(str(azim))



###### Class for drawing on Canvas #######
class myCanvas(FigureCanvas):
    def __init__(self):
        self.fig =plt.figure(figsize=(6,6))
        FigureCanvas.__init__(self,self.fig)
        self.fig.clear()
        self.ax = self.fig.add_subplot(111,projection='3d')
        self.ax.scatter([0],[0],[0])
 
    # def plot_points(self, points):
    #     x = np.asarray(points)[:,0]
    #     y = np.asarray(points)[:,1]
    #     z = np.asarray(points)[:,2]
    #     self.ax.cla()
    #     self.ax.scatter(x,y,z,c='b',s=0.01)
    #     self.ax.set_xlabel('X')
    #     self.ax.set_ylabel('Y')
    #     self.ax.set_zlabel('Z')
    #     self.ax.view_init(elev=30,azim=-60)
    #     self.fig.canvas.draw_idle()
    
    # def rotate_plot(self,elev_0='null',azim_0='null'):
    #     print((elev_0,azim_0))
    #     if elev_0 == 'null' and azim_0 != 'null':
    #         elev = self.ax.elev
    #         self.ax.view_init(elev,int(azim_0))
    #         self.fig.canvas.draw_idle()
    #         print('You were here')
    #     elif elev_0 != 'null' and azim_0 == 'null':
    #         azim = self.ax.azim
    #         self.ax.view_init(int(elev_0),azim)
    #         self.fig.canvas.draw_idle()
    #         print('You were here')

    # def get_elev_and_azim(self):
    #     if self.ax.elev or self.ax.elev == 0:
    #         print(self.ax.elev)
    #         return self.ax.elev, self.ax.azim
    #     else:
    #         return 'null','null'

    def scatter_pyqtgraph(self,points,colors=(1,1,1,1)):
        x = np.asarray(points)[:,0]
        y = np.asarray(points)[:,1]
        z = np.asarray(points)[:,2]
        scatter = gl.GLScatterPlotItem(pos=np.column_stack((x,y,z)),size=0.02,color=colors)
        return scatter

    def create_a_plane(self,size=1):
        # Define the XZ plane using meshgrid
        x = np.arange(-size, size, 0.1)
        z = np.arange(-size, size, 0.1)
        X, Z = np.meshgrid(x, z)
        Y = np.zeros_like(X)-0.05

        # Create the mesh plane

        verts = np.vstack([X.flatten(), Y.flatten(), Z.flatten()]).transpose()
        faces = []
        for i in range(len(x)-1):
            for j in range(len(z)-1):
                v1 = i*(len(z))+j
                v2 = (i+1)*(len(z))+j
                v3 = (i+1)*(len(z))+j+1
                v4 = i*(len(z))+j+1
                faces.append([v1, v2, v3])
                faces.append([v1, v3, v4])
                
        # Create a GLMeshItem and add it to the GLViewWidget

        mesh = gl.GLMeshItem(vertexes=verts, faces=faces, smooth=False)

        mesh.setColor((1.0, 0.0, 0.0, 0.5))
        mesh.setGLOptions('translucent')

        transform = mesh.transform()
        transform = np.array(transform.data())
        transform = transform.reshape((4, 4))

        # Transform the vertices of the plane by the inverse of the transformation matrix
        invTransform = np.linalg.inv(transform)
        transformedVertices = np.dot(verts, invTransform[:3, :3]) + invTransform[:3, 3]

        # Find the normal vector of the plane based on the transformed vertices
        p1, p2, p3 = transformedVertices[0], transformedVertices[1], transformedVertices[-1]
        v1, v2 = p2 - p1, p3 - p1
        normal = np.cross(v1, v2)
        normal /= np.linalg.norm(normal)

        # Find the distance of the plane from the origin along the normal vector
        d = -np.dot(normal, p1)
        plane_eq = [normal[0],normal[1],normal[2],d]
        return mesh , plane_eq
    
    def find_and_plot_the_intersecting_points(self,a,b,c,d,pcd):
        intersections=[]
        for point in pcd.points:
            x,y,z = point
            if abs(a*x+b*y+c*z+d) <= 0.01:
                print("correct")
                intersections.append(point)
        print(np.asarray(intersections).shape)
        x1 = np.asarray(intersections)[:,0]
        y1 = np.asarray(intersections)[:,1]
        z1 = np.asarray(intersections)[:,2]
        intersects = gl.GLScatterPlotItem(pos=np.column_stack((x1,y1,z1)),size=0.1,color=(0,1,0,1))
        pos=np.column_stack((x1,y1,z1))
        return intersects , pos

    def project_points_on_plane(self,a,b,c,d,intersects):
        planenormal = (a,b,c)
        distance_from_origin = -d / np.linalg.norm(planenormal)
        normalized_normal = planenormal/np.linalg.norm(planenormal)      

        projected_points = []
        for point in intersects:
            # Calculate the distance of the point from the plane
            point_dist = a*point[0] + b*point[1] + c*point[2] + d
            
            # Calculate the projected point
            projected_point = point - point_dist*np.array([a, b, c]) - distance_from_origin*np.array([a, b, c])
            projected_points.append(projected_point)

        projected_points = np.array(projected_points)
        x1 = projected_points[:,0]
        y1 = projected_points[:,1]
        z1 = projected_points[:,2]
        projections = gl.GLScatterPlotItem(pos=np.column_stack((x1,y1,z1)),size=0.1,color=(0,0,1,1))

        return projections



def window():
    app = QApplication(sys.argv)
    win = myWindow()

    win.show()
    sys.exit(app.exec_())

window()