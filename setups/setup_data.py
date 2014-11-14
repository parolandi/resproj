

'''
logger: solvers.least_squares.DecisionVariableLogger()
'''
instrumentation_data = {
    "logger": None,
    }


'''
number_of_intervals: int
data_splicing: function
algorithm_setting: str
model_setup: function
problem_setup: function
sensitivity_model_setup: function
sensitivity_problem_setup: function
algorithm_setup: function
instrumentation_setup: function
data_setup: function
'''
experiment_setup = {
    "model_setup": None,
    "problem_setup": None,
    "sensitivity_model_setup": None,
    "sensitivity_problem_setup": None,
    "algorithm_setup": None,
    "instrumentation_setup": None,
    "protocol_setup": None,
    "data_setup": None,
# kind of legacy
    "number_of_intervals": 0,
    "data_splicing": None,
    "algorithm_setting": "",
}
