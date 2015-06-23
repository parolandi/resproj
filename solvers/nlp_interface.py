
import models.model_data as momoda
import solvers.least_squares as solesq
import solvers.monte_carlo_multiple_least_squares as somcmlesq


def solve(model, problem, algorithm):
    """
    Solve nonlinear programming problem for generic (local, global) solver settings
    algorithm: solver settings
    returns: models.model_data.NumericResult
    """
    if algorithm["class"] == solesq.solve:
        point = solesq.solve(model, problem, algorithm)
    elif algorithm["class"] == somcmlesq.solve:
        result = somcmlesq.solve(model, problem, algorithm)
        data = {}
        data["status"] = 0
        # TEST: 2015-06-23
        if len(result["decision_variables"]) == 0:
            data["status"] = 1
        data["x"] = result["decision_variables"]
        point = momoda.NumericResult(data)
    else:
        raise
    return point