
import common.environment as coen
import common.io as coio


# TODO: it may pay off to call formatter before writing
def report_nonlinear_confidence_region_intervals_and_points(intervals, points):
    resfile = \
        coen.get_results_location() + coen.get_nonlinconfreg_intervals_and_points_file_name()
    coio.write_to_csv(intervals, resfile)
    coio.write_to_csv(points["decision_variables"], resfile)
    coio.write_to_csv(points["objective_function"], resfile)