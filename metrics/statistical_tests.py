
import scipy.stats

# TODO: unencrypt these user messages
user_messages = {
    "one_sided_chi_squared_test_values": "Sum of residuals value {}, chi-squared value: {}",
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
    }

# TODO: validation of user input

# the significance is one sided, naturally
# res: residual, maximum likelihood
# dof: degrees-of-freedom
# significance: probability
def calculate_one_sided_chi_squared_test_for_mean_sum_squared_residuals(res, dof, significance):
    chi_squared_value = scipy.stats.chi2.isf(significance, dof)
    print(user_messages["one_sided_chi_squared_test_values"].format(res, chi_squared_value))
    if res < chi_squared_value:
        print(user_messages["one_sided_chi_squared_test_pass_oneliner"])
        print(user_messages["one_sided_chi_squared_test_pass_description"])
        return True
    else:
        print(user_messages["one_sided_chi_squared_test_fail_oneliner"])
        print(user_messages["one_sided_chi_squared_test_fail_description"])
        return False


# res: residual, maximum likelihood
# dof: degrees-of-freedom
# significance: probability
# the significance is joint two sided
def calculate_two_sided_chi_squared_test_for_mean_sum_squared_residuals(res, dof, significance):
    q = (1-significance)/2
    chi_squared_value_lower = scipy.stats.chi2.ppf(q, dof)
    chi_squared_value_upper = scipy.stats.chi2.isf(q, dof)
    print(user_messages["two_sided_chi_squared_test_values"].format(res, chi_squared_value_lower, chi_squared_value_upper))
    if res > chi_squared_value_lower and res < chi_squared_value_upper:
        print(user_messages["two_sided_chi_squared_test_pass_oneliner"])
        print(user_messages["two_sided_chi_squared_test_pass_description"])
        return True
    else:
        print(user_messages["two_sided_chi_squared_test_fail_oneliner"])
        if res <= chi_squared_value_lower:
            print(user_messages["two_sided_chi_squared_test_fail_lower_oneliner"])
        if res >= chi_squared_value_upper:
            print(user_messages["two_sided_chi_squared_test_fail_upper_oneliner"])
        return False
