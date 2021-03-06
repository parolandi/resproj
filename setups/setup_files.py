
import common.io as coio
import common.environment as coen
import output.dissertation.confidence_regions as oudicore


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
    
    
class Figure03():

    def add_urls(self, config):
        pathfile = coen.get_output_location()
        config["locator"] = coio.FileResources(). \
            set_measured_calibration(pathfile+"fig-03-measured-calib.csv"). \
            set_measured_validation(pathfile+"fig-03-measured-valid.csv"). \
            set_predicted_calibration(pathfile+"fig-03-predicted-calib.csv"). \
            set_predicted_validation(pathfile+"fig-03-predicted-valid.csv"). \
            set_error_calibration(pathfile+"fig-03-error-calib.csv"). \
            set_error_validation(pathfile+"fig-03-error-valid.csv")            
        return config
    

class Figure04():

    def add_urls(self, config):
        pathfile = coen.get_output_location()
        config["locator"] = coio.FileResources(). \
            set_measured_calibration(pathfile+"fig-04-measured-calib.csv"). \
            set_measured_validation(pathfile+"fig-04-measured-valid.csv"). \
            set_predicted_calibration(pathfile+"fig-04-predicted-calib.csv"). \
            set_predicted_validation(pathfile+"fig-04-predicted-valid.csv"). \
            set_error_calibration(pathfile+"fig-04-error-calib.csv"). \
            set_error_validation(pathfile+"fig-04-error-valid.csv")            
        return config
    

class Figure05():

    def add_urls(self, config):
        pathfile = coen.get_output_location()
        config["locator"] = coio.FileResources(). \
            set_measured_calibration(pathfile+"fig-05-measured-calib.csv"). \
            set_measured_validation(pathfile+"fig-05-measured-valid.csv"). \
            set_predicted_calibration(pathfile+"fig-05-predicted-calib.csv"). \
            set_predicted_validation(pathfile+"fig-05-predicted-valid.csv"). \
            set_error_calibration(pathfile+"fig-05-error-calib.csv"). \
            set_error_validation(pathfile+"fig-05-error-valid.csv")            
        return config
    
    
class Figure070809():
    """
    Exp-20
    """
    def add_urls(self, config):
        pathfile = coen.get_output_location()
        config["locator"] = coio.FileResources(). \
            set_multiple_realisations(pathfile+"fig-070809-ncr-points.csv"). \
            set_ellipse(oudicore.Figure06())
        return config


class Figure111213():
    """
    Exp-22
    """
    def add_urls(self, config):
        pathfile = coen.get_output_location()
        config["locator"] = coio.FileResources(). \
            set_multiple_realisations(pathfile+"fig-111213-ncr-points.csv"). \
            set_ellipse(oudicore.Figure06())
        return config


class Figure151617():
    """
    Exp-21
    """
    def add_urls(self, config):
        pathfile = coen.get_output_location()
        config["locator"] = coio.FileResources(). \
            set_multiple_realisations(pathfile+"fig-151617-ncr-points.csv"). \
            set_ellipse(oudicore.Figure06())
        return config


class Figure192021():
    """
    Exp-23
    """
    def add_urls(self, config):
        pathfile = coen.get_output_location()
        config["locator"] = coio.FileResources(). \
            set_multiple_realisations(pathfile+"fig-192021-ncr-points.csv"). \
            set_ellipse(oudicore.Figure06())
        return config


class Figure232425():
    """
    Exp-24
    """
    def add_urls(self, config):
        pathfile = coen.get_output_location()
        config["locator"] = coio.FileResources(). \
            set_multiple_realisations(pathfile+"fig-232425-ncr-points.csv"). \
            set_ellipse(oudicore.Figure06())
        return config
