
import output.dissertation.confidence_regions as oucore
import results.plots_regions as replre


class Figure00():

    def get_plot_config(self):
        return None


class Figure06():
    
    def plot_it(self):
        ellipse = oucore.Figure06().get_ellipsoid()
        center = oucore.Figure06().get_center()
        replre.plot_qudratic_confidence_region_2D_projections_combinatorial(center, ellipse)
        
    
if __name__ == '__main__':
    Figure06().plot_it()