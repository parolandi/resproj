
import unittest

import copy

import data.data_splicing
import experiments.experiment
import workflows.workflow_data


'''
Examine the effect of changing the data splicing pattern between
different interpolation and extrapolation "extremes", using 30 points
and both CG and NM methods
'''
class TestExperiment01(unittest.TestCase):


    number_of_intervals = 30
    NM_method = "key-Nelder-Mead"
    CG_method = "key-CG"

    def test_do_experiment_01_at_conditions_111000_with_CG(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_111000
        config["algorithm_setting"] = self.CG_method 
        config["number_of_intervals"] = self.number_of_intervals
        baseline = self.setup_test_baseline_experiment_01_at_conditions_111000_with_CG()
        experiments.experiment.do_experiment(self, config, baseline)

    
    def test_do_experiment_01_at_conditions_000111_with_CG(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_000111
        config["algorithm_setting"] = self.CG_method
        config["number_of_intervals"] = self.number_of_intervals
        baseline = self.setup_test_baseline_experiment_01_at_conditions_000111_with_CG()
        experiments.experiment.do_experiment(self, config, baseline)


    def test_do_experiment_01_at_conditions_101010_with_CG(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_101010
        config["algorithm_setting"] = self.CG_method
        config["number_of_intervals"] = self.number_of_intervals
        baseline = self.setup_test_baseline_experiment_01_at_conditions_101010_with_CG()
        experiments.experiment.do_experiment(self, config, baseline)


    def test_do_experiment_01_at_conditions_111000_with_NM(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_111000
        config["algorithm_setting"] = self.NM_method
        config["number_of_intervals"] = self.number_of_intervals
        baseline = self.setup_test_baseline_experiment_01_at_conditions_111000_with_NM() 
        experiments.experiment.do_experiment(self, config, baseline)


    def test_do_experiment_01_at_conditions_000111_with_NM(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_000111
        config["algorithm_setting"] = self.NM_method
        config["number_of_intervals"] = self.number_of_intervals
        baseline = self.setup_test_baseline_experiment_01_at_conditions_000111_with_NM()
        experiments.experiment.do_experiment(self, config, baseline)


    def test_do_experiment_01_at_conditions_101010_with_NM(self):
        config = dict(experiments.experiment.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_101010
        config["algorithm_setting"] = self.NM_method
        config["number_of_intervals"] = self.number_of_intervals
        baseline = self.setup_test_baseline_experiment_01_at_conditions_101010_with_NM()
        experiments.experiment.do_experiment(self, config, baseline)


    def setup_test_baseline_experiment_01_at_conditions_111000_with_CG(self):
        baseline = copy.deepcopy(workflows.workflow_data.workflow_results)
        baseline["full"]["params"] = [1.05280058, 2.05003397]
        baseline["calibration"]["params"] = [1.01362744, 2.03093039]
        baseline["validation"]["params"] = [1.01362744, 2.03093039]
        baseline["calib+valid"]["params"] = [1.01362744, 2.03093039]
        baseline["full"]["obj"] = 1.6631843343
        baseline["calibration"]["obj"] = 1.03788036995
        baseline["validation"]["obj"] = 0.840418151025
        baseline["calib+valid"]["obj"] = 1.70969400227
        baseline["full"]["conf_intervs"] = [2.53734575e-04, 6.34336437e-05]
        baseline["calibration"]["conf_intervs"] = [0.00044277, 0.00011069]
        baseline["validation"]["conf_intervs"] = [2.51482289e-04, 6.28705722e-05]
        baseline["calib+valid"]["conf_intervs"] = [2.68123978e-04, 6.70309946e-05]
        baseline["full"]["algo_stats"]["iters"] = 4
        baseline["calibration"]["algo_stats"]["iters"] = 5
        baseline["validation"]["algo_stats"]["iters"] = 5
        baseline["calib+valid"]["algo_stats"]["iters"] = 5
        return baseline
    

    def setup_test_baseline_experiment_01_at_conditions_000111_with_CG(self):
        baseline = copy.deepcopy(workflows.workflow_data.workflow_results)
        baseline["full"]["params"] = [1.05280058, 2.05003397]
        baseline["calibration"]["params"] = [1.06600027, 2.05647111]
        baseline["validation"]["params"] = [1.06600027, 2.05647111]
        baseline["calib+valid"]["params"] = [1.06600027, 2.05647111]
        baseline["full"]["obj"] = 1.6631843343
        baseline["calibration"]["obj"] = 0.778236553861
        baseline["validation"]["obj"] = 1.05883316623
        baseline["calib+valid"]["obj"] = 1.66846517362
        baseline["full"]["conf_intervs"] = [2.53734575e-04, 6.34336437e-05]
        baseline["calibration"]["conf_intervs"] = [2.15645207e-04, 5.39113017e-05]
        baseline["validation"]["conf_intervs"] = [0.00046083, 0.00011521]
        baseline["calib+valid"]["conf_intervs"] = [2.55348417e-04, 6.38371043e-05]
        baseline["full"]["algo_stats"]["iters"] = 4
        baseline["calibration"]["algo_stats"]["iters"] = 4
        baseline["validation"]["algo_stats"]["iters"] = 4
        baseline["calib+valid"]["algo_stats"]["iters"] = 4
        return baseline


    def setup_test_baseline_experiment_01_at_conditions_101010_with_CG(self):
        baseline = copy.deepcopy(workflows.workflow_data.workflow_results)
        baseline["full"]["params"] = [1.05280058, 2.05003397]
        baseline["calibration"]["params"] = [1.08223643, 1.99708962]
        baseline["validation"]["params"] = [1.08223643, 1.99708962]
        baseline["calib+valid"]["params"] = [1.08223643, 1.99708962]
        baseline["full"]["obj"] = 1.6631843343
        baseline["calibration"]["obj"] = 0.739034729562
        baseline["validation"]["obj"] = 1.28037159968
        baseline["calib+valid"]["obj"] = 1.85080177458
        baseline["full"]["conf_intervs"] = [2.53734575e-04, 6.34336437e-05]
        baseline["calibration"]["conf_intervs"] = [2.24500192e-04, 5.61250479e-05]
        baseline["validation"]["conf_intervs"] = [0.0005837, 0.00014592]
        baseline["calib+valid"]["conf_intervs"] = [3.14209052e-04, 7.85522631e-05]
        baseline["full"]["algo_stats"]["iters"] = 4
        baseline["calibration"]["algo_stats"]["iters"] = 5
        baseline["validation"]["algo_stats"]["iters"] = 5
        baseline["calib+valid"]["algo_stats"]["iters"] = 5
        return baseline


    def setup_test_baseline_experiment_01_at_conditions_111000_with_NM(self):
        baseline = copy.deepcopy(workflows.workflow_data.workflow_results)
        baseline["full"]["params"] = [1.05280045, 2.05003397]
        baseline["calibration"]["params"] = [1.01362739, 2.03093042]
        baseline["validation"]["params"] = [1.01362739, 2.03093042]
        baseline["calib+valid"]["params"] = [1.01362739, 2.03093042]
        baseline["full"]["obj"] = 1.6631843343
        baseline["calibration"]["obj"] = 1.03788036995
        baseline["validation"]["obj"] = 0.840418133228
        baseline["calib+valid"]["obj"] = 1.70969398447
        baseline["full"]["conf_intervs"] = [2.53734575e-04, 6.34336437e-05]
        baseline["calibration"]["conf_intervs"] = [0.00044277, 0.00011069]
        baseline["validation"]["conf_intervs"] = [2.51482278e-04, 6.28705696e-05]
        baseline["calib+valid"]["conf_intervs"] = [2.68123973e-04, 6.70309932e-05]
        baseline["full"]["algo_stats"]["iters"] = 58
        baseline["calibration"]["algo_stats"]["iters"] = 50
        baseline["validation"]["algo_stats"]["iters"] = 50
        baseline["calib+valid"]["algo_stats"]["iters"] = 50
        return baseline
    

    def setup_test_baseline_experiment_01_at_conditions_000111_with_NM(self):
        baseline = copy.deepcopy(workflows.workflow_data.workflow_results)
        baseline["full"]["params"] = [1.05280045, 2.05003397]
        baseline["calibration"]["params"] = [1.06600026, 2.05647111]
        baseline["validation"]["params"] = [1.06600026, 2.05647111]
        baseline["calib+valid"]["params"] = [1.06600026, 2.05647111]
        baseline["full"]["obj"] = 1.6631843343
        baseline["calibration"]["obj"] = 0.778236553861
        baseline["validation"]["obj"] = 1.05883316523
        baseline["calib+valid"]["obj"] = 1.66846517261
        baseline["full"]["conf_intervs"] = [2.53734575e-04, 6.34336437e-05]
        baseline["calibration"]["conf_intervs"] = [2.15645207e-04, 5.39113017e-05]
        baseline["validation"]["conf_intervs"] = [0.00046083, 0.00011521]
        baseline["calib+valid"]["conf_intervs"] = [2.55348417e-04, 6.38371042e-05]
        baseline["full"]["algo_stats"]["iters"] = 58
        baseline["calibration"]["algo_stats"]["iters"] = 55
        baseline["validation"]["algo_stats"]["iters"] = 55
        baseline["calib+valid"]["algo_stats"]["iters"] = 55
        return baseline


    def setup_test_baseline_experiment_01_at_conditions_101010_with_NM(self):
        baseline = copy.deepcopy(workflows.workflow_data.workflow_results)
        baseline["full"]["params"] = [1.05280045, 2.05003397]
        baseline["calibration"]["params"] = [1.08223647, 1.99708961]
        baseline["validation"]["params"] = [1.08223647, 1.99708961]
        baseline["calib+valid"]["params"] = [1.08223647, 1.99708961]
        baseline["full"]["obj"] = 1.6631843343
        baseline["calibration"]["obj"] = 0.739034729562
        baseline["validation"]["obj"] = 1.28037170474
        baseline["calib+valid"]["obj"] = 1.85080187965
        baseline["full"]["conf_intervs"] = [2.53734575e-04, 6.34336437e-05]
        baseline["calibration"]["conf_intervs"] = [2.24500192e-04, 5.61250479e-05]
        baseline["validation"]["conf_intervs"] = [0.0005837, 0.00014592]
        baseline["calib+valid"]["conf_intervs"] = [3.14209088e-04, 7.85522720e-05]
        baseline["full"]["algo_stats"]["iters"] = 58
        baseline["calibration"]["algo_stats"]["iters"] = 53
        baseline["validation"]["algo_stats"]["iters"] = 53
        baseline["calib+valid"]["algo_stats"]["iters"] = 53
        return baseline

    
if __name__ == "__main__":
    experiments.experiment.set_showing_plots(True)
    unittest.main()
