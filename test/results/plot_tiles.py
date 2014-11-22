
import unittest
import results.plot_tiles as rpt


class TestPlotTiles(unittest.TestCase):


    def test_plot_states_and_sensitivities(self):
        time = [0,1,2,3]
        states = [[1,1,1,1],[2,2,2,2]]
        # mn, with m state and n parameter 
        sensitivities = [[11,11,11,11],[12,12,12,12],[13,13,13,13], \
                         [21,21,21,21],[22,22,22,22],[23,23,23,23]]
        rpt.plot_states_and_sensitivities(time, states, sensitivities, 3)


if __name__ == "__main__":
    unittest.main()
