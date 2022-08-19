import PySimpleGUI as sg
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def update_figure(data):
    axes = fig.axes
    x = [i[0] for i in data]
    y = [int(i[1]) for i in data]
    axes[0].plot(x, y, 'r-')
    figute_canvas_agg.draw()
    figute_canvas_agg.get_tk_widget().pack()


sg.theme('DarkTeal6')
table_content = []

layout = [
    [sg.Table(headings=['Observation', 'Result'],
              values=table_content,
              expand_x=True,
              hide_vertical_scroll=True,
              key='-TABLE-')],
    [sg.Input(key='-INPUT-', expand_x=True), sg.Button('Submit')],
    [sg.Canvas(key='-CANVAS-')]
]

window = sg.Window('Graph App', layout, finalize=True)

running = True

# Matplot Lib
fig = matplotlib.figure.Figure(figsize=(5, 4))
fig.add_subplot(111).plot([], [])
figute_canvas_agg = FigureCanvasTkAgg(fig, window['-CANVAS-'].TKCanvas)
figute_canvas_agg.draw()
figute_canvas_agg.get_tk_widget().pack()

while running:
    event, value = window.read()
    
    if event == sg.WINDOW_CLOSED:
        running = False
    
    if event == 'Submit':
        new_value = value['-INPUT-']
        if new_value.isnumeric():
            
            table_content.append([len(table_content) + 1, float(new_value)])
            
            window['-INPUT-'].update("")
            window['-TABLE-'].update(table_content)
            update_figure(table_content)
        else:
            sg.Popup("Enter Numbers")
            window['-INPUT-'].update("")

window.close()
