
import models.kremlingetal_bioreactor as mokrbi
import results.plot_data as replda
import results.plot_records as replre
import setups.setup_files as sesefi

class Figure0708Config():

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


class Figure00Config():

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
    
    
class Figure1112Config():

    def get_plot_config(self):
        config = replda.TiledPlotFormattingData(4)
        param_names = mokrbi.get_names_parameters_to_be_estimated()
        lbs = [-0.03, -0.15, -0.4, -1]
        ubs = [0.05, 0.15, 0.8, 2.5]
        for ii in range(4):
            config.set_axes_data( \
                replda.PlotAxisFormattingData(). \
                    set_min_max_label(0,0,param_names[ii]). \
                    set_major_ticks([lbs[ii],0,ubs[ii]]), \
                ii)
        return config


class Figure1516Config():

    def get_plot_config(self):
        config = replda.TiledPlotFormattingData(4)
        param_names = mokrbi.get_names_parameters_to_be_estimated()
        lbs = [-0.08, -0.15, -0.5, 0]
        ubs = [0.04, 0.20, 0.1, 35]
        for ii in range(4):
            config.set_axes_data( \
                replda.PlotAxisFormattingData(). \
                    set_min_max_label(0,0,param_names[ii]). \
                    set_major_ticks([lbs[ii],0,ubs[ii]]), \
                ii)
        return config


class Figure07():
    
    def plot_it(self):
        locator = {}
        locator = sesefi.Figure070809().add_urls(locator)
        config = Figure0708Config().get_plot_config()
        replre.plot_nonlinear_confidence_region_2D_projections_combinatorial_scaled_at_record(config, locator)


class Figure08():

    def plot_it(self):
        locator = {}
        locator = sesefi.Figure070809().add_urls(locator)
        config = Figure0708Config().get_plot_config()
        replre.plot_nonlinear_confidence_region_3D_projections_combinatorial_scaled_at_record(config, locator)


class Figure09():

    def plot_it(self):
        locator = {}
        locator = sesefi.Figure070809().add_urls(locator) 
        config = Figure00Config().get_plot_config()
        replre.plot_confidence_regions_2D_scaled_at_record(config, locator)


class Figure11():
    
    def plot_it(self):
        locator = {}
        locator = sesefi.Figure111213().add_urls(locator)
        config = Figure1112Config().get_plot_config()
        replre.plot_nonlinear_confidence_region_2D_projections_combinatorial_scaled_at_record(config, locator)
        
        
class Figure12():

    def plot_it(self):
        locator = {}
        locator = sesefi.Figure111213().add_urls(locator)
        config = Figure1112Config().get_plot_config()
        replre.plot_nonlinear_confidence_region_3D_projections_combinatorial_scaled_at_record(config, locator)
        
        
class Figure13():

    def plot_it(self):
        locator = {}
        locator = sesefi.Figure111213().add_urls(locator)
        config = Figure00Config().get_plot_config()
        replre.plot_confidence_regions_2D_scaled_at_record(config, locator)
        
        
class Figure15():
    
    def plot_it(self):
        locator = {}
        locator = sesefi.Figure151617().add_urls(locator)
        config = Figure1516Config().get_plot_config()
        replre.plot_nonlinear_confidence_region_2D_projections_combinatorial_scaled_at_record(config, locator)
        
        
class Figure16():

    def plot_it(self):
        locator = {}
        locator = sesefi.Figure151617().add_urls(locator)
        config = Figure1516Config().get_plot_config()
        replre.plot_nonlinear_confidence_region_3D_projections_combinatorial_scaled_at_record(config, locator)
        
        
class Figure17():

    def plot_it(self):
        locator = {}
        locator = sesefi.Figure151617().add_urls(locator)
        config = Figure00Config().get_plot_config()
        replre.plot_confidence_regions_2D_scaled_at_record(config, locator)
        
        
if __name__ == '__main__':
    Figure07().plot_it()
    Figure08().plot_it()
    Figure09().plot_it()
    Figure11().plot_it()
    Figure12().plot_it()
    Figure13().plot_it()
    Figure15().plot_it()
    Figure16().plot_it()
    Figure17().plot_it()
    