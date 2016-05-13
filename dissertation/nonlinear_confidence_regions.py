
import results.plot_data as replda
import results.plot_records as replre
import setups.setup_files as sesefi


class Figure2d():

    def get_plot_config(self):
        config = replda.TiledPlotFormattingData(4)
        config.set_axes_data( \
            replda.PlotAxisFormattingData().set_min_max_label(0,0,"p1"), 0). \
        set_axes_data(
            replda.PlotAxisFormattingData().set_min_max_label(0,0,"p2"), 1). \
        set_axes_data(
            replda.PlotAxisFormattingData().set_min_max_label(0,0,"p3"), 2). \
        set_axes_data(
            replda.PlotAxisFormattingData().set_min_max_label(0,0,"p4"), 3)
        return config


class Figure3d():

    def get_plot_config(self):
        config = replda.TiledPlotFormattingData(4)
        return config


class Figure0X():
    
    def plot_it(self):
        locator = {}
        locator = sesefi.Figure0X().add_urls(locator)
        config = Figure2d().get_plot_config()
        replre.plot_nonlinear_confidence_region_2D_projections_combinatorial_at_record(config, locator)
        config = Figure3d().get_plot_config()
        replre.plot_nonlinear_confidence_region_3D_projections_combinatorial_at_record(config, locator)


if __name__ == '__main__':
    Figure0X().plot_it()