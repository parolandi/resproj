
import output.dissertation.confidence_regions as oucore
import results.plots_regions as replre

if __name__ == '__main__':
    ellipse = oucore.Figure06().get_ellipsoid()
    center = oucore.Figure06().get_center()
    replre.plot_qudratic_confidence_region_2D_projections_combinatorial(center, ellipse)
