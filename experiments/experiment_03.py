
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


class TestExperiment03(unittest.TestCase):


    def test_do_experiment_at_conditions_110110_and_30_points_with_CG(self):
        config = dict(self.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_110110
        config["algorithm_setting"] = "key-CG"
        config["number_of_intervals"] = 30
        _ = None
        self.do_experiment(config, _)

    
    def test_do_experiment_at_conditions_101101_and_30_points_with_CG(self):
        config = dict(self.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_101101
        config["algorithm_setting"] = "key-CG"
        config["number_of_intervals"] = 30
        _ = None
        self.do_experiment(config, _)

    
    def test_do_experiment_at_conditions_011011_and_30_points_with_CG(self):
        config = dict(self.experiment_setup)
        config["data_splicing"] = data.data_splicing.splice_data_with_pattern_011011
        config["algorithm_setting"] = "key-CG"
        config["number_of_intervals"] = 30
        _ = None
        self.do_experiment(config, _)

    
    experiment_setup = {
        "number_of_intervals": 0,
        "data_splicing": None,
        "algorithm_setting": "",
    }

    
    def do_setup(self, config):
        # configuration
        final_time = 3.0
        intervals = config["number_of_intervals"]
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
            stdev, act_meas_traj, exp_meas_traj, meas_noise_traj = self.do_setup(config)
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
        
#        self.do_test_point(point_results, baseline["full"])

        fig = solvers.plot.get_figure()

        path_results = workflows.basic.do_workflow_at_solution_path( \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance, \
                stdev, solution_path, fig)

#        self.do_test_path(path_results, baseline["full"])

        all_results = dict(workflows.workflow_data.workflow_results)
        all_results["full"] = path_results

        dataset = config["data_splicing"](problem_instance["time"], exp_meas_traj, meas_noise_traj, act_meas_traj)
#        id = dataset["id"]
#        dataset["id"] = id + "-n-" + str(config["number_of_intervals"])
    
        # calibration data set
        # least-squares
        model_instance, problem_instance, sens_model_instance, sens_problem_instance, \
            stdev, act_meas_traj, exp_meas_traj, meas_noise_traj = self.do_setup(config)

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

#        self.do_test_point(point_results, baseline["calibration"])
        
        path_results = workflows.basic.do_workflow_at_solution_path( \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance, \
                stdev, solution_path, fig)

#        self.do_test_path(path_results, baseline["calibration"])

        all_results["calibration"] = path_results
        
        # validation data set
        problem_instance["outputs"] = dataset["valid"]["meas"]
        problem_instance["time"] = dataset["valid"]["time"]

        point_results = workflows.basic.do_workflow_at_solution_point( \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance, \
                stdev, problem_instance["outputs"], dataset["valid"]["true"])
        point_results["params"] = copy.deepcopy(result.x)

#        self.do_test_point(point_results, baseline["validation"])
        
        path_results = workflows.basic.do_workflow_at_solution_path( \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance, \
                stdev, solution_path, fig)

#        self.do_test_path(path_results, baseline["validation"])

        all_results["validation"] = path_results
                
        # validation and calibration data sets
        problem_instance["outputs"] = exp_meas_traj
        problem_instance["time"] = full_time

        point_results = workflows.basic.do_workflow_at_solution_point( \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance, \
                stdev, problem_instance["outputs"], act_meas_traj)
        point_results["params"] = copy.deepcopy(result.x)

#        self.do_test_point(point_results, baseline["calib+valid"])
        
        path_results = workflows.basic.do_workflow_at_solution_path( \
                models.ordinary_differential.linear_2p2s, model_instance, problem_instance, \
                models.ordinary_differential.sensitivities_linear_2p2s, sens_model_instance, sens_problem_instance, \
                stdev, solution_path, fig)

#        self.do_test_path(path_results, baseline["calib+valid"])

        all_results["calib+valid"] = path_results

        # results
        if do_results:
            fig.suptitle("Dataset" + dataset["id"] + "-s-" + slv_method)
            solvers.plot.show_figure()
        print(slv_method)
        print(dataset["id"])
        results.report_workflows.report_results(all_results)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()