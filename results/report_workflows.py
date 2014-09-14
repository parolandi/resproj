
from __future__ import print_function
import math


# it: workflow_data
def report_data(it):
    print("Params", it["params"])
    print("Obj", it["obj"][len(it["obj"])-1])
    print("Obj contribs", it["obj_contribs"][len(it["obj_contribs"])-1])
    print("Conf intervs", it["conf_intervs"][len(it["conf_intervs"])-1])
    

#it : workflow_results
def report_results(it):
    print("Label", "Full", "Calib", "Valid", "Calib+Valid", "Sum")
    
    print("Params", \
          it["full"]["params"], \
          it["calibration"]["params"], \
          it["validation"]["params"], \
          it["calib+valid"]["params"], \
          "[n/a]")
    print("Obj", \
          it["full"]["obj"][len(it["full"]["obj"])-1], \
          it["calibration"]["obj"][len(it["calibration"]["obj"])-1], \
          it["validation"]["obj"][len(it["validation"]["obj"])-1], \
          it["calib+valid"]["obj"][len(it["calib+valid"]["obj"])-1], \
          it["calibration"]["obj"][len(it["calibration"]["obj"])-1] + \
          it["validation"]["obj"][len(it["validation"]["obj"])-1])
    print("Obj contribs", \
          it["full"]["obj_contribs"][len(it["full"]["obj_contribs"])-1], \
          it["calibration"]["obj_contribs"][len(it["calibration"]["obj_contribs"])-1], \
          it["validation"]["obj_contribs"][len(it["validation"]["obj_contribs"])-1], \
          it["calib+valid"]["obj_contribs"][len(it["calib+valid"]["obj_contribs"])-1], \
          [it["calibration"]["obj_contribs"][len(it["calibration"]["obj_contribs"])-1][0] +
          it["validation"]["obj_contribs"][len(it["validation"]["obj_contribs"])-1][0], \
          it["calibration"]["obj_contribs"][len(it["calibration"]["obj_contribs"])-1][1] +
          it["validation"]["obj_contribs"][len(it["validation"]["obj_contribs"])-1][1]])
    print("Conf intervs", \
          it["full"]["conf_intervs"][len(it["full"]["conf_intervs"])-1], \
          it["calibration"]["conf_intervs"][len(it["calibration"]["conf_intervs"])-1], \
          it["validation"]["conf_intervs"][len(it["validation"]["conf_intervs"])-1], \
          it["calib+valid"]["conf_intervs"][len(it["calib+valid"]["conf_intervs"])-1], \
          
          [math.sqrt(it["calibration"]["conf_intervs"][len(it["calibration"]["conf_intervs"])-1][0] *
          it["validation"]["conf_intervs"][len(it["validation"]["conf_intervs"])-1][0]), \
          math.sqrt(it["calibration"]["conf_intervs"][len(it["calibration"]["conf_intervs"])-1][1] *
          it["validation"]["conf_intervs"][len(it["validation"]["conf_intervs"])-1][1])])
    