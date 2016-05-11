from Cython.Compiler.Naming import self_cname

import numpy as np


plot_data = {
    "figure": None,
    "index": 0,
    "no_cols": 0,
    "no_rows": 0,
    "plot_count": 0,
    "title": "",
    "window_title": "",
    "ylabel": "",
    }


class WindowPlotData():
    
    title = ""
    
    def set_title(self, value):
        self.title = value
        return self


def get_plot_colours(dim):
    assert(dim <= 6)
    return ['r', 'g', 'b', 'y', 'c', 'm']


class TimeCourseData():

    independent = None
    measurements = None
    predictions = None
    errors = None
    
    def set_independent(self, values):
        self.independent = values
        return self
    
    def set_measurements(self, values):
        self.measurements = values
        return self
    
    def set_predictions(self, values):
        self.predictions = values
        return self
    
    def set_errors(self, values):
        self.errors = values
        return self


class PlotAxisFormattingData():
    
    min_val = 0
    max_val = 0
    label = ""
    # TODO hard-coded
    major_ticks = np.arange(0,60+1,2)
    eng_units = ""
    
    def set_min_max_label(self, min_val, max_val, label):
        self.min_val = min_val
        self.max_val = max_val
        self.label = label
        return self

    def set_min_max_label_units(self, min_val, max_val, label, units):
        self.set_min_max_label(min_val, max_val, label)
        self.eng_units = units
        return self
    

class PlotTraceFormattingData():
    
    colour = 'r'
    mark = 'o'
    
    def set_colour_mark(self, colour, mark):
        self.colour = colour
        self.mark = mark
        return self


# SubplotFormattingData
class SinglePlotFormattingData():
    
    x_axis = PlotAxisFormattingData()
    y_axis = PlotAxisFormattingData()
    trace = PlotTraceFormattingData()
    
    def set_x_axis(self, data):
        self.x_axis = data
        return self
        
    def set_y_axis(self, data):
        self.y_axis = data
        return self
    
    def set_trace(self, data):
        self.trace = data
        return self 


class MultiPlotLayoutData():
    
    no_cols = 0
    no_rows = 0
    #count = 0
    index = 0
    indices = []
    figure = None
    
    def set_no_cols_no_rows_indices(self, no_cols, no_rows, indices):
        self.no_cols = no_cols
        self.no_rows = no_rows
        self.indices = indices
        return self


class MultiPlotFormattingData():
    
    count = 0
    layout = MultiPlotLayoutData()
    multi_plots = []
    window = WindowPlotData()
    
    def __init__(self, count):
        self.multi_plots = [SinglePlotFormattingData() for _ in range(count)]
        self.count = count
        
    def set_formatting_data(self, data, index):
        self.multi_plots[index] = data
        return self
    
    def set_layout_data(self, data):
        self.layout = data
        return self

    def set_window_data(self, data):
        self.window = data
        return self
