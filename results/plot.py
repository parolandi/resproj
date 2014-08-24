
import matplotlib.pyplot as pp


def plot_errors_and_residuals(independent,  errors, residuals):
    # TODO assertions
    
    x = independent
    legend = []
    for ii in range(len(errors)):
        pp.plot(x, errors[ii], 'o-')
        legend.append("e" + str(ii))
        pp.plot(x, residuals[ii], '+-')
        legend.append("p" + str(ii))
    pp.legend(legend)
    pp.show()


def plot_fit(independent,  measurements, predictions, actuals):
    # TODO assertions
    
    x = independent
    y_meas = measurements
    y_pred = predictions
    y_true = actuals
    legend = []
    for ii in range(len(y_meas)):
        pp.plot(x, y_meas[ii], 'o')
        legend.append("m" + str(ii))
        pp.plot(x, y_pred[ii], '+-')
        legend.append("p" + str(ii))
        pp.plot(x, y_true[ii], '*-')
        legend.append("t" + str(ii))
    pp.legend(legend)
    pp.show()


def plot_observations(independent,  measurements):
    x = independent
    y_meas = measurements
    legend = [] 
    for ii in range(len(y_meas)):
        pp.plot(x, y_meas[ii], 'o')
        legend.append("m" + str(ii))
    pp.legend(legend)
    pp.show()


def plot_residuals(independent,  residuals):
    x = independent
    ress = residuals
    legend = [] 
    for ii in range(len(ress)):
        pp.plot(x, ress[ii], 'o')
        legend.append("r" + str(ii))
    pp.legend(legend)
    pp.show()


def plot_observation_ensembles(independent,  measurements):
    x = independent
    y_meass = measurements
    legend = []
    # ensembles
    done_already = False
    color_cycle = ['r', 'g', 'b', 'y']
    for ii in range(len(y_meass)):
        # observations
        for jj in range(len(y_meass[ii])):
            
            pp.plot(x, y_meass[ii][jj], color=color_cycle[jj], linestyle='', marker='o')
            if not done_already:
                legend.append("m" + str(jj))
        done_already = True
    pp.legend(legend)
    pp.show()
