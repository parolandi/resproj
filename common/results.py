
import numpy as np

def append_traces_to_time(time, traces):
    if len(time) == 0 and len(traces) == 0:
        return None
    time = np.asarray(time)
    time_and_traces = np.append([np.transpose(time)], traces, axis = 0)
    return time_and_traces

def append_traces_to_time_and_transpose(time, traces):
    data = append_traces_to_time(time, traces)
    if data is None:
        return
    return np.transpose(data)