
import results.plot_data as replda
import results.plot_records as replre
import setups.setup_files as sesefi


class Figure01():

    def get_plot_config(self):
        count = 5
        config = replda.MultiPlotFormattingData(count).set_layout_data( \
            replda.MultiPlotLayoutData().set_no_cols_no_rows_indices(1, count, [0,1]))
        config.set_formatting_data( \
            replda.SinglePlotFormattingData(). \
                set_x_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"")). \
                set_y_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"X")). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[0], 'o')), \
                0)
        config.set_formatting_data( \
            replda.SinglePlotFormattingData(). \
                set_x_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"")). \
                set_y_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"S")). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[1], 'o')), \
                1)
        config.set_formatting_data( \
            replda.SinglePlotFormattingData(). \
                set_x_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"")). \
                set_y_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"M1")). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[2], 'o')), \
                2)
        config.set_formatting_data( \
            replda.SinglePlotFormattingData(). \
                set_x_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"")). \
                set_y_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"M2")). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[3], 'o')), \
                3)
        config.set_formatting_data( \
            replda.SinglePlotFormattingData(). \
                set_x_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"Time")). \
                set_y_axis(replda.PlotAxisFormattingData().set_min_max_label(0,0,"E")). \
                set_trace(replda.PlotTraceFormattingData().set_colour_mark(replda.get_plot_colours(6)[4], 'o')), \
                4)
        return config

    def plot_it(self):
        config = self.get_plot_config()
        locator = {}
        sesefi.Figure01().add_urls(locator)
        replre.plot_tiled_calibration_and_validation_trajectories_at_record(config, locator)

if __name__ == '__main__':
    Figure01().plot_it()