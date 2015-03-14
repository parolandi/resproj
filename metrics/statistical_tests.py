
from __future__ import print_function
import scipy.stats

import common.exceptions
import common.utilities

# TODO: unencrypt these user messages
user_messages = {
    "one_sided_chi_squared_test_info_oneliner": "Sum of residuals value: {}; chi-squared value: {}",
    "one_sided_chi_squared_test_pass_oneliner": "OK! Sum of residuals is less than chi-squared value (this is a one-sided test; two-sided test recommended)",
    "one_sided_chi_squared_test_pass_description": "blah, blah",
    "one_sided_chi_squared_test_fail_oneliner": "OOPS! Sum of residuals greater than chi-squared value (this is a one-sided test; two-sided test recommended)",
    "one_sided_chi_squared_test_fail_description": "blah, blah",
    "two_sided_chi_squared_test_values": "Sum of residuals value {}, chi-squared values: {}, {}",
    "two_sided_chi_squared_test_pass_oneliner": "OK! Sum of residuals is within chi-squared values (this is the recommended two-sided test)",
    "two_sided_chi_squared_test_pass_description": "blah, blah",
    "two_sided_chi_squared_test_fail_oneliner": "OOPS! Sum of residuals not within chi-squared values (this is the recommended two-sided test)",
    "two_sided_chi_squared_test_fail_lower_oneliner": "OOPS! Too small sum of residuals",
    "two_sided_chi_squared_test_fail_upper_oneliner": "OOPS! Too large sum of residuals",
    "two_sided_chi_squared_test_fail_description": "blah, blah",
    "two_sided_t_student_test_info_oneliner": "Computed t-value: {}; reference t-value: {}",
    "two_sided_t_student_test_info_description": "Note that this is an approximate test!",
    "two_sided_t_student_test_pass_oneliner": "OK! Student-t value is greater than reference t-value",
    "two_sided_t_student_test_pass_description": "This means that the parameter has been estimated with sufficient statistical confidence",
    "two_sided_t_student_test_fail_oneliner": "OOPS! Student-t value is less than reference t-value",
    "two_sided_t_student_test_fail_description": "This means that the parameter has not been estimated with sufficient statistical confidence",
    }


# TODO legacy
def calculate_degrees_of_freedom(measurements, parameters_to_be_estimated):
    n = common.utilities.size_it(measurements)
    k = len(parameters_to_be_estimated)
    return n - k


def calculate_one_sided_chi_squared_value(significance, dof):
    return scipy.stats.chi2.isf(significance, dof)


def calculate_two_sided_t_student_value(significance, no_meas, no_params):
    q = (1-significance)/2
    return scipy.stats.t.isf(q, no_meas-no_params)


# the significance is one sided, naturally
# res: residual, maximum likelihood
# dof: degrees-of-freedom
# significance: probability
def calculate_one_sided_chi_squared_test_for_mean_sum_squared_residuals(res, dof, significance):
    global print_user_messages
    print_user_messages = False

    chi_squared_value = scipy.stats.chi2.isf(significance, dof)
    if print_user_messages:
        print(user_messages["one_sided_chi_squared_test_info_oneliner"].format(res, chi_squared_value))
    if res < chi_squared_value:
        if print_user_messages:
            print(user_messages["one_sided_chi_squared_test_pass_oneliner"])
            print(user_messages["one_sided_chi_squared_test_pass_description"])
        return True
    else:
        if print_user_messages:
            print(user_messages["one_sided_chi_squared_test_fail_oneliner"])
            print(user_messages["one_sided_chi_squared_test_fail_description"])
        return False


def calculate_thresholds_two_sided_chi_squared_test_for_mean_sum_squared_residuals(dof, significance):
    q = (1-significance)/2
    chi_squared_value_lower = scipy.stats.chi2.ppf(q, dof)
    chi_squared_value_upper = scipy.stats.chi2.isf(q, dof)
    return chi_squared_value_lower, chi_squared_value_upper


# res: residual, maximum likelihood
# dof: degrees-of-freedom
# significance: probability
# the significance is joint two sided
def calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals(res, dof, significance):
    global print_user_messages
    print_user_messages = False

    chi_squared_value_lower, chi_squared_value_upper = \
        calculate_thresholds_two_sided_chi_squared_test_for_mean_sum_squared_residuals(dof, significance)
    if print_user_messages:
        print(user_messages["two_sided_chi_squared_test_values"].format(res, chi_squared_value_lower, chi_squared_value_upper))
    if res > chi_squared_value_lower and res < chi_squared_value_upper:
        if print_user_messages:
            print(user_messages["two_sided_chi_squared_test_pass_oneliner"])
            print(user_messages["two_sided_chi_squared_test_pass_description"])
        return True
    else:
        if print_user_messages:
            print(user_messages["two_sided_chi_squared_test_fail_oneliner"])
        if res <= chi_squared_value_lower:
            if print_user_messages:
                print(user_messages["two_sided_chi_squared_test_fail_lower_oneliner"])
        if res >= chi_squared_value_upper:
            if print_user_messages:
                print(user_messages["two_sided_chi_squared_test_fail_upper_oneliner"])
        return False


# parameter_value, standard_error: such that t=(parameter_value-trueparameter_value)/standard_error
# dof: degrees-of-freedom
# significance: probability
# the significance is two-sided
# TODO: convenience; vectorise for all parameters
def calculate_two_sided_t_student_test_for_parameter_estimates(parameter_value, standard_error, dof, significance):
    common.exceptions.assert_throw(standard_error > 0.0)
    common.exceptions.assert_throw(parameter_value > 0.0)
    common.exceptions.assert_throw(dof > 0)
    common.exceptions.assert_throw(significance > 0.0 and significance < 1.0)

    global print_user_messages
    print_user_messages = False
    
    q = (1-significance)/2
    reference_t_stat = scipy.stats.t.isf(q, dof)
    value_t_stat = parameter_value / standard_error
    if print_user_messages:
        print(user_messages["two_sided_t_student_test_info_oneliner"].format(value_t_stat, reference_t_stat))
        print(user_messages["two_sided_t_student_test_info_description"])
    if value_t_stat > reference_t_stat:
        if print_user_messages:
            print(user_messages["two_sided_t_student_test_pass_oneliner"])
            print(user_messages["two_sided_t_student_test_pass_description"])
        return True
    else:
        if print_user_messages:
            print(user_messages["two_sided_t_student_test_fail_oneliner"])
            print(user_messages["two_sided_t_student_test_fail_description"])
        return False
