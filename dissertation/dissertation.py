
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
                set_y_axis(replda.PlotAxisFormattingData().set_min_max_label_units(0,0,"X", " [g/L]")). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[0], 'o')), \
                0)
        config.set_formatting_data( \
            replda.SinglePlotFormattingData(). \
                set_x_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"")). \
                set_y_axis(replda.PlotAxisFormattingData().set_min_max_label_units(0,0,"S", " [g/L]")). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[1], 'o')), \
                1)
        config.set_formatting_data( \
            replda.SinglePlotFormattingData(). \
                set_x_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"")). \
                set_y_axis(replda.PlotAxisFormattingData().set_min_max_label_units(0,0,"M1", " [umol/g]")). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[2], 'o')), \
                2)
        config.set_formatting_data( \
            replda.SinglePlotFormattingData(). \
                set_x_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"")). \
                set_y_axis(replda.PlotAxisFormattingData().set_min_max_label_units(0,0,"M2", " [umol/g]")). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[3], 'o')), \
                3)
        config.set_formatting_data( \
            replda.SinglePlotFormattingData(). \
                set_x_axis(replda.PlotAxisFormattingData().set_min_max_label_units(0,0,"Time", " [hr]")). \
                set_y_axis(replda.PlotAxisFormattingData().set_min_max_label_units(0,0,"E", " [umol/g]")). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[4], 'o')), \
                4)
        return config


class Figure01():
    
    def plot_it(self):
        config = Figure00().get_plot_config()
        locator = {}
        sesefi.Figure01().add_urls(locator)
        replre.plot_tiled_calibration_and_validation_trajectories_at_record(config, locator)


class Figure02():
    
    def plot_it(self):
        config = Figure00().get_plot_config()
        locator = {}
        sesefi.Figure02().add_urls(locator)
        replre.plot_tiled_calibration_and_validation_trajectories_at_record(config, locator)


if __name__ == '__main__':
    Figure01().plot_it()
    Figure02().plot_it()