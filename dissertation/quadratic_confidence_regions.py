
import models.kremlingetal_bioreactor as mokrbi
import output.dissertation.confidence_regions as oucore
import results.plot_data as replda
import results.plots_regions as replre
import utils.confidence_region as utcore

class Figure00():

    def get_plot_config(self):
        config = replda.TiledPlotFormattingData(4)
        param_names = mokrbi.get_names_parameters_to_be_estimated()
        for ii in range(4):
            config.set_axes_data( \
                replda.PlotAxisFormattingData(). \
                    set_min_max_label(0,0,param_names[ii]). \
                    set_major_ticks([-1,0,1]), \
                ii)
        return config


class Figure06():
    
    def plot_it(self):
        config = Figure00().get_plot_config()
        ellipse = oucore.Figure06().get_ellipsoid()
        center = oucore.Figure06().get_center()
        [center, ellipse] = utcore.regularise_ellipsoid_standard(center, ellipse)
        replre.plot_qudratic_confidence_region_2D_projections_combinatorial(config, center, ellipse)
        
    
class Figure10():
    
    def plot_it(self):
        config = Figure00().get_plot_config()
        ellipse = oucore.Figure10().get_ellipsoid()
        center = oucore.Figure10().get_center()
        [center, ellipse] = utcore.regularise_ellipsoid_standard(center, ellipse)
        replre.plot_qudratic_confidence_region_2D_projections_combinatorial(config, center, ellipse)


class Figure14():
    
    def plot_it(self):
        config = Figure00().get_plot_config()
        ellipse = oucore.Figure14().get_ellipsoid()
        center = oucore.Figure14().get_center()
        [center, ellipse] = utcore.regularise_ellipsoid_standard(center, ellipse)
        replre.plot_qudratic_confidence_region_2D_projections_combinatorial(config, center, ellipse)


if __name__ == '__main__':
    Figure06().plot_it()
    Figure10().plot_it()
    Figure14().plot_it()
