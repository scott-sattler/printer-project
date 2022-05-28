import PySimpleGUI as sg  # noqa:
from main import InspectQueue, Printer
import threading

char_buff = 0
sec_wait = 0

# config
sg.LOOK_AND_FEEL_TABLE['Native'] = {
    'BACKGROUND': sg.COLOR_SYSTEM_DEFAULT,
    'TEXT': sg.COLOR_SYSTEM_DEFAULT,
    'INPUT': sg.COLOR_SYSTEM_DEFAULT,
    'TEXT_INPUT': sg.COLOR_SYSTEM_DEFAULT,
    'SCROLL': sg.COLOR_SYSTEM_DEFAULT,
    'BUTTON': (sg.COLOR_SYSTEM_DEFAULT, sg.COLOR_SYSTEM_DEFAULT),
    'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0,
}

sg.theme('Native')
# sg.theme_previewer()

sg.set_options(
    margins=(10, 10),
    element_padding=(0, 0),
    font=("Courier New", 12),
    sbar_relief="False",
)


# window contents
column_left = \
    [
        [sg.Column([[sg.Text('Print Text Label')]], justification='center')],
        [sg.Checkbox('Buffer', enable_events=True, default=True, key="-BUFF-", expand_x=True, pad=((0, 0), (5, 5))),
         sg.Checkbox('Time', enable_events=True, default=True, key="-WAIT-", expand_x=True, pad=((0, 0), (5, 5)))],
        [sg.InputText(key="-B1-")],
        [sg.Button(button_text='Print Job 1', pad=((0, 0), (0, 10)), border_width=0)],
        [sg.InputText(key="-B2-")],
        [sg.Button(button_text='Print Job 2', pad=((0, 0), (0, 10)), border_width=0)],
        [sg.Multiline(size=(10, 4), key='-MULTI-', expand_x=True)],
        [sg.Button(button_text='Print Job 3', pad=((0, 0), (0, 10)), border_width=0)],
        [sg.Column([[sg.Button('Exit', border_width=0)]], justification='right')],
    ]

column_center = \
    [
        [sg.Text('Status Information', expand_x=True, justification='c')], [sg.Output(size=(50, 15), key='-CENTER-')],

    ]

column_right = \
    [
        [sg.Text('Printed Label Text', expand_x=True, justification='c')], [sg.Output(size=(50, 15))],
    ]

layout = [
    [
        sg.Column(column_left, justification='top', pad=((0, 20), (0, 0))),
        sg.Column(column_center),
        sg.Column(column_right)
    ]]

# create window
window = sg.Window('', layout, element_justification='l', finalize=True)

if __name__ == "__main__":

    p_app = Printer(debug={'text': False, 'buffer_capacity': 12, 'queue_timeout_sec': 6})

    window['-BUFF-'].update(text=f'{p_app.buffer_capacity} Char Buffer')
    window['-WAIT-'].update(text=f'{p_app.queue_timeout_sec} Second Wait')

    # event loop
    while True:
        pending_job_queue = p_app.label_queue
        if pending_job_queue.qsize() > 0:
            job_text = [i[1] for i in list(pending_job_queue.inspect())]
            if len(job_text) > 0:
                window['-CENTER-'].update('')
                window['-CENTER-'].print(job_text, colors='black')
        else:
            window.find_element(key='-CENTER-').update('')

        event, values = window.read(timeout=50)
        if event in (sg.WIN_CLOSED, 'Exit'):  # if user closes window or clicks cancel
            break
        match event:
            case 'Print Job 1':
                query = values['-B1-']
                threading.Thread(target=p_app.add_print_job, kwargs={'label_text': query}).start()
            case 'Print Job 2':
                query = values['-B2-']
                threading.Thread(target=p_app.add_print_job, kwargs={'label_text': query}).start()
            case 'Print Job 3':
                query = values['-MULTI-']
                threading.Thread(target=p_app.add_print_job, kwargs={'label_text': query}).start()
                window['-CENTER-'].update('')

            case '-BUFF-':
                query = values['-BUFF-']
                if query:
                    p_app.buffer_capacity = p_app.default_debug_values['buffer_capacity']
                    # window['-CENTER-'].print(f"buffer: {p_app.buffer_capacity}", colors='black')
                else:
                    p_app.buffer_capacity = p_app.default_constraints['buffer_capacity']
                    # window['-CENTER-'].print(f"buffer: {p_app.buffer_capacity}", colors='black')
            case '-WAIT-':
                query = values['-WAIT-']
                if query:
                    p_app.buffer_capacity = p_app.default_debug_values['queue_timeout_sec']
                    # window['-CENTER-'].print(f"buffer: {p_app.buffer_capacity}", colors='black')
                else:
                    p_app.buffer_capacity = p_app.default_constraints['queue_timeout_sec']
                    # window['-CENTER-'].print(f"buffer: {p_app.buffer_capacity}", colors='black')

    window.close()
