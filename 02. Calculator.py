import PySimpleGUI as sg
from random import choice


def create_window(theme, disp_number='_'):
    sg.theme(theme)
    sg.set_options(font='Franklin 14', button_element_size=(6, 3))
    button_size = (6, 3)
    layout = [
        [
            sg.Text(
                disp_number,
                font='Franklin 26',
                justification='right',
                expand_x=True,
                pad=(10, 20),
                right_click_menu=theme_menu,
                key='-TEXT-'
            )
        ],
        [
            sg.Button('AC', expand_x=True),
            sg.Push(),
            sg.Button('/', size=button_size)
        ],
        [
            sg.Button('7', size=button_size),
            sg.Button('8', size=button_size),
            sg.Button('9', size=button_size),
            sg.Button('*', size=button_size)
        ],
        [
            sg.Button('4', size=button_size),
            sg.Button('5', size=button_size),
            sg.Button('6', size=button_size),
            sg.Button('-', size=button_size)
        ],
        [
            sg.Button('1', size=button_size),
            sg.Button('2', size=button_size),
            sg.Button('3', size=button_size),
            sg.Button('+', size=button_size)
        ],
        [
            sg.Button('0', expand_x=True),
            sg.Button('.', size=button_size),
            sg.Button('=', size=button_size)
        ],
    ]
    return sg.Window('Calculator', layout)


theme_list_builtin = sg.theme_list()
current_theme = choice(theme_list_builtin)
theme_menu = ['menu', theme_list_builtin]

window = create_window(current_theme)

running = True
current_no = []
full_operation = []

while running:
    event, value = window.read()
    
    if event == sg.WINDOW_CLOSED:
        running = False
    
    if event in theme_menu[1]:
        window.close()
        window = create_window(event, ''.join(current_no))
    
    if event in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
        current_no.append(event)
        if len(current_no) > 13:
            current_no = current_no[0: 13]
        window['-TEXT-'].update(''.join(current_no))
    
    if event in ['+', '-', '*', '/']:
        if current_no:
            full_operation.append(''.join(current_no))
            current_no = []
            full_operation.append(event)
        else:
            full_operation.pop(-1)
            full_operation.append(event)
        
    if event == '=':
        if current_no:
            full_operation.append(''.join(current_no))
            result = round(eval(''.join(full_operation)), 5)
            if result % 10 == 0:
                result = int(result)
            
            window['-TEXT-'].update(result)
            full_operation = []
            current_no = [str(result)]
        
    if event == 'AC':
        current_no = []
        full_operation = []
        window['-TEXT-'].update("_")
        
window.close()
