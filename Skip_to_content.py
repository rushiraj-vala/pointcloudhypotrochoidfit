import PySimpleGUI as sg
import matplotlib.pyplot as plt
import os 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

working_directory = os.getcwd()

year = [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010]
unemployment_rate = [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
  
def create_plot(year, unemployment_rate):
    plt.figure(figsize=(4,4))
    plt.scatter(year, unemployment_rate, color='red', marker='o')
    plt.title('Unemployment Rate Vs Year', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Unemployment Rate', fontsize=14)
    plt.grid(True)
    # plt.figure(figsize=(6,6))
    return plt.gcf()

layout = [[sg.Text('Line Plot')],
          [sg.Text("Choose a .PLY format file: ")],
          [sg.InputText(key="-FILE_PATH-"), sg.FileBrowse(initial_folder = working_directory, file_types=[("PLY Files","*.ply")])],
          [sg.Canvas(size=(300, 300), key='-CANVASA-')],
          [sg.Button('Submit'),sg.Exit()]
         ]

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def move_center(window):
    screen_width, screen_height = window.get_screen_dimensions()
    win_width, win_height = window.size
    x, y = (screen_width - win_width)//2, (screen_height - win_height)//2
    window.move(x, y)

window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout, finalize=True, element_justification='center')

move_center(window)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Submit':
        draw_figure(window['-CANVASA-'].TKCanvas, create_plot(year, unemployment_rate))

window.close()