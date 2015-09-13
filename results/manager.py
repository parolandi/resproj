
import common.environment as coen
import common.diagnostics as codi
import common.io as coio

# TODO: it may pay off to add a level of indirection and call formatter before writing

def get_sys_filepathname():
    return coen.get_results_location() + coen.get_calibvalid_system_file_name()


def get_sen_filepathname():
    return coen.get_results_location() + coen.get_calibvalid_sensitivity_file_name()


def report_nonlinear_confidence_region_intervals_and_points(intervals, points):
    """
    intervals list of list?   
    points    models.model_data.optimisation_problem_point
    """
    resfile = \
        coen.get_results_location() + coen.get_nonlinconfreg_intervals_and_points_file_name()
    coio.write_to_csv(intervals, resfile)
    coio.write_to_csv(points["decision_variables"], resfile)
    coio.write_to_csv(points["objective_function"], resfile)
    

def report_system_based_point_results(sbpr):
    """
    sbpr: workflows.workflow_data.system_based_point_results
    Warning: could this method possibly have a side effect on unit-testing?
    """
    f = open(get_sys_filepathname(), 'a')
    f.write("* Parameters *\n")
    for ii in range(len(sbpr["params"])):
        f.write(str(sbpr["params"][ii])+"\n")
    f.write("* SSR *\n")
    f.write(str(sbpr["ssr"])+"\n")
    f.write("* SSR contributions *\n")
    for ii in range(len(sbpr["ssrs"])):
        f.write(str(sbpr["ssrs"][ii])+"\n")
    # TODO: ress_vals
    f.write("* Chi-squared test *\n")
    f.write( \
        str(sbpr["ssr_test"]) + " " + \
        str(sbpr["ssr_thresh_lb"]) + " " + \
        str(sbpr["ssr"]) + " " + \
        str(sbpr["ssr_thresh_ub"])+"\n")
    f.write("* Chi-squared test contributions *\n")
    for ii in range(len(sbpr["ssrs_tests"])):
        pass
        #print(sbpr["ssrs_tests"][ii], sbpr["ssrs_thresh_lb"][ii], sbpr["ssrs"][ii], sbpr["ssrs_thresh_ub"][ii])


def report_sensitivity_based_point_results(sbpr):
    """
    sbpr: workflows.workflow_data.sensitivity_based_point_results
    """
    f = open(get_sen_filepathname(), 'a')
    f.write("* Parameters *\n")
    for ii in range(len(sbpr["params"])):
        f.write(str(sbpr["params"][ii])+"\n")
    f.write("* Covariance matrix *\n")
    for ii in range(len(sbpr["cov_matrix"])):
        for jj in range(len(sbpr["cov_matrix"][ii])):
            f.write(str(sbpr["cov_matrix"][ii][jj]) + " ")
        f.write("\n")
    f.write("* Covariance matrix determinant*\n")
    f.write(str(sbpr["cov_det"])+"\n")
    f.write("* Estimated variance *\n")
    f.write(str(sbpr["est_var"])+"\n")
    f.write("* Ellipsoid radius *\n")
    f.write(str(sbpr["ell_radius"])+"\n")
    f.write("* Confidence intervals *\n")
    for ii in range(len(sbpr["conf_intvs"])):
        f.write(str(sbpr["conf_intvs"][ii]))
        f.write("\n")
    f.write("* Correlation matrix *\n")
    for ii in range(len(sbpr["corr_matrix"])):
        for jj in range(len(sbpr["corr_matrix"][ii])):
            f.write(str(sbpr["corr_matrix"][ii][jj]) + " ") 
        f.write("\n")   
    f.write("* Correlation matrix determinant*\n")
    f.write(str(sbpr["corr_det"])+"\n")


def report_decision_variables_and_objective_function(point):
    """
    point: models.model_data.optimisation_problem_point
    """
    fsys = open(get_sys_filepathname(), 'a')
    fsen = open(get_sen_filepathname(), 'a')
    dvs = "decision variables: \n" + str(point["decision_variables"]) + "\n"
    obj = "objective function: \n" + str(point["objective_function"]) + "\n"
    fsys.write(dvs)
    fsys.write(obj)
    fsen.write(dvs)
    fsen.write(obj)
    
    
def report_date_and_time():
    fsys = open(get_sys_filepathname(), 'a')
    fsen = open(get_sen_filepathname(), 'a')
    dnt = codi.get_date_and_time() + "\n"
    fsys.write(dnt)
    fsen.write(dnt)