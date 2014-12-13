
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
    print(sbpr["ssr_test"])
    print("* Chi-squared test contributions *")
    for ii in range(len(sbpr["ssrs_tests"])):
        print(sbpr["ssrs_tests"][ii])


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
    print("* Standard deviation *")
    print(sbpr["est_stdev"])
    print("* Ellipsoid radius *")
    print(sbpr["ell_radius"])
    print("* Confidence intervals *")
    for ii in range(len(sbpr["conf_intvs"])):
        print(sbpr["conf_intvs"][ii])
