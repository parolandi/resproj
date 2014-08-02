    def do_test_epo_receptor_solve_time_course_dof(self):
        params = numpy.ones(len(models.ordinary_differential.params_i))
        for par in models.ordinary_differential.params_i.items():
            params[par[1]] = models.ordinary_differential.epo_receptor_default_parameters[par[0]]
        inputs = numpy.ones(len(models.ordinary_differential.inputs_i))
        for inp in models.ordinary_differential.inputs_i.items():
            inputs[inp[1]] = models.ordinary_differential.epo_receptor_default_inputs[inp[0]]

        model_instance = dict(models.model_data.model_structure)
        model_instance["parameters"] = params
        model_instance["inputs"] = inputs
        model_instance["states"] = numpy.zeros(len(models.ordinary_differential.epo_receptor_states))
        
        problem_instance = dict(models.model_data.problem_structure)
        problem_instance["initial_conditions"] = numpy.zeros(len(models.ordinary_differential.epo_receptor_states))
        problem_instance["initial_conditions"][models.ordinary_differential.states_i["Epo"]] = 2030.19
        problem_instance["initial_conditions"][models.ordinary_differential.states_i["EpoR"]] = 516
        times = numpy.arange(0.0, 1500.0, 100.0)
        problem_instance["time"] = times
        # WIP deep-copy
#        problem_instance["parameters"] = copy.deepcopy(model_instance["parameters"])
        problem_instance["parameters"] = model_instance["parameters"]
        problem_instance["inputs"] = model_instance["inputs"]
        problem_instance["states"] = model_instance["states"]
        
        offset = 0.001
        problem_instance["parameters"][models.ordinary_differential.params_i["k_on"]] += offset
        problem_instance["parameter_indices"] = [[models.ordinary_differential.params_i["k_on"]]]
        
        result = solvers.initial_value.compute_trajectory_st( \
            models.ordinary_differential.epo_receptor, model_instance, problem_instance)
        snapshots = numpy.asarray(result)
        trajectories = numpy.transpose(snapshots)
        actual = dict(models.ordinary_differential.epo_receptor_states)
        for item in models.ordinary_differential.states_i.items():
            key = item[0]
            index = item[1]
            actual[key] = trajectories[index]
        expected = dict(models.ordinary_differential.epo_receptor_states)
        # copasi result @times=0:1500:100
        expected["Epo"] = numpy.asarray([2030.19, 638.782, 155.361, 37.5639, 10.2865, 2.90606, 0.82607, 0.235169, 0.0669758, 0.0190769,  0.00543388, 0.00154781, 0.000440884, 0.000125583, 3.57718E-005, 1.01894E-005])
        if (offset > 0.0):
            expected["Epo"][0] += 10
#        assert(len(actual["Epo"]) == len(expected["Epo"]))
#        res = 
        gap = 3
        if (offset > 0.0):
            gap = 5
            [self.assertNotAlmostEquals(act, exp, gap) for act, exp in zip(actual["Epo"], expected["Epo"])]
        else:
            [self.assertAlmostEquals(act, exp, gap) for act, exp in zip(actual["Epo"], expected["Epo"])]