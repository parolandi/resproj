
import scipy.integrate

import copy
import logging
import numpy

import common.utilities
import common.diagnostics as cd
import models.model_data as mmd


def handle_initial_point(values, problem_instance):
    if problem_instance["initial"] == "exclude":
        values = common.utilities.exclude_initial_point(values)
    return values


# TODO: deep copy?
# TODO: instrument reporting of data
# TODO: test @ failure
def solve(model_data, problem_data):
    """
    Calls odepack.lsoda to solve the initial value problem for stiff and non-stiff ode's.
    Preconditions: at this point in time, all problem-specific stuff must have been done;
    this is a direct solver call and there is no context to do problem-specific things
    returns
        status: integer
        y:      snapshots
        data:   diagnostics
    """
    # TODO: are these assertions valid?
    assert(len(problem_data["initial_conditions"]) == len(model_data["states"]))
    assert(model_data["states"] is not None)
    # TODO: preconditions
    # TODO: warnings
    # if problem_data != model_data, then warn

    # TODO: sort alphabetically
    
    if problem_data["forcing_inputs"] is None:
        logging.info(problem_data)

        y, data, status = scipy.integrate.odeint(
            func        = model_data["model"], \
            y0          = problem_data["initial_conditions"], \
            # A sequence of time points for which to solve for y.
            # The initial value point should be the first element of this sequence.
            # http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html#scipy.integrate.odeint
            t           = problem_data["time"], \
            args        = (model_data["parameters"], model_data["inputs"]), \
            full_output = True, \
            printmessg  = False, \
            ixpr        = False, \
            mxstep      = 50000)
        
        if status == 2:
            status = 0
    
    else:
        times_orig = copy.deepcopy(problem_data["time"])
        initial_conditions_orig = copy.deepcopy(problem_data["initial_conditions"])
        initials = None
        data = []
        y = None
        status = 0
        num_s = len(problem_data["forcing_inputs"]["continuous_time_intervals"])
        for ii in range(num_s-1):
            
            forcing_inputs = []
            for uu in range(len(model_data["inputs"])):
                forcing_inputs.append(problem_data["forcing_inputs"]["piecewise_constant_inputs"][ii][uu])
            model_data["inputs"] = forcing_inputs
            problem_data["inputs"] = forcing_inputs

            times = []
            for tt in range(len(problem_data["time"])):
                if problem_data["time"][tt] >= problem_data["forcing_inputs"]["continuous_time_intervals"][ii] \
                    and problem_data["time"][tt] <= problem_data["forcing_inputs"]["continuous_time_intervals"][ii+1]:
                    times.append(problem_data["time"][tt])
            problem_data["time"] = times
            
            # WIP: 2015-05-16, need to be careful with yesnoyes, for example
            if len(times) == 0:
                logging.warn("solvers.initialvalue: zero-length times at stage " + str(ii+1) + " of " + str(num_s-1))
                if ii+1 == num_s-1:
                    continue
                else:
                    assert(False)
                    raise
            
            # no need to do anything for outputs here...
            
            if ii > 0:
                problem_data["initial_conditions"] = initials
             
            #logging.info(problem_data)
            
            y_s, data_s, status_s = scipy.integrate.odeint(
                func        = model_data["model"], \
                y0          = problem_data["initial_conditions"], \
                # A sequence of time points for which to solve for y.
                # The initial value point should be the first element of this sequence.
                # http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html#scipy.integrate.odeint
                t           = problem_data["time"], \
                args        = (model_data["parameters"], model_data["inputs"]), \
                full_output = True, \
                printmessg  = False, \
                ixpr        = False, \
                mxstep      = 50000)
            
            initials = y_s[-1]
            # WIP: 2015-05-16, perhaps these y need to be conditional
            if ii == 0:
                y = copy.deepcopy(y_s)
            else:
                y = numpy.concatenate((y,y_s[1:]))
            data.append(data_s)
            if status_s == 2:
                status_s = 0
            status = status + status_s
            
            # need to do this here, as this gets operated upon in the loop
            problem_data["time"] = times_orig
            
        # TODO: 2015-0416, this invariant needs to be done better
        problem_data["time"] = times_orig
        problem_data["initial_conditions"] = initial_conditions_orig
    return status, y, data


