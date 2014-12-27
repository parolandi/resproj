
import unittest
import results.plot_tiles as testme

import numpy


class TestPlotTiles(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestPlotTiles, self).__init__(*args, **kwargs)
        self.do_plotting = True

    
    def test_plot_states_and_sensitivities(self):
        time = [0,1,2,3]
        states = [[1,1,1,1],[2,2,2,2]]
        # mn, with m state and n parameter 
        sensitivities = [[11,11,11,11],[12,12,12,12],[13,13,13,13], \
                         [21,21,21,21],[22,22,22,22],[23,23,23,23]]
        testme.plot_states_and_sensitivities(time, states, sensitivities, 3)


    def test_plot_measurements_with_calibration_and_validation_trajectories_with_errors_without_errors_2x(self):
        independent_calib = [0, 1, 2, 3, 4, 5]
        measurements_calib = [[1.0, 1.1, 1.2, 1.3, 1.4, 1.5], [2.0, 2.1, 2.2, 2.3, 2.4, 2.5]]
        predictions_calib = [[1.0+0.1, 1.1-0.1, 1.2-0.1, 1.3+0.1, 1.4-0.1, 1.5+0.1], [2.0+0.1, 2.1-0.1, 2.2-0.1, 2.3+0.1, 2.4-0.1, 2.5+0.1]]
        independent_valid = [0, 6, 7, 8, 9, 10]
        measurements_valid = [[1.0, 1.6, 1.7, 1.8, 1.9, 2.0], [2.0, 2.6, 2.7, 2.8, 2.9, 3.0]]
        predictions_valid = [[1.0+0.1, 1.6-0.1, 1.7-0.1, 1.8+0.1, 1.9-0.1, 2.0+0.1], [2.0+0.1, 2.6-0.1, 2.7-0.1, 2.8+0.1, 2.9-0.1, 3.0+0.1]]
        testme.plot_measurements_with_calibration_and_validation_trajectories_with_errors( \
            independent_calib, measurements_calib, predictions_calib, None, \
            independent_valid, measurements_valid, predictions_valid, None)


    def test_plot_measurements_with_calibration_and_validation_trajectories_with_errors_2x(self):
        independent_calib = [0, 1, 2, 3, 4, 5]
        measurements_calib = numpy.asarray([[1.0, 1.1, 1.2, 1.3, 1.4, 1.5], [2.0, 2.1, 2.2, 2.3, 2.4, 2.5]])
        predictions_calib = numpy.asarray([[1.0+0.1, 1.1-0.1, 1.2-0.1, 1.3+0.1, 1.4-0.1, 1.5+0.1], [2.0+0.1, 2.1-0.1, 2.2-0.1, 2.3+0.1, 2.4-0.1, 2.5+0.1]])
        errors_calib = [[0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]]
        independent_valid = [0, 6, 7, 8, 9, 10]
        measurements_valid = numpy.asarray([[1.0, 1.6, 1.7, 1.8, 1.9, 2.0], [2.0, 2.6, 2.7, 2.8, 2.9, 3.0]])
        predictions_valid = numpy.asarray([[1.0+0.1, 1.6-0.1, 1.7-0.1, 1.8+0.1, 1.9-0.1, 2.0+0.1], [2.0+0.1, 2.6-0.1, 2.7-0.1, 2.8+0.1, 2.9-0.1, 3.0+0.1]])
        errors_valid = errors_calib
        testme.plot_measurements_with_calibration_and_validation_trajectories_with_errors( \
            independent_calib, measurements_calib, predictions_calib, errors_calib, \
            independent_valid, measurements_valid, predictions_valid, errors_valid)
        testme.show_all()


    def test_plot_residual_trajectories_with_errors_2x(self):
        independent_calib = [0, 1, 2, 3, 4, 5]
        measurements_calib = numpy.asarray([[1.0, 1.1, 1.2, 1.3, 1.4, 1.5], [2.0, 2.1, 2.2, 2.3, 2.4, 2.5]])
        predictions_calib = numpy.asarray([[1.0+0.1, 1.1-0.1, 1.2-0.1, 1.3+0.1, 1.4-0.1, 1.5+0.1], [2.0+0.1, 2.1-0.1, 2.2-0.1, 2.3+0.1, 2.4-0.1, 2.5+0.1]])
        errors_calib = [[0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]]
        independent_valid = [0, 6, 7, 8, 9, 10]
        measurements_valid = numpy.asarray([[1.0, 1.6, 1.7, 1.8, 1.9, 2.0], [2.0, 2.6, 2.7, 2.8, 2.9, 3.0]])
        predictions_valid = numpy.asarray([[1.0+0.1, 1.6-0.1, 1.7-0.1, 1.8+0.1, 1.9-0.1, 2.0+0.1], [2.0+0.1, 2.6-0.1, 2.7-0.1, 2.8+0.1, 2.9-0.1, 3.0+0.1]])
        errors_valid = errors_calib
        testme.plot_residual_trajectories_with_errors( \
            independent_calib, measurements_calib, predictions_calib, errors_calib, \
            independent_valid, measurements_valid, predictions_valid, errors_valid)
        testme.show_all()

    
    # TODO: test with None as errors
    

if __name__ == "__main__":
    unittest.main()
