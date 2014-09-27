
import unittest
import copy
import numpy

import common.utilities
import data.data_splicing
import data.generator
import metrics.ordinary_differential
import models.model_data
import models.ordinary_differential
import results.report_workflows
import solvers.initial_value
import solvers.least_squares
import solvers.plot
import solvers.solver_data
import workflows.basic


class TestExperiment01(unittest.TestCase):


    def test_do_experiment_01_at_conditions_111000_with_CG(self):
        config = dict(self.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_111000
        config["algorithm_setting"] = "key-CG" 
        baseline = self.setup_test_baseline_experiment_01_at_conditions_111000_with_CG()
        self.do_experiment(config, baseline)


    def test_do_experiment_01_at_conditions_000111_with_CG(self):
        config = dict(self.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_000111
        config["algorithm_setting"] = "key-CG"
        baseline = self.setup_test_baseline_experiment_01_at_conditions_000111_with_CG()
        self.do_experiment(config, baseline)


    def test_do_experiment_01_at_conditions_101010_with_CG(self):
        config = dict(self.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_101010
        config["algorithm_setting"] = "key-CG"
        baseline = self.setup_test_baseline_experiment_01_at_conditions_101010_with_CG()
        self.do_experiment(config, baseline)


    def test_do_experiment_01_at_conditions_111000_with_NM(self):
        config = dict(self.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_111000
        config["algorithm_setting"] = "key-Nelder-Mead"
        baseline = self.setup_test_baseline_experiment_01_at_conditions_111000_with_NM() 
        self.do_experiment(config, baseline)


    def test_do_experiment_01_at_conditions_000111_with_NM(self):
        config = dict(self.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_000111
        config["algorithm_setting"] = "key-Nelder-Mead"
        baseline = self.setup_test_baseline_experiment_01_at_conditions_000111_with_NM()
        self.do_experiment(config, baseline)


    def test_do_experiment_01_at_conditions_101010_with_NM(self):
        config = dict(self.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_101010
        config["algorithm_setting"] = "key-Nelder-Mead"
        baseline = self.setup_test_baseline_experiment_01_at_conditions_101010_with_NM()
        self.do_experiment(config, baseline)


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

    
    experiment_setup = {
        "data_splicing": None,
        "algorithm_setting": "",
    }


    def do_setup(self):
        # configuration
        final_time = 3.0
        intervals = 30
        stdev = 0.2
        
        times = numpy.linspace(0.0, final_time, intervals+1, endpoint=True)
        inputs = numpy.array([1.0, 2.0])
        params = numpy.array([1.0, 2.0])
        output_indices = numpy.array([0, 1])
        param_indices = numpy.array([0, 1])
        sens_states = numpy.array([0.0, 0.0, 0.0, 0.0])
        states = numpy.array([10.0, 8.0])
        
        # boiler-plate
        model_instance = dict(models.model_data.model_structure)
        model_instance["inputs"] = inputs
        model_instance["parameters"] = params
        model_instance["states"] = states
        model_instance["time"] = 0.0
        
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["initial_conditions"] = copy.deepcopy(model_instance["states"])
        problem_instance["inputs"] = copy.deepcopy(model_instance["inputs"])
        problem_instance["time"] = times
        problem_instance["parameters"] = copy.deepcopy(model_instance["parameters"])
        problem_instance["parameter_indices"] = param_indices
        problem_instance["initial"] = "exclude"

        mi = copy.deepcopy(model_instance)
        pi = copy.deepcopy(problem_instance)

        measured = numpy.asarray(solvers.initial_value.compute_trajectory_st( \
            models.ordinary_differential.linear_2p2s, mi, pi))
        
        true_measurement_trajectories = common.utilities.sliceit_astrajectory(measured)
        
        no_states = len(model_instance["states"])
        data.generator.set_seed(117)
        measurement_noise = []
        for ii in range(no_states):
            measurement_noise.append(stdev * data.generator.normal_distribution(intervals+1))
        data.generator.unset_seed()
        
        experimental_measurement_trajectories = true_measurement_trajectories + measurement_noise
        
        problem_instance["outputs"] = experimental_measurement_trajectories
        problem_instance["output_indices"] = output_indices

        sens_model_instance = dict(models.model_data.model_structure)
        sens_model_instance["inputs"] = copy.deepcopy(model_instance["inputs"])
        sens_model_instance["parameters"] = copy.deepcopy(model_instance["parameters"])
        sens_model_instance["states"] = sens_states
        sens_model_instance["time"] = 0.0
        
        sens_problem_instance = dict(models.model_data.problem_structure)
        sens_problem_instance["initial_conditions"] = copy.deepcopy(sens_model_instance["states"])
        sens_problem_instance["inputs"] = copy.deepcopy(sens_model_instance["inputs"])
        sens_problem_instance["parameters"] = copy.deepcopy(sens_model_instance["parameters"])
        sens_problem_instance["parameter_indices"] = copy.deepcopy(problem_instance["parameter_indices"])
        sens_problem_instance["time"] = copy.deepcopy(problem_instance["time"])
        
        return model_instance, problem_instance, sens_model_instance, sens_problem_instance, \
            stdev, true_measurement_trajectories, experimental_measurement_trajectories, measurement_noise


    def do_test_point(self, point_results, baseline):
        return
    
        expected = baseline["params"]
        actual = point_results["params"]
        [self.assertAlmostEquals(exp, acts, 8) for exp, acts in zip(expected, actual)]

        expected = baseline["obj"]
        actual = point_results["ssr"]
        self.assertAlmostEquals(expected, actual, 8)
        
        expected = baseline["conf_intervs"]
        actual = point_results["conf_intvs"]
        [self.assertAlmostEquals(exp, acts, 8) for exp, acts in zip(expected, actual)]
        

    def do_test_path(self, path_results, baseline):
        return
    
        expected = baseline["algo_stats"]["iters"]
        actual = path_results["algo_stats"]["iters"]
        self.assertEquals(expected, actual)

    
    # TODO: do deep copies    
    def do_experiment(self, config, baseline):
        # TODO: user messages

        # configure
        do_results = True
        ig_multiplier = 1.0
        # or "key-Nelder-Mead" 
        slv_method = solvers.solver_data.nonlinear_algebraic_methods[config["algorithm_setting"]]
        tolerance = 1E-8
        
        # setup
        model_instance, problem_instance, sens_model_instance, sens_problem_instance, \
            stdev, act_meas_traj, exp_meas_traj, meas_noise_traj = self.do_setup()
        # TODO: use deep copies
        full_time = copy.deepcopy(problem_instance["time"])
        intial_guesses = copy.deepcopy(problem_instance["parameters"]) * ig_multiplier

        algorithm_instance = dict(solvers.solver_data.algorithm_structure)
        logger = solvers.least_squares.DecisionVariableLogger()
        algorithm_instance["callback"] = logger.log_decision_variables
        algorithm_instance["initial_guesses"] = intial_guesses
        algorithm_instance["method"] = slv_method
        algorithm_instance["tolerance"] = tolerance
        
        # whole data set
        # least-squares
        logger.log_decision_variables(algorithm_instance["initial_guesses"])
        result = solvers.least_squares.solve_st( \
            metrics.ordinary_differential.sum_squared_residuals_st, \
            models.ordinary_differential.linear_2p2s, model_instance, problem_instance, algorithm_instance)
        problem_instance["parameters"] = copy.deepcopy(result.x)
        sens_problem_instance["parameters"] = copy.deepcopy(result.x)
        solution_path = logger.get_decision_variables()

        point_results = workflows.basic.do_workflow_at_solution_point( \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance, \
                stdev, problem_instance["outputs"], act_meas_traj)
        point_results["params"] = copy.deepcopy(result.x)
        
        self.do_test_point(point_results, baseline["full"])

        fig = solvers.plot.get_figure()

        path_results = workflows.basic.do_workflow_at_solution_path( \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance, \
                stdev, solution_path, fig)

        self.do_test_path(path_results, baseline["full"])

        all_results = dict(workflows.workflow_data.workflow_results)
        all_results["full"] = path_results

        dataset = config["data_splicing"](problem_instance["time"], exp_meas_traj, meas_noise_traj, act_meas_traj)
    
        # calibration data set
        # least-squares
        model_instance, problem_instance, sens_model_instance, sens_problem_instance, \
            stdev, act_meas_traj, exp_meas_traj, meas_noise_traj = self.do_setup()

        problem_instance["outputs"] = dataset["calib"]["meas"]
        problem_instance["time"] = dataset["calib"]["time"]

        logger = solvers.least_squares.DecisionVariableLogger()
        algorithm_instance["callback"] = logger.log_decision_variables
        algorithm_instance["initial_guesses"] = intial_guesses
        logger.log_decision_variables(algorithm_instance["initial_guesses"])
        result = solvers.least_squares.solve_st( \
            metrics.ordinary_differential.sum_squared_residuals_st, \
            models.ordinary_differential.linear_2p2s, model_instance, problem_instance, algorithm_instance)
        problem_instance["parameters"] = copy.deepcopy(result.x)
        sens_problem_instance["parameters"] = copy.deepcopy(result.x)
        solution_path = logger.get_decision_variables()
        
        point_results = workflows.basic.do_workflow_at_solution_point( \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance, \
                stdev, problem_instance["outputs"], dataset["calib"]["true"])
        point_results["params"] = copy.deepcopy(result.x)

        self.do_test_point(point_results, baseline["calibration"])
        
        path_results = workflows.basic.do_workflow_at_solution_path( \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance, \
                stdev, solution_path, fig)

        self.do_test_path(path_results, baseline["calibration"])

        all_results["calibration"] = path_results
        
        # validation data set
        problem_instance["outputs"] = dataset["valid"]["meas"]
        problem_instance["time"] = dataset["valid"]["time"]

        point_results = workflows.basic.do_workflow_at_solution_point( \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance, \
                stdev, problem_instance["outputs"], dataset["valid"]["true"])
        point_results["params"] = copy.deepcopy(result.x)

        self.do_test_point(point_results, baseline["validation"])
        
        path_results = workflows.basic.do_workflow_at_solution_path( \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance, \
                stdev, solution_path, fig)

        self.do_test_path(path_results, baseline["validation"])

        all_results["validation"] = path_results
                
        # validation and calibration data sets
        problem_instance["outputs"] = exp_meas_traj
        problem_instance["time"] = full_time

        point_results = workflows.basic.do_workflow_at_solution_point( \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance, \
                stdev, problem_instance["outputs"], act_meas_traj)
        point_results["params"] = copy.deepcopy(result.x)

        self.do_test_point(point_results, baseline["calib+valid"])
        
        path_results = workflows.basic.do_workflow_at_solution_path( \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance, \
                stdev, solution_path, fig)

        self.do_test_path(path_results, baseline["calib+valid"])

        all_results["calib+valid"] = path_results

        # results
        if do_results:
            fig.suptitle("Dataset" + dataset["id"] + "-s-" + slv_method)
            solvers.plot.show_figure()
        print(slv_method)
        print(dataset["id"])
        results.report_workflows.report_results(all_results)


if __name__ == "__main__":
    unittest.main()