'''
Computes the dynamic snapshots (or "time course") corresponding to the initial value problem.
Warning: it will unconditionally include the initial point
returns NumericResult
'''
def evaluate_timecourse_snapshots(model_data, problem_data):
    # TODO: problem_data["initial"] not being handled correctly if called direction
    assert(model_data["model"] is not None)
    # TODO: preconditions

    status, snapshots, diags_stats = solve(model_data, problem_data)
    results = {}
    is_successful = lambda x: True if x == 0 else False
    results["success"] = is_successful(status)
    results["snapshots"] = snapshots
    results["diags_stats"] = diags_stats
    result = mmd.NumericResult(results)
    return result


'''
Computes the dynamic trajectories (or "time course") corresponding to the initial value problem.
It conditionally includes/excludes the initial point
'''
# TODO: let problem_data count and use to override model_data
def evaluate_timecourse_trajectories(model_data, problem_data):
    assert(model_data["model"] is not None)
    # TODO: preconditions

    result = evaluate_timecourse_snapshots(model_data, problem_data)
    including_initial_value = common.utilities.sliceit_astrajectory(result.snapshots)
    trajectories = handle_initial_point(including_initial_value, problem_data)
    results = {}
    results["success"] = result.success
    results["trajectories"] = trajectories
    results["diags_stats"] = result.diags_stats
    result = mmd.NumericResult(results)
    return result


# TODO: rename; "compute_timecourse_snapshots"
def compute_trajectory_st(model, model_data, problem_data):
    """
    Computes the dynamic snapshots (or "time course") corresponding to the initial value problem.
    Warning: it will unconditionally include the initial point
    """
    # TODO: problem_data["initial"] not being handled correctly if called direction
    # TODO: preconditions
    assert(len(model_data["parameters"]) > 0)
    assert(len(model_data["inputs"]) > 0)

    if model is None:
        assert(model_data["model"] is not None)

    if model is not None:
        model_data["model"] = model
        cd.print_legacy_code_message()

    _, snapshot, _ = solve(model_data, problem_data)
    
    return snapshot


'''
Computes the dynamic trajectories (or "time course") corresponding to the initial value problem.
It conditionally includes/excludes the initial point
'''
# TODO: return numpy.array()
# TODO: let problem_data count and use to override model_data
def compute_timecourse_trajectories(model, model_data, problem_data):
    # TODO: preconditions

    if model is not None:
        cd.print_legacy_code_message()
    
    snapshots = compute_trajectory_st(model, model_data, problem_data)
    including_initial_value = common.utilities.sliceit_astrajectory(snapshots)
    trajectories = handle_initial_point(including_initial_value, problem_data)

    return trajectories

# -----------------------------------------------------------------------------
'''
Legacy
'''
# -----------------------------------------------------------------------------
'''
Calls odepack.lsoda to solve the initial value problem for stiff and non-stiff ode's.
Preconditions: at this point in time, all problem-specific stuff must have been done;
this is a direct solver call and there is no context to do problem-specific things
'''
# TODO: remove when possible
# TODO: deep copy?
def solve_lsoda_st(model, model_data, problem_data):
    assert(len(problem_data["initial_conditions"]) == len(model_data["states"]))
    # TODO: preconditions

    cd.print_legacy_code_message()

    # TODO: sort alphabetically
    y, data, _ = scipy.integrate.odeint(
        func        = model, \
        y0          = problem_data["initial_conditions"], \
        # A sequence of time points for which to solve for y.
        # The initial value point should be the first element of this sequence.
        # http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html#scipy.integrate.odeint
        t           = problem_data["time"], \
        args        = (model_data["parameters"], model_data["inputs"]), \
        full_output = True, \
        printmessg  = False, \
        ixpr        = False,
        mxstep      = 50000)
    return y, data