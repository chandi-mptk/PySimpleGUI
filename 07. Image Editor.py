import PySimpleGUI as sg
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO


def update_image(orig, blur, contrast, emboss, contour, flipx, flipy):
    image = orig.filter(ImageFilter.GaussianBlur(blur))
    image = image.filter(ImageFilter.UnsharpMask(contrast))
    
    if emboss:
        image = image.filter(ImageFilter.EMBOSS())
    if contour:
        image = image.filter(ImageFilter.CONTOUR())
    
    if flipx:
        image = ImageOps.mirror(image)
    if flipy:
        image = ImageOps.flip(image)
    
    bytes = BytesIO()
    image.save(bytes, format='PNG')
    window['-IMAGE-'].update(data=bytes.getvalue())
    return image


image_path = sg.popup_get_file("Open", no_window=True)
control_column = sg.Column([
    [sg.Frame('Blur', layout=[[sg.Slider(range=(0, 10), orientation='h', key='-BLUR-')]])],
    [sg.Frame('Contrast', layout=[[sg.Slider(range=(0, 10), orientation='h', key='-CONTRAST-')]])],
    [sg.Checkbox('Emboss', key='-EMBOSS-'), sg.Checkbox('Contour', key='-CONTOUR-')],
    [sg.Checkbox('Flip X', key='-FLIPX-'), sg.Checkbox('Flip Y', key='-FLIPY-')],
    [sg.Button('Save image', key='-SAVE-')],

])
image_column = sg.Column([[sg.Image(image_path, key='-IMAGE-')]])
layout = [
    [control_column, image_column]
]

original = Image.open(image_path)
window = sg.Window('Image Editor', layout)

running = True

while running:
    event, values = window.read(timeout=10)
    
    if event == sg.WINDOW_CLOSED:
        running = False
        
    if event == '-SAVE-':
        save_path = sg.popup_get_file(
            'Save',
            save_as=True,
            no_window=True,
            default_extension='.png',
            file_types=(("PNG", "*.png"), )
        )
        if save_path:
            image.save(save_path, 'PNG')
    
    image = update_image(
        original,
        values['-BLUR-'],
        values['-CONTRAST-'],
        values['-EMBOSS-'],
        values['-CONTOUR-'],
        values['-FLIPX-'],
        values['-FLIPY-']
    )

window.close()
