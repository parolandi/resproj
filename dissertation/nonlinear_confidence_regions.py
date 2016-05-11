
import results.plot_records as replre
import setups.setup_files as sesefi


class Figure0X():
    
    def plot_it(self):
        config = None
        locator = {}
        locator = sesefi.Figure0X().add_urls(locator)
        replre.plot_nonlinear_confidence_region_2D_projections_combinatorial_at_record(config, locator)
        replre.plot_nonlinear_confidence_region_3D_projections_combinatorial_at_record(config, locator)

if __name__ == '__main__':
    Figure0X().plot_it()