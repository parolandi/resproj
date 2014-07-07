
import application.legacy
import experiments.algebraic

if __name__ == '__main__':
    
    def doit():
        experiments.algebraic.experiment3()
        experiments.algebraic.experiment4()
        
        application.legacy.doit()
        return
    
    # just do it
    doit()