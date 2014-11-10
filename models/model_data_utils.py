
import copy


'''
Set model's and problem's parameters to the values given
values:       list
model_data:   models.model_data.model_structure
problem_data: models.model_data.problem.problem_structure
'''
def apply_values_to_parameters(values, model_data, problem_data):
    if problem_data is not None:
        problem_data["parameters"] = copy.deepcopy(values)
    
    if model_data is not None:
        assert(problem_data is not None)
        for ii in range(len(problem_data["parameter_indices"])):
            model_data["parameters"][problem_data["parameter_indices"][ii]] = \
                copy.deepcopy(values[ii])


'''
Set model's and problem's parameters to the values given by the decision variables
opt_sol:      models.model_data.optimisation_problem_solution
model_data:   models.model_data.model_structure
problem_data: models.model_data.problem.problem_structure
'''
def apply_decision_variables_to_parameters(opt_sol, model_data, problem_data):
    apply_values_to_parameters(opt_sol["decision_variables"], model_data, problem_data)
