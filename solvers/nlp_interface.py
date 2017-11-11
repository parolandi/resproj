
import models.model_data as momoda
import solvers.least_squares as solesq
import solvers.monte_carlo_multiple_least_squares as somcmlesq

import logging


def solve_unlegacy(model, problem, algorithm):
    """
    Solve nonlinear programming problem for generic (local, global) solver settings
    algorithm: solver settings
    returns: models.model_data.NumericResult
    """
    logging.debug("solvers.nlp_interface")
    if algorithm["call"] == solesq.solve:
        point = solesq.solve(model, problem, algorithm)
    elif algorithm["call"] == somcmlesq.solve:
        result = somcmlesq.solve(model, problem, algorithm)
        data = {}
        data["status"] = 0
        data["x"] = result["decision_variables"]
        # TEST: 2015-06-23
        if len(result["decision_variables"]) == 0:
            data["status"] = 1
            # WIP 2015-07-12; this doesn't work
            data["x"] = algorithm["initial_guesses"]
        point = momoda.NumericResult(data)
    else:
        raise
    logging.info("NLP point: " + str(point))
    return point


def solve(model, problem, algorithm):
    """
    Solve nonlinear programming problem for generic (local, global) solver settings
    algorithm: solver settings
    returns: models.model_data.NumericResult
    """
    logging.debug("solvers.nlp_interface")
    if algorithm["class"] == solesq.solve:
        point = solesq.solve(model, problem, algorithm)
    elif algorithm["class"] == somcmlesq.solve:
        result = somcmlesq.solve(model, problem, algorithm)
        data = {}
        data["status"] = 0
        data["x"] = result["decision_variables"]
        # TEST: 2015-06-23
        if len(result["decision_variables"]) == 0:
            data["status"] = 1
            # WIP 2015-07-12; this doesn't work
            data["x"] = algorithm["initial_guesses"]
        point = momoda.NumericResult(data)
    else:
        raise
    logging.info("NLP point: " + str(point))
    return point