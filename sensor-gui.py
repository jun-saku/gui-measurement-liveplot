import PySimpleGUI as sg
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime
import matplotlib.animation as anim

_VARS = {'window': False,
         'fig_agg': False,
         'pltFig': False}

plt.style.use('default')

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw_idle()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# initial values (data and index)
plotSize = 25                               # no. of indices in plot
index = np.arange(0, plotSize, 1)           # index array
data = np.zeros(plotSize)                   # dummy initial value
refPoint = 0                                # reference minimum index
i = refPoint
measure = True
measurement_array = []
headings = ['Date', 'Time', 'Distance', 'Time Elapsed']

# create dummy data

def get_data():
    return random.randint(0, 99)


# Pysimple GUI

AppFont = 'Any 16'                                                # change font here
sg.theme('Default1')

# add elements to layout var
layout = [[sg.Canvas(key='figCanvas', background_color='white'),
           sg.Table(values=measurement_array,
                    headings=headings,
                    max_col_width=50,
                    auto_size_columns=False,
                    display_row_numbers=True,
                    justification='right',
                    num_rows=20,
                    key='-TABLE-',
                    row_height=20)],
          [sg.Button('Pause', font=AppFont),
           sg.Button('Close', font=AppFont),
           sg.Button('Save', font=AppFont)]]

_VARS['window'] = sg.Window('River Level Sensor GUI',
                            layout,
                            finalize=True,
                            resizable=True,
                            location=(100, 100),
                            element_justification="center",
                            background_color='white')

def draw_chart():
    _VARS['pltFig'] = plt.figure()
    plt.plot(index, data)
    _VARS['fig_agg'] = draw_figure(_VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])


def update_chart():
    _VARS['fig_agg'].get_tk_widget().forget()
    global data, i, measurement_array
    y_val = get_data()                                            # assign measurement data here
    i += 1                                                        # change minimum index after n points
    j = i + plotSize
    data = np.append(data, y_val)                                 # insert values of measurements here
    date_now = datetime.now()
    yymmdd = date_now.strftime('%m/%d/%Y')
    hhmmss = date_now.strftime('%H:%M:%S.%f')[:-3]
    measurement_array.append([yymmdd, hhmmss, data[j - 2], 'TT.TTTTT'])
    # plt.cla()
    plt.clf()                                                     # clear plot
    plt.plot(index, data[i:j])
    _VARS['fig_agg'] = draw_figure(_VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])


# initialize plot
draw_chart()


# main loop
while True:
    event, values = _VARS['window'].read(timeout=200)
    if event == sg.WIN_CLOSED or event == 'Close':
        # export_csv(measurement_array)                      # added new button below. disregard
        break
    elif event == 'Pause':
        measure = not measure
    if measure:  # add functions for updates here
        update_chart()
        _VARS['window']["-TABLE-"].update(values=measurement_array)
        _VARS['window']["-TABLE-"].Widget.see(i)
    if event == 'Save':
        df = pd.DataFrame(measurement_array, columns=headings)
        time_stamp = datetime.now()
        file_path = 'data_dummy/' + time_stamp.strftime('%m-%d-%Y_%H-%M-%S-%f')[:-3] + '.csv'
        df.to_csv(file_path)
        sg.Popup('File Saved to path: ' + file_path)

_VARS['window'].close()
