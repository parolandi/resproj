
import unittest


import data.data_splicing
import experiments.experiment


number_of_intervals = 30
CG_method = "key-CG"


class TestExperiment03(unittest.TestCase):


    def test_do_experiment_at_conditions_110110_and_30_points_with_CG(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_110110
        config["algorithm_setting"] = "key-CG"
        config["number_of_intervals"] = 30
        _ = None
        experiments.experiment.do_experiment(self, config, _)

    
    def test_do_experiment_at_conditions_101101_and_30_points_with_CG(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_101101
        config["algorithm_setting"] = "key-CG"
        config["number_of_intervals"] = 30
        _ = None
        experiments.experiment.do_experiment(self, config, _)

    
    def test_do_experiment_at_conditions_011011_and_30_points_with_CG(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_011011
        config["algorithm_setting"] = "key-CG"
        config["number_of_intervals"] = 30
        _ = None
        experiments.experiment.do_experiment(self, config, _)

    
if __name__ == "__main__":
    unittest.main()