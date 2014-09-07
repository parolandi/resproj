
from __future__ import print_function
import math

workflow_data = {
    "params": [],
    "obj": [],
    "obj_contribs": [],
    "ssr": [],
    "ssr_contribs": [],
    "conf_intervs": [],
    }


workflow_results = {
    "full": workflow_data,
    "calibration": workflow_data,
    "validation": workflow_data,
    "calib+valid": workflow_data, 
    }


def report_all(results):
    print("Label", "Full", "Calib", "Valid", "Calib+Valid", "Sum")
    
    print("Params", \
          results["full"]["params"], \
          results["calibration"]["params"], \
          results["validation"]["params"], \
          results["calib+valid"]["params"], \
          "[n/a]")
    print("Obj", \
          results["full"]["obj"][len(results["full"]["obj"])-1], \
          results["calibration"]["obj"][len(results["calibration"]["obj"])-1], \
          results["validation"]["obj"][len(results["validation"]["obj"])-1], \
          results["calib+valid"]["obj"][len(results["calib+valid"]["obj"])-1], \
          results["calibration"]["obj"][len(results["calibration"]["obj"])-1] + \
          results["validation"]["obj"][len(results["validation"]["obj"])-1])
    print("Obj contribs", \
          results["full"]["obj_contribs"][len(results["full"]["obj_contribs"])-1], \
          results["calibration"]["obj_contribs"][len(results["calibration"]["obj_contribs"])-1], \
          results["validation"]["obj_contribs"][len(results["validation"]["obj_contribs"])-1], \
          results["calib+valid"]["obj_contribs"][len(results["calib+valid"]["obj_contribs"])-1], \
          [results["calibration"]["obj_contribs"][len(results["calibration"]["obj_contribs"])-1][0] +
          results["validation"]["obj_contribs"][len(results["validation"]["obj_contribs"])-1][0], \
          results["calibration"]["obj_contribs"][len(results["calibration"]["obj_contribs"])-1][1] +
          results["validation"]["obj_contribs"][len(results["validation"]["obj_contribs"])-1][1]])
    print("Conf intervs", \
          results["full"]["conf_intervs"][len(results["full"]["conf_intervs"])-1], \
          results["calibration"]["conf_intervs"][len(results["calibration"]["conf_intervs"])-1], \
          results["validation"]["conf_intervs"][len(results["validation"]["conf_intervs"])-1], \
          results["calib+valid"]["conf_intervs"][len(results["calib+valid"]["conf_intervs"])-1], \
          
          [math.sqrt(results["calibration"]["conf_intervs"][len(results["calibration"]["conf_intervs"])-1][0] *
          results["validation"]["conf_intervs"][len(results["validation"]["conf_intervs"])-1][0]), \
          math.sqrt(results["calibration"]["conf_intervs"][len(results["calibration"]["conf_intervs"])-1][1] *
          results["validation"]["conf_intervs"][len(results["validation"]["conf_intervs"])-1][1])])
    