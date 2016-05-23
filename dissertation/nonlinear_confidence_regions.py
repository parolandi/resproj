
import models.kremlingetal_bioreactor as mokrbi
import results.plot_data as replda
import results.plot_records as replre
import setups.setup_files as sesefi

class Figure2d():

    def get_plot_config(self):
        config = replda.TiledPlotFormattingData(4)
        param_names = mokrbi.get_names_parameters_to_be_estimated()
        lbs = [-0.04, -0.1, -0.4, -1]
        ubs = [0.04, 0.15, 0.8, 3.5]
        for ii in range(4):
            config.set_axes_data( \
                replda.PlotAxisFormattingData(). \
                    set_min_max_label(0,0,param_names[ii]). \
                    set_major_ticks([lbs[ii],0,ubs[ii]]), \
                ii)
        return config


class Figure3d():

    def get_plot_config(self):
        config = replda.TiledPlotFormattingData(4)
        param_names = mokrbi.get_names_parameters_to_be_estimated()
        lbs = [-0.04, -0.1, -0.4, -1]
        ubs = [0.04, 0.15, 0.8, 3.5]
        for ii in range(4):
            config.set_axes_data( \
                replda.PlotAxisFormattingData(). \
                    set_min_max_label(0,0,param_names[ii]). \
                    set_major_ticks([lbs[ii],0,ubs[ii]]), \
                ii)
        return config


class Figure2d_qcr_ncr():

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
    
    
class Figure0X():
    
    def plot_it(self):
        locator = {}
        locator = sesefi.Figure0X().add_urls(locator)
        config = Figure2d().get_plot_config()
        replre.plot_nonlinear_confidence_region_2D_projections_combinatorial_scaled_at_record(config, locator)
        config = Figure3d().get_plot_config()
        replre.plot_nonlinear_confidence_region_3D_projections_combinatorial_scaled_at_record(config, locator)
        config = Figure2d_qcr_ncr().get_plot_config()
        replre.plot_confidence_regions_2D_scaled_at_record(config, locator)


if __name__ == '__main__':
    Figure0X().plot_it()
