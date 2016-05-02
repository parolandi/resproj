
import numpy as np

def append_traces_to_time(time, traces):
    time = np.asarray(time)
    time_and_traces = np.append([np.transpose(time)], traces, axis=0)
    return time_and_traces

def append_traces_to_time_and_transpose(time, traces):
    return np.transpose(append_traces_to_time(time,traces))