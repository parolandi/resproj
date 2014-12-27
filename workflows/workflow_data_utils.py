
def print_system_based_point_results(sbpr):
    """
    sbpr: workflows.workflow_data.system_based_point_results
    Warning: could this method possibly have a side effect on unit-testing?
    """
    print("* Parameters *")
    for ii in range(len(sbpr["params"])):
        print(sbpr["params"][ii])
    print("* SSR *")
    print(sbpr["ssr"])
    print("* SSR contributions *")
    for ii in range(len(sbpr["ssrs"])):
        print(sbpr["ssrs"][ii])
    # TODO: ress_vals
    print("* Chi-squared test *")
    print(sbpr["ssr_test"], sbpr["ssr_thresh_lb"], sbpr["ssr"], sbpr["ssr_thresh_ub"])
    print("* Chi-squared test contributions *")
    for ii in range(len(sbpr["ssrs_tests"])):
        print(sbpr["ssrs_tests"][ii], sbpr["ssrs_thresh_lb"][ii], sbpr["ssrs"][ii], sbpr["ssrs_thresh_ub"][ii])


def print_sensitivity_based_point_results(sbpr):
    """
    sbpr: workflows.workflow_data.sensitivity_based_point_results
    """
    print("* Parameters *")
    for ii in range(len(sbpr["params"])):
        print(sbpr["params"][ii])
    print("* Covariance matrix *")
    for ii in range(len(sbpr["cov_matrix"])):
        for jj in range(len(sbpr["cov_matrix"][ii])):
            print(sbpr["cov_matrix"][ii][jj])    
    print("* Covariance matrix determinant*")
    print(sbpr["cov_det"])
    print("* Standard deviation *")
    print(sbpr["est_stdev"])
    print("* Ellipsoid radius *")
    print(sbpr["ell_radius"])
    print("* Confidence intervals *")
    for ii in range(len(sbpr["conf_intvs"])):
        print(sbpr["conf_intvs"][ii])
    print("* Correlation matrix *")
    for ii in range(len(sbpr["corr_matrix"])):
        for jj in range(len(sbpr["corr_matrix"][ii])):
            print(sbpr["corr_matrix"][ii][jj])    
    print("* Correlation matrix determinant*")
    print(sbpr["corr_det"])
