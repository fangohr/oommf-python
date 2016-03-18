import os
import sys

# putting 'joommf' into search path
sys.path.insert(0, os.path.abspath('..'))
print(sys.path)


def test_run_min_example():
    import joommf.minimisation_example
    joommf.minimisation_example.main()



def test_run_dyn_example():
    import joommf.dynamics_example
    joommf.dynamics_example.main()
