
import common.io as coio
import common.environment as coen

class Figure01():

    def add_urls(self, config):
        pathfile = coen.get_output_location()
        config["locator"] = coio.FileResources(). \
            set_measured_calibration(pathfile+"fig-01-measured-calib.csv"). \
            set_measured_validation(pathfile+"fig-01-measured-valid.csv"). \
            set_predicted_calibration(pathfile+"fig-01-predicted-calib.csv"). \
            set_predicted_validation(pathfile+"fig-01-predicted-valid.csv"). \
            set_error_calibration(pathfile+"fig-01-error-calib.csv"). \
            set_error_validation(pathfile+"fig-01-error-valid.csv")            
        return config
    

class Figure02():

    def add_urls(self, config):
        pathfile = coen.get_output_location()
        config["locator"] = coio.FileResources(). \
            set_measured_calibration(pathfile+"fig-02-measured-calib.csv"). \
            set_measured_validation(pathfile+"fig-02-measured-valid.csv"). \
            set_predicted_calibration(pathfile+"fig-02-predicted-calib.csv"). \
            set_predicted_validation(pathfile+"fig-02-predicted-valid.csv"). \
            set_error_calibration(pathfile+"fig-02-error-calib.csv"). \
            set_error_validation(pathfile+"fig-02-error-valid.csv")            
        return config