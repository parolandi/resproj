
import output.dissertation.confidence_regions as oucore
import results.plot_data as replda
import results.plots_regions as replre


class Figure00():

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


class Figure06():
    
    def plot_it(self):
        config = Figure00().get_plot_config()
        ellipse = oucore.Figure06().get_ellipsoid()
        center = oucore.Figure06().get_center()
        replre.plot_qudratic_confidence_region_2D_projections_combinatorial(config, center, ellipse)
        
    
if __name__ == '__main__':
    Figure06().plot_it()