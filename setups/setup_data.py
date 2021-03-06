
'''
logger: solvers.solver_utilities.DecisionVariableLogger()
'''
instrumentation_data = {
    "logger": None,
    }


protocol_step_data = {
    "calib": ("donot", "do", "done"),
    "valid": ("donot", "do", "done"),
    }


local_data = {
    "do_plotting": True, 
    }


'''
number_of_intervals: int
data_splicing: function
algorithm_setting: str
model_setup: function
problem_setup: function
sensitivity_setup: function
sensitivity_model_setup: function
sensitivity_problem_setup: function
algorithm_setup: function
instrumentation_setup: function
data_setup: function
'''
experiment_setup = {
    "model_setup": None,
    "problem_setup": None,
    "sensitivity_setup": None,
    "sensitivity_model_setup": None,
    "sensitivity_problem_setup": None,
    "algorithm_setup": None,
    "instrumentation_setup": None,
    "protocol_setup": None,
    "protocol_step": dict(protocol_step_data),
    "data_setup": None,
# kind of legacy
    "number_of_intervals": 0,
    "data_splicing": None,
    "algorithm_setting": "",
    "local_setup": dict(local_data),
    }


# TODO: this could have a name and a sequence index
experiment_protocol = {
    # experiment_setup
    "protocol_step": [],
    }