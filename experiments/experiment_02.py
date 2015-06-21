import unittest

import logging

import common.diagnostics as codi
import data.data_splicing
import experiments.experiment


'''
Examine the effect of changing the number of data points between
20, 30 and 40 points with the same data splicing pattern 111000
using CG
'''
class TestExperiment02(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestExperiment02, self).__init__(*args, **kwargs)
        logging.basicConfig(filename=codi.get_name_logging_file(),level=codi.get_logging_level())
        logging.info("exp-02")
        logging.info(codi.get_date_and_time())


    CG_method = "key-CG"
    

    def test_do_experiment_at_conditions_111000_and_20_points_with_CG(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_111000
        config["algorithm_setting"] = self.CG_method
        config["number_of_intervals"] = 20
        _ = None
        experiments.experiment.do_experiment(self, config, _)


    def test_do_experiment_at_conditions_111000_and_30_points_with_CG(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_111000
        config["algorithm_setting"] = self.CG_method
        config["number_of_intervals"] = 30
        _ = None
        experiments.experiment.do_experiment(self, config, _)

    
    def test_do_experiment_at_conditions_111000_and_40_points_with_CG(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_111000
        config["algorithm_setting"] = self.CG_method
        config["number_of_intervals"] = 40
        _ = None
        experiments.experiment.do_experiment(self, config, _)


if __name__ == "__main__":
    unittest.main()
