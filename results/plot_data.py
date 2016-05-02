
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

def get_plot_colours(dim):
    assert(dim <= 6)
    return ['r', 'g', 'b', 'y', 'c', 'm']

class TimeCourseData():

    independent = None
    measurements = None
    predictions = None
    errors = None

class PlotAxisFormattingData():
    
    min = 0
    max = 0
    label = ""
    #major_ticks = [0]

class PlotTraceFormattingData():
    colour = 'r'
    mark = 'o'

class SinglePlotFormattingData():
    
    x_axis = PlotAxisFormattingData()
    y_axis = PlotAxisFormattingData()
    trace = PlotTraceFormattingData()

class MultiPlotLayoutData():
    no_cols = 0
    no_rows = 0
    #count = 0
    index = 0
    indices = []
    figure = None    

class MultiPlotFormattingData():
    multi_plots = []
    all_axis = PlotAxisFormattingData()
    main_plot = None
    count = 0
    layout = MultiPlotLayoutData()
    multi_traces = []
    
    def __init__(self, count):
        tmp = []
        self.multi_plots = [SinglePlotFormattingData() for ii in range(count)]
        self.count = count
        