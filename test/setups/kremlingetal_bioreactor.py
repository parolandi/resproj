
import unittest
import setups.kremlingetal_bioreactor as testme


# TODO: 2015-05-31; test base problem setup
class TestKremlingEtAlBioreactor(unittest.TestCase):


    def test_sensitivity_model_setup(self):
        model = testme.do_sensitivity_model_setup()
        self.assertTrue(len(model["states"]) == 36)


if __name__ == "__main__":
    unittest.main()
