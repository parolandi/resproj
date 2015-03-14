
'''
Produce data that result from config values
return:
    model_instance
    data_instance
    problem_instance
    protocol
'''
def apply_config(config):
    # setup
    model_instance = config["model_setup"]()
    data_instance = config["data_setup"]()
    problem_instance  = config["problem_setup"](model_instance, data_instance["calib"])
    protocol = config["protocol_setup"]()
    return model_instance, data_instance, problem_instance, protocol


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