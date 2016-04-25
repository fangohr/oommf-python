import pytest
from evolvers import RungeKuttaEvolve


class TestRungeKuttaEvolve(object):
    def setup(self):
        # Set of valid arguments.
        self.args1 = [[1, 1, 1],
                      [0.5, 1e5, 0.01],
                      [0.05, 2.21e5, 5e6],
                      [0.1, .1, 1e-2]]

        # Set of invalid arguments.
        self.args2 = [[-0.1, 1, 1],
                      [0.5, -1e5, 0.01],
                      [0.05, 2.21e5, 'abc'],
                      [0.1, .1, -1e-2]]

    def test_init(self):
        # Valid arguments.
        for arg in self.args1:
            alpha = arg[0]
            gamma_G = arg[1]
            start_dm = arg[2]

            evolver = RungeKuttaEvolve(alpha, gamma_G, start_dm)

            assert evolver.alpha == alpha
            assert isinstance(alpha, (int, float))
            assert evolver.gamma_G == gamma_G
            assert isinstance(gamma_G, (int, float))
            assert evolver.start_dm == start_dm
            assert isinstance(start_dm, (int, float))

    def test_init_exceptions(self):
        # Invalid arguments (ValueError expected).
        for arg in self.args2:
            alpha = arg[0]
            gamma_G = arg[1]
            start_dm = arg[2]

            with pytest.raises(ValueError):
                evolver = RungeKuttaEvolve(alpha, gamma_G, start_dm)

    def test_get_mif(self):
        for arg in self.args1:
            alpha = arg[0]
            gamma_G = arg[1]
            start_dm = arg[2]

            evolver = RungeKuttaEvolve(alpha, gamma_G, start_dm)

            mif = evolver.get_mif()
            mif_lines = evolver.get_mif().split('\n')

            # Assert comment.
            l = mif_lines[0].split()
            assert l[0] == '#'
            assert l[1] == 'RungeKutta'
            assert l[2] == 'evolver'

            # Assert set statements.
            expected_data = [('alpha', alpha),
                             ('gamma_G', gamma_G),
                             ('start_dm', start_dm)]
            c = 0
            for line in mif_lines[1:4]:
                l = line.split()
                assert l[0] == 'set'
                assert l[1] == expected_data[c][0]
                assert float(l[2]) == expected_data[c][1]
                c += 1

            # Assert Specify line.
            l = mif_lines[4].split()
            assert l[0] == 'Specify'
            assert l[1].split(':')[0] == 'Oxs_RungeKuttaEvolve'
            assert l[2] == '{'

            # Assert parameters lines
            assert mif_lines[5][0] == '\t'
            l = mif_lines[5].split()
            assert l[0] == 'alpha'
            assert l[1] == '$alpha'

            # Assert parameters lines
            assert mif_lines[6][0] == '\t'
            l = mif_lines[6].split()
            assert l[0] == 'gamma_G'
            assert l[1] == '$gamma_G'

            # Assert parameters lines
            assert mif_lines[7][0] == '\t'
            l = mif_lines[7].split()
            assert l[0] == 'start_dm'
            assert l[1] == '$start_dm'

            # Assert mif end.
            assert mif_lines[8] == '}'

            # Assert new lines at the end of the string.
            assert mif[-2:] == '\n\n'
