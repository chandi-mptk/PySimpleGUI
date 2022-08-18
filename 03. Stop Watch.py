import PySimpleGUI as sg
from time import time
from tkinter import *

sg.theme('black')
layout = [
    [sg.Push(), sg.Image('close.png', pad=0, enable_events=True, key='-CLOSE-')],
    # [sg.VPush()],
    [sg.Text('', font='Young 50', key='-TIME-')],
    [
        sg.Button('Start', button_color=('#FFFFFF', '#FF0000'), border_width=0, key='-STARTSTOP-'),
        sg.Button('Lap', button_color=('#FFFFFF', '#FF0000'), border_width=0, key='-LAP-', visible=False)
    ],
    [sg.Column([[]], key='-LAPS-')],
    [sg.VPush()]
]
window = sg.Window(
    'Stopwatch',
    layout,
    size=(300, 300),
    no_titlebar=True,
    element_justification='center'
)

running = True
start_time = 0
active = False
lap_counter = 0

while running:
    event, value = window.read(timeout=10)
    
    if event in (sg.WINDOW_CLOSED, '-CLOSE-'):
        running = False
        
    if event == '-STARTSTOP-':
        start_time = time()
        active = not active
        if active:
            window['-LAP-'].update(visible=True)
            window['-STARTSTOP-'].update(text='Stop')
        else:
            window['-LAP-'].update(visible=False)
            window['-STARTSTOP-'].update(text='Start')
            lap_counter = 0
            elapsed_time = 0
    
    if active:
        elapsed_time = round(time() - start_time, 1)
        window['-TIME-'].update(elapsed_time)
    
    if event == '-LAP-':
        lap_counter += 1
        if lap_counter > 4:
            window[f'-{lap_counter - 4}-'].update(visible=False)
            window[f'-{lap_counter - 4}-'].Widget.master.pack_forget()
            window.extend_layout(container=window['-LAPS-'], rows=[[sg.Column(
                layout=[[sg.Text(lap_counter), sg.VSeparator(), sg.Text(elapsed_time)]], key=f'-{lap_counter}-')]])
        else:
            window.extend_layout(container=window['-LAPS-'], rows=[[sg.Column(
                layout=[[sg.Text(lap_counter), sg.VSeparator(), sg.Text(elapsed_time)]], key=f'-{lap_counter}-')]])
        
        
window.close()
