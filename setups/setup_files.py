
import common.io as coio
import common.environment as coen

class Figure01():

    def add_urls(self, config):
        pathfile = coen.get_output_location()
        config["locator"] = coio.FileResources(). \
            set_measured_calibration(pathfile+"fig-01-measured-calib.csv"). \
            set_measured_validation(pathfile+"fig-01-measured-valid.csv"). \
            set_predicted_calibration(pathfile+"fig-01-predicted-calib.csv"). \
            set_predicted_validation(pathfile+"fig-01-predicted-valid.csv")
        return config