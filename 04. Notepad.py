import PySimpleGUI as sg
from random import choice
from pathlib import Path

sg.theme(choice(sg.theme_list()))

smileys = [
    'Happy', [':)', 'xD', ':D', '<3'],
    'Sad', [':(', 'T_T'],
    'Other', [':3']
]
smileys_event = smileys[1] + smileys[3] + smileys[5]

menu_layout = [
    ['File', ['Open', 'Save', '---', 'Exit']],
    ['Tools', ['Word Count']],
    ['Add', smileys]
]

layout = [
    [sg.Menu(menu_layout)],
    [sg.Text('Untitled', key='-DOCNAME-')],
    [sg.Multiline(no_scrollbar=True, size=(40, 30), key='-TEXTBOX-')]
]

window = sg.Window('Notepad', layout)

running = True

open_file_data = None


def open_file():
    file_path = sg.popup_get_file('open', no_window=True)
    if file_path:
        file = Path(file_path)
        data = file.read_text()
        window['-DOCNAME-'].update(file.name)
        return data


def save_to_file():
    file_path = sg.popup_get_file('Save as', no_window=True, save_as=True, default_extension='.txt',
                                  file_types=(("Text Documents", "*.txt"), ("ALL Files", "*.*"),))
    if file_path:
        file = Path(file_path)
        file.write_text(value['-TEXTBOX-'])
        window['-DOCNAME-'].update(file.name)


while running:
    event, value = window.read()
    
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        if window['-DOCNAME-'].get() == 'Untitled':
            if value['-TEXTBOX-'] != '':
                save_to_file()
        else:
            if open_file_data != value['-TEXTBOX-']:
                if sg.popup_yes_no(title="Do you Want to Save?", ) == 'Yes':
                    save_to_file()
        running = False
    
    if event == 'Open':
        open_file_data = open_file()
        window['-TEXTBOX-'].update(open_file_data)
    
    if event == 'Save':
        save_to_file()
    
    if event == 'Word Count':
        data = value['-TEXTBOX-']
        words = list(filter(lambda x: x != '', data.replace('\n', ' ').split(' ')))
        print(words)
        word_count = len(words)
        char_count = len(''.join(words))
        space_count = data.count(' ')
        sg.Popup(
            f'Word Count: {word_count} \nChar Count: {char_count}\nBlank Space : {space_count}\nTotal Char: {len(data)}')
    
    if event in smileys_event:
        current_text = value['-TEXTBOX-']
        if current_text[-1] == " ":
            new_text = f"{current_text}{event}"
        else:
            new_text = f"{current_text} {event}"
        window['-TEXTBOX-'].update(new_text)

window.close()
