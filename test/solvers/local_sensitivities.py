
import unittest
import solvers.local_sensitivities as testme

import test.common.mock_models as cmm


class TestLocalSensitivities(unittest.TestCase):


    def test_compute_timecourse_trajectories_and_sensitivities_with_linear_2p2s(self):
        model_data, problem_data = cmm.do_setup_include_initial()
        sens_traj = testme.compute_timecourse_trajectories_and_sensitivities(model_data, problem_data)
        self.assertAlmostEquals(sens_traj[0][len(sens_traj[0])-1], 1.0, 8)
        self.assertAlmostEquals(sens_traj[1][len(sens_traj[1])-1], 2.0, 8)
        self.assertAlmostEquals(sens_traj[2][len(sens_traj[2])-1], 1.0, 8)
        self.assertAlmostEquals(sens_traj[3][len(sens_traj[3])-1], 0.0, 8)
        self.assertAlmostEquals(sens_traj[4][len(sens_traj[4])-1], 0.0, 8)
        self.assertAlmostEquals(sens_traj[5][len(sens_traj[5])-1], 2.0, 8)


if __name__ == "__main__":
    unittest.main()