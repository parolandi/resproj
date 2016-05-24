
import results.plot_data as replda
import results.plot_records as replre
import setups.setup_files as sesefi


class Figure00():

    def get_plot_config(self):
        count = 5
        config = replda.MultiPlotFormattingData(count).set_layout_data( \
            replda.MultiPlotLayoutData().set_no_cols_no_rows_indices(1, count, [0,1]))
        config.set_formatting_data( \
            replda.SinglePlotFormattingData(). \
                set_x_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"")). \
                set_y_axis(replda.PlotAxisFormattingData(). \
                    set_min_max_label_units(0,0,"X", " [g/L]"). \
                    set_major_ticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[0], 'o')), \
                0)
        config.set_formatting_data( \
            replda.SinglePlotFormattingData(). \
                set_x_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"")). \
                set_y_axis(replda.PlotAxisFormattingData(). \
                    set_min_max_label_units(0,0,"S", " [g/L]"). \
                    #set_major_ticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0])). \
                    set_major_ticks([0.0, 0.4, 0.8, 1.2, 1.6, 2.0])). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[1], 'o')), \
                1)
        config.set_formatting_data( \
            replda.SinglePlotFormattingData(). \
                set_x_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"")). \
                set_y_axis(replda.PlotAxisFormattingData(). \
                    set_min_max_label_units(0,0,"M1", " [umol/g]"). \
                    #set_major_ticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])). \
                    set_major_ticks([0.0, 0.2, 0.4, 0.6, 0.8])). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[2], 'o')), \
                2)
        config.set_formatting_data( \
            replda.SinglePlotFormattingData(). \
                set_x_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"")). \
                set_y_axis(replda.PlotAxisFormattingData(). \
                    set_min_max_label_units(0,0,"M2", " [umol/g]"). \
                    #set_major_ticks([0.0, 2E-3, 4E-3, 6E-3, 8E-3, 1E-2, 1.2E-2, 1.4E-2, 1.6E-2, 1.8E-2, 2E-2])). \
                    set_major_ticks([0.0, 4E-3, 8E-3, 1.2E-2, 1.6E-2, 2E-2, 2.4E-2])). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[3], 'o')), \
                3)
        config.set_formatting_data( \
            replda.SinglePlotFormattingData(). \
                set_x_axis(replda.PlotAxisFormattingData().set_min_max_label_units(0,0,"Time", " [hr]")). \
                set_y_axis(replda.PlotAxisFormattingData(). \
                    set_min_max_label_units(0,0,"E", " [umol/g]"). \
                    #set_major_ticks([0.0, 1E-2, 2E-2, 3E-2, 4E-2, 5E-2, 6E-2, 7E-2, 8E-2])). \
                    #set_major_ticks([0.0, 2E-2, 4E-2, 6E-2, 8E-2])). \
                    set_major_ticks([0.0, 1.5E-2, 3E-2, 4.5E-2, 6E-2, 7.5E-2, 9E-2])). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[4], 'o')), \
                4)
        return config


class Figure01():
    
    def plot_it(self):
        config = Figure00().get_plot_config()
        config.set_window_data(replda.WindowPlotData().set_title("Figure 01"))
        locator = {}
        sesefi.Figure01().add_urls(locator)
        replre.plot_tiled_calibration_and_validation_trajectories_at_record(config, locator)


class Figure02():
    
    def plot_it(self):
        config = Figure00().get_plot_config()
        config.set_window_data(replda.WindowPlotData().set_title("Figure 02"))
        locator = {}
        sesefi.Figure02().add_urls(locator)
        replre.plot_tiled_calibration_and_validation_trajectories_at_record(config, locator)


class Figure03():
    
    def plot_it(self):
        config = Figure00().get_plot_config()
        config.set_window_data(replda.WindowPlotData().set_title("Figure 03"))
        locator = {}
        sesefi.Figure03().add_urls(locator)
        replre.plot_tiled_calibration_and_validation_trajectories_at_record(config, locator)
        
        
class Figure04():
    
    def plot_it(self):
        config = Figure00().get_plot_config()
        config.set_window_data(replda.WindowPlotData().set_title("Figure 04"))
        locator = {}
        sesefi.Figure04().add_urls(locator)
        replre.plot_tiled_calibration_and_validation_trajectories_at_record(config, locator)
        
        
class Figure05():
    
    def plot_it(self):
        config = Figure00().get_plot_config()
        config.set_window_data(replda.WindowPlotData().set_title("Figure 05"))
        locator = {}
        sesefi.Figure05().add_urls(locator)
        replre.plot_tiled_calibration_and_validation_trajectories_at_record(config, locator)
        
        
if __name__ == '__main__':
    Figure01().plot_it()
    Figure02().plot_it()
    Figure03().plot_it()
    Figure04().plot_it()
    Figure05().plot_it()
