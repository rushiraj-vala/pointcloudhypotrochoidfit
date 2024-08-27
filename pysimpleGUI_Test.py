import PySimpleGUI as sg
import open3d as op3
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FCTA

working_directory = os.getcwd()
XYZ=[]
X=[]
Y=[]
Z=[]

# global dictionary
_vars = {'window': False,
         'fig_agg': False,
         'plt_fig': False,
         'figure': False,
         'axes': False,
         'azimuth': '',
         'elevation': '',
         }

def open_ply_file(ply_file_path):
    pcd = op3.io.read_point_cloud(ply_file_path)
    XYZ = np.asarray(pcd.points)
    X = XYZ[:,0] 
    Y = XYZ[:,1] 
    Z = XYZ[:,2] 
    print(X[0])
    return XYZ, X, Y, Z

def create_parallel_plane(value, axis='y'):
    if axis == 'z' or axis == 'Z':
        x_mesh = np.linspace(-0.5,0.5,10)
        y_mesh = np.linspace(-0.5,0.5,10)
        z_mesh = np.ones(x_mesh.shape)*value 
        x, y = np.meshgrid(x_mesh,y_mesh)
        z = 0*x + 0*y + value
        return x ,y,z

    elif axis == 'x' or axis == 'X':
        y_mesh = np.linspace(-0.5,0.5,10)
        z_mesh = np.linspace(-0.5,0.5,10)
        x_mesh = np.ones(y_mesh.shape)*value 
        y, z = np.meshgrid(y_mesh,z_mesh)
        x = 0*y + 0*z + value
        return x ,y,z

    elif axis == 'y' or axis == 'Y':
        x_mesh = np.linspace(-0.5,0.5,10)
        z_mesh = np.linspace(-0.5,0.5,10)
        y_mesh = np.ones(x_mesh.shape)*value 
        x, z= np.meshgrid(x_mesh,z_mesh)
        y = 0*x + 0*z + value
        return x ,y,z
    else :
        print('No proper parallel plane selected')

def draw_figure(canvas, figure):
    figure_canvas_agg = FCTA(figure,canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both',expand=1)
    return figure_canvas_agg

def create_scatter_plot(x,y,z,marker_size,color,title,x_label,y_label, z_label, plane='y',plane_height=0):
    x_mesh,y_mesh,z_mesh = create_parallel_plane(plane_height,plane)
    plt.cla()
    plt.clf()
    fig = plt.figure() 
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x_mesh,y_mesh,z_mesh,color='red',alpha=0.5)
    ax.scatter(x,y,z,color=str(color),s=marker_size)
    fig.set_figheight(5,True)  # Cannot be too small other wise white figure
    fig.set_figwidth(5,True)  # Cannot be too small other wise white figure
    plt.title(str(title),fontsize=14)
    ax.set_xlabel(str(x_label))
    ax.set_ylabel(str(y_label))
    ax.set_zlabel(str(z_label))
    ax.elev = 30
    ax.azim = 30
    
    _vars['figure'] = fig
    _vars['axes'] = ax
    _vars['azimuth']=ax.azim
    _vars['elevation']=ax.elev
    window['azimu'].update(_vars['azimuth'])
    window['elev'].update(_vars['elevation'])
    _vars['fig_agg']=draw_figure(window['-CANVAS0-'].TKCanvas,_vars['figure'])
    return  

def rotate_along_az(value):
    _vars['fig_agg'].get_tk_widget
    _vars['azimuth']
    _vars['elevation']
    
    window['elev'].update(_vars['elevation'])
    draw_figure(window['-CANVAS0-'].TKCanvas,_vars['figure'])
    return 


def move_center(window):
    screen_width, screen_height = window.get_screen_dimensions()
    win_width, win_height = window.size
    x, y = (screen_width - win_width)//2, (screen_height - win_height)//2
    window.move(x, y)

layout = [
    [sg.Text("Choose a .PLY format file: ")],
    [sg.InputText(key="-FILE_PATH-"),
    sg.FileBrowse(initial_folder = working_directory, file_types=[("PLY Files","*.ply")]),
    sg.Button("Ok")],
    [sg.Canvas(size=(1200,600),key="-CANVAS0-")],
    #  sg.Canvas(size=(300,300),key="-CANVAS1-")],
    # [sg.Canvas(size=(300,300),key="-CANVAS2-")],
    [sg.Button(" <- "),sg.Text(key='azimu'),sg.Button(" -> ")],
    [sg.Button(" ^ "),sg.Text(key='elev'),sg.Button(" v ")],
    [sg.Button("Exit")]
] 

window = sg.Window( title = "3D Point Cloud", layout = layout, element_justification='center',finalize=True)

move_center(window)

while True:
    event, values = window.read()
    # End program if press OK or click on closed
    if event == "Exit" or event == sg.WIN_CLOSED:

        break
    elif event == "Ok":
        if values["-FILE_PATH-"] != "":
            ply_file_path_0 = values["-FILE_PATH-"]
            XYZ_0, X_0, Y_0, Z_0 = open_ply_file(ply_file_path=ply_file_path_0)
            create_scatter_plot(X_0,Y_0,Z_0, 0.01,'blue','X - Y','X','Y','Z',plane='y',plane_height=0)
            # draw_figure(window['-CANVAS1-'].TKCanvas,create_scatter_plot(Y_0,Z_0,0.01,'green','Y - Z','Y','Z',plane='x',plane_height=0))
            # draw_figure(window['-CANVAS2-'].TKCanvas,create_scatter_plot(Z_0,X_0,0.01,'red','Z - X','Z','X',plane='y',plane_height=0))

window.close()

