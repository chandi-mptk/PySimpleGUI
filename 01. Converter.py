import PySimpleGUI as sg
from string import digits

spin_list = ['KM to Mile', 'KG to Pound', 'Sec to Min']
max_len_list = max(map(lambda x: len(x), spin_list)) + 1
number_list = ['.']
number_list.extend(list(digits))

layout = [
    [
        sg.Input(key='-INPUT-'),
        sg.Spin(spin_list, key='-UNITS-', size=max_len_list),
        sg.Button('Convert', key='-CONVERT-')
    ],
    [sg.Text('Output', key='-OUTPUT-'), ],
]
window = sg.Window('Converter', layout)

running = True


def km_to_mile(input_no, decimals):
    output = round(float(input_no) * 0.621371, decimals)
    return f'{input_val} KM are {output} Miles'


def kg_to_pound(input_no, decimals):
    output = round(float(input_no) * 2.20462, decimals)
    return f'{input_val} KG are {output} Pounds'


def sec_to_min(input_no, decimals):
    output = round(float(input_no) * 0.0166667, decimals)
    return f'{input_val} Seconds are {output} Minutes'


while running:
    event, value = window.read()
    if event == sg.WINDOW_CLOSED:
        running = False
    if event == '-CONVERT-':
        input_val = value['-INPUT-']
        window['-INPUT-'].update('')
        if input_val.isnumeric():
            decimals = 2 if ('.' not in input_val) else len(input_val.split('.')[1])
            match value['-UNITS-']:
                case 'KM to Mile':
                    output_str = km_to_mile(input_val, decimals)
                case 'KG to Pound':
                    output_str = kg_to_pound(input_val, decimals)
                case 'Sec to Min':
                    output_str = sec_to_min(input_val, decimals)
        else:
            output_str = f'{input_val} not valid'
        window['-OUTPUT-'].update(output_str)

window.Close()
