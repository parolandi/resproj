
import unittest

import data.data_splicing
import experiments.experiment


'''
Examine the effect of changing the number of data points between
20, 30 and 40 points with the same data splicing pattern 111000
using CG
'''
class TestExperiment03(unittest.TestCase):


    number_of_intervals = 30
    CG_method = "key-CG"


    def test_do_experiment_at_conditions_110110_and_30_points_with_CG(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_110110
        config["algorithm_setting"] = self.CG_method
        config["number_of_intervals"] = self.number_of_intervals
        _ = None
        experiments.experiment.do_experiment(self, config, _)

    
    def test_do_experiment_at_conditions_101101_and_30_points_with_CG(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_101101
        config["algorithm_setting"] = self.CG_method
        config["number_of_intervals"] = self.number_of_intervals
        _ = None
        experiments.experiment.do_experiment(self, config, _)

    
    def test_do_experiment_at_conditions_011011_and_30_points_with_CG(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_011011
        config["algorithm_setting"] = self.CG_method
        config["number_of_intervals"] = self.number_of_intervals
        _ = None
        experiments.experiment.do_experiment(self, config, _)

    
if __name__ == "__main__":
    unittest.main()
