
import experiments.legacy_algebraic
import experiments.legacy_ordinary_differential

if __name__ == '__main__':
    
    # do all legacy ordinary differential experiments
    def do_legorddiff():
        experiments.legacy_ordinary_differential.experiment1()
        experiments.legacy_ordinary_differential.experiment2()
        experiments.legacy_ordinary_differential.experiment3()
        experiments.legacy_ordinary_differential.experiment4()
        experiments.legacy_ordinary_differential.experiment5()
        experiments.legacy_ordinary_differential.experiment6()
        experiments.legacy_ordinary_differential.experiment7()
        

    # do all legacy algebraic experiments
    def do_legalg():
        experiments.legacy_algebraic.experiment3()
        experiments.legacy_algebraic.experiment4()
        experiments.legacy_algebraic.experiment5()
        experiments.legacy_algebraic.experiment6()
        experiments.legacy_algebraic.experiment7()
        experiments.legacy_algebraic.experiment8()
        
    
    # just do it
    do_legalg()
    do_legorddiff()
