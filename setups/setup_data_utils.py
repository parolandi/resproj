
def apply_config(config):
    """Legacy"""
    model_instance = config["model_setup"]()
    data_instance = config["data_setup"]()
    problem_instance  = config["problem_setup"](model_instance, data_instance["calib"])
    protocol = config["protocol_setup"]()
    return model_instance, data_instance, problem_instance, protocol


def get_model_data_problem_protocol_with_calib(config):
    """
    Produce data that results from config values with *calib*
    return:
        model_instance
        data_instance
        problem_instance
        protocol
    """
    return apply_config(config)


def get_model_data_problem_algorithm_with_calib(config):
    """
    Produce data that result from config values with *calib*
    return:
        model_instance
        data_instance
        problem_instance
        algorithm_instance
    """
    model, data, problem, _ = apply_config(config)
    _, _, algorithm = get_model_problem_algorithm_with_calib(config)
    return model, data, problem, algorithm


def get_model_problem_algorithm_with_calib(config):
    """
    Produce data that result from config values with *calib*
    returns
        model_structure
        problem_structure
        algorithm
    """
    model_instance = config["model_setup"]()
    data_instance = config["data_setup"]()
    problem_instance  = config["problem_setup"](model_instance, data_instance["calib"])
    algorithm = config["algorithm_setup"](None)
    return model_instance, problem_instance, algorithm


def get_model_problem_protocol_and_step(config):
    protocol = config["protocol_setup"]()
    model = config["model_setup"]()
    data = config["data_setup"]()
    protocol_step = get_next_protocol_step(config)
    problem = config["problem_setup"](model, data[protocol_step])
    return model, problem, protocol, protocol_step


def get_next_protocol_step(config):
    step = ""
    if config["protocol_step"]["calib"] == "do":
        step = "calib"
    elif config["protocol_step"]["valid"] == "do":
        step = "valid"
    return step


def set_next_protocol_step(config):
    if config["protocol_step"]["calib"] == "do":
        config["protocol_step"]["calib"] = "done"
    elif config["protocol_step"]["valid"] == "do":
        config["protocol_step"]["valid"] = "done"
