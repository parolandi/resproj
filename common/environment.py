def get_doing_quick_tests_only():
    return False


def get_doing_plotting():
    return False


def get_results_location():
    return "C:/Users/mamuts/Desktop/"


def get_objective_function_and_decision_variables_file_name():
    return "hpnts.csv"


def get_nonlinconfreg_intervals_and_points_file_name():
    return "resncriap.csv"


def get_experimental_data_location():
    return "C:/workspace/resproj/experiments/"


def get_experimental_data_0_20_file_name():
    return "data_time_0_20.txt"


def get_experimental_data_0_60_file_name():
    return "data_time_0_60.txt"


def get_experimental_data_file_0_20():
    return get_experimental_data_location() + get_experimental_data_0_20_file_name()


def get_experimental_data_file_0_60():
    return get_experimental_data_location() + get_experimental_data_0_60_file_name()


def get_calibvalid_system_file_name():
    return "syspnt.txt"


def get_calibvalid_sensitivity_file_name():
    return "senpnt.txt"