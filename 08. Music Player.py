import PySimpleGUI as sg
import base64
from io import BytesIO
from PIL import Image
from pygame import mixer, time

mixer.init()
clock = time.Clock()


def base64_image_import(path):
    image = Image.open(path)
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue())


def buttone_state(state):
    window['-PLAY-'].update(disabled=state)
    window['-PAUSE-'].update(disabled=not state)


# Music File Import
music_path = sg.popup_get_file('Open', no_window=True)
song_name = music_path.split('/')[-1].split('.')[0]
song = mixer.Sound(music_path)

# Timer
song_length = int(song.get_length())
time_since_start = 0
pause_time = 0
playing = False

sg.theme('reddit')

play_path = 'play.png'
pause_path = 'pause.png'

base64_image_import(play_path)

play_layout = [
    [sg.VPush()],
    [sg.Push(), sg.Text(song_name, font='Arial 20'), sg.Push()],
    [sg.VPush()],
    [
        sg.Push(),
        sg.Button(image_data=base64_image_import(play_path), border_width=0, key='-PLAY-'),
        sg.Button(image_data=base64_image_import(pause_path), border_width=0, key='-PAUSE-', disabled=True),
        sg.Push()
    ],
    [sg.VPush()],
    [sg.Push(), sg.Progress(song_length, size=(20, 20), key='-PROGRESS-'), sg.Push()],
    [sg.VPush()]
]
volume_layout = [
    [sg.VPush()],
    [sg.Push(), sg.Slider(range=(0, 100), orientation='h', default_value=10, key='-VOLUME-'), sg.Push()],
    [sg.VPush()]
]

layout = [
    [sg.TabGroup([[
        sg.Tab('Play', play_layout),
        sg.Tab('Volume', volume_layout)
    ]])]
]

window = sg.Window('Music Player', layout)

running = True

while running:
    
    event, values = window.read(timeout=1)
    
    if event == sg.WINDOW_CLOSED:
        running = False
    
    if playing:
        time_since_start = time.get_ticks()
        window['-PROGRESS-'].update_bar((time_since_start - pause_time) // 1000, song_length)
    
    if event == '-PLAY-':
        playing = True
        pause_time += time.get_ticks() - time_since_start
        
        if mixer.get_busy():
            buttone_state(True)
            mixer.unpause()
        else:
            buttone_state(True)
            song.play()
    
    if event == '-PAUSE-':
        playing = False
        buttone_state(False)
        mixer.pause()
    
    if not mixer.get_busy() and playing:
        playing = False
        buttone_state(False)
        time_since_start = 0
        pause_time = 0
    
    song.set_volume(values['-VOLUME-'] / 100)

window.close()
