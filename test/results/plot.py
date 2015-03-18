
import unittest
import results.plot as testme

import numpy

import results.plot_data as replda


class TestPlot(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(TestPlot, self).__init__(*args, **kwargs)
        self.do_plotting = True


    def setup_plot(self):
        plotdata = dict(replda.plot_data)
        plotdata["title"] = "test"
        plotdata["window_title"] = "Test"
        return plotdata
    

    def test_plot_ellipse(self):
        mean = [1,0]
        covariance = [[1,2],[2,9]]
        if self.do_plotting:
            testme.plot_ellipse(mean, covariance, self.setup_plot())


    def test_plot_ellipse_and_box(self):
        mean = [1,0]
        covariance = [[1,2],[2,9]]
        vertices = [[0,2], [0,2]]
        if self.do_plotting:
            testme.plot_ellipse_and_box(mean, covariance, vertices, self.setup_plot())
        covariance = [[1,-1],[-1,9]]
        if self.do_plotting:
            testme.plot_ellipse_and_box(mean, covariance, vertices, self.setup_plot())


    def test_plot_box(self):
        vertices = [[0,2], [0,2]]
        if self.do_plotting:
            testme.plot_box(vertices, self.setup_plot())


    def test_plot_scatter(self):
        x = [1,2,3,4,5]
        y = [5,4,3,2,1]
        if self.do_plotting:
            testme.plot_scatter(x, y, self.setup_plot())
        

    def test_plot_scatter_and_box(self):
        x = numpy.asarray([1,2,3,4,5])
        y = numpy.asarray([5,4,3,2,1])
        vertices = [[0,2], [0,2]]
        if self.do_plotting:
            testme.plot_scatter_and_box(x, y, vertices, self.setup_plot())


if __name__ == "__main__":
    unittest.main()