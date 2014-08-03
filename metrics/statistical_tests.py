
import scipy.stats

# TODO: unencrypt these user messages
user_messages = {
    "one_sided_chi_squared_test_pass_oneliner": "OK! RMS is less than CHI2 value (this is a one-sided test; two-sided test recommended)",
    "one_sided_chi_squared_test_pass_description": "blah, blah",
    "one_sided_chi_squared_test_fail_oneliner": "OOPS! RMS greater than CHI2 value (this is a one-sided test; two-sided test recommended)",
    "one_sided_chi_squared_test_fail_description": "blah, blah",
    "two_sided_chi_squared_test_pass_oneliner": "OK! RMS is within CHI2 values (this is the recommended two-sided test)",
    "two_sided_chi_squared_test_pass_description": "blah, blah",
    "two_sided_chi_squared_test_fail_oneliner": "OOPS! RMS not within CHI2 values (this is the recommended two-sided test)",
    "two_sided_chi_squared_test_fail_lower_oneliner": "OOPS! Too small RMS",
    "two_sided_chi_squared_test_fail_upper_oneliner": "OOPS! Too large RMS",
    "two_sided_chi_squared_test_fail_description": "blah, blah",
    }

# TODO: validation of user input

# the significance is one sided, naturally
def calculate_one_sided_chi_squared_test_for_mean_sum_squared_residuals(rms, dof, significance):
    chi_squared_value = scipy.stats.chi2.isf(significance, dof)
    if rms < chi_squared_value:
        print(user_messages["one_sided_chi_squared_test_pass_oneliner"])
        print(user_messages["one_sided_chi_squared_test_pass_description"])
        return True
    else:
        print(user_messages["one_sided_chi_squared_test_fail_oneliner"])
        print(user_messages["one_sided_chi_squared_test_fail_description"])
        return False


# the significance is joint two sided
def calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals(rms, dof, significance):
    q = (1-significance)/2
    chi_squared_value_lower = scipy.stats.chi2.ppf(q, dof)
    chi_squared_value_upper = scipy.stats.chi2.isf(q, dof)
    print(chi_squared_value_lower, chi_squared_value_upper)
    if rms > chi_squared_value_lower and rms < chi_squared_value_upper:
        print(user_messages["two_sided_chi_squared_test_pass_oneliner"])
        print(user_messages["two_sided_chi_squared_test_pass_description"])
        return True
    else:
        print(user_messages["two_sided_chi_squared_test_fail_oneliner"])
        if rms <= chi_squared_value_lower:
            print(user_messages["two_sided_chi_squared_test_fail_lower_oneliner"])
        if rms >= chi_squared_value_upper:
            print(user_messages["two_sided_chi_squared_test_fail_upper_oneliner"])
        return False
