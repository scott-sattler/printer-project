import PySimpleGUI as sg  # noqa:
from main import InspectQueue, Printer
import threading

# config
sg.LOOK_AND_FEEL_TABLE['Native'] = {
    'BACKGROUND': sg.COLOR_SYSTEM_DEFAULT,
    'TEXT': sg.COLOR_SYSTEM_DEFAULT,
    'INPUT': sg.COLOR_SYSTEM_DEFAULT,
    'TEXT_INPUT': sg.COLOR_SYSTEM_DEFAULT,
    'SCROLL': '',  # sg.COLOR_SYSTEM_DEFAULT
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
)

# window contents
column_left = \
    [
        [sg.Column([[sg.Text('Print Text Label')]], justification='center')],
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
        [sg.Output(size=(50, 15), key='-CENTER-')],
    ]

column_right = \
    [
        [sg.Output(size=(50, 15))],
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

    q_app = InspectQueue()
    p_app = Printer(debugging=False, debugging_values=True, enqueue_print=False)

    # usr_input = ''
    # while True:
    #     usr_input = input("Label text (exit() to exit): ")
    #     if usr_input == "exit()":
    #         break
    #     thread = threading.Thread(target=app.add_print_job, kwargs={'label_text': usr_input})
    #     thread.start()
    #
    #     event, values = window.read()
    #     if event in (sg.WIN_CLOSED, 'Exit'):  # if user closes window or clicks cancel
    #         break

    # window.close()

    # event loop
    while True:
        pending_job_queue = p_app.label_queue
        if pending_job_queue.qsize() > 0:
            job_text = list(pending_job_queue.inspect())[-1][1]
            if len(job_text) > 0:
                window['-CENTER-'].print(job_text, colors='black')
        else:  # TODO FIX
            window['-CENTER-'].update('')

        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):  # if user closes window or clicks cancel
            break
        match event:
            case 'Print Job 1':
                query = values['-B1-'].rstrip()
                threading.Thread(target=p_app.add_print_job, kwargs={'label_text': query}).start()

                # print('Print Job from 1:', p_app.print_log.get(), flush=True)
            case 'Print Job 2':
                query = values['-B2-'].rstrip()
                threading.Thread(target=p_app.add_print_job, kwargs={'label_text': query}).start()
                # print('Print Job from 2:', query, flush=True)
            case 'Print Job 3':
                query = values['-MULTI-'].rstrip()
                threading.Thread(target=p_app.add_print_job, kwargs={'label_text': query}).start()
                window['-CENTER-'].update('')
                # print('Print Job from 3:', query, flush=True)

    window.close()


