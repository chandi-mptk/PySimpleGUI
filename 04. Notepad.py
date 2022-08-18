import PySimpleGUI as sg
from random import choice


def create_window(theme):
    sg.theme(theme)
    menu_layout = [
        ['File', ['Open', 'Save', '---', 'Exit']],
        ['Tools', ['Word Count']],
    ]
    
    layout = [
        [sg.Menu(menu_layout)],
        [sg.Text('Untitled', key='-DOCNAME-')],
        [sg.Multiline(no_scrollbar=True, size=(40, 30), key='-TEXTBOX-')]
    ]
    return sg.Window('Notepad', layout)


window = create_window(choice(sg.theme_list()))

running = True

while running:
    event, value = window.read()
    
    if event == sg.WINDOW_CLOSED:
        running = False
    
    if event == 'Word Count':
        data = value['-TEXTBOX-']
        words = list(filter(lambda x: x != '', data.replace('\n', ' ').split(' ')))
        print(words)
        word_count = len(words)
        char_count = len(''.join(words))
        space_count = data.count(' ')
        sg.Popup(
            f'Word Count: {word_count} \nChar Count: {char_count}\nBlank Space : {space_count}\nTotal Char: {len(data)}')

window.close()
