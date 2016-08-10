# -*- coding: utf-8 -*-
import dolfin
import mshr
import helpers
import numpy
import pyfvm
from pyfvm.form_language import *
from sympy import pi, sin, cos, exp
import unittest


def exact_sol(x):
    return cos(pi/2 * (x[0]**2 + x[1]**2 + x[2]**2))


class Bratu(FvmProblem):
    def apply(self, u):
        def rhs(x):
            z = pi/2 * (x[0]**2 + x[1]**2 + x[2]**2)
            return 2*pi * (1.5 * sin(z) + z * cos(z)) - 2.0 * exp(cos(z))

        return integrate(lambda x: -n_dot_grad(u(x)), dS) \
            - integrate(lambda x: 2.0 * exp(u(x)), dV) \
            - integrate(rhs, dV)

    def dirichlet(self, u):
        return [
            (lambda x: u(x) - exact_sol(x), 'boundary')
            ]


def get_mesh(k):
    h = 0.5**(k+2)
    c = mshr.Sphere(dolfin.Point(0., 0., 0.), 1.0, int(2*pi / h))
    m = mshr.generate_mesh(c, 2.0 / h)
    return pyfvm.meshTetra.meshTetra(
            m.coordinates(),
            m.cells(),
            mode='geometric'
            )


class ConvergenceBratu3dBallTest(unittest.TestCase):

    def setUp(self):
        return

    @staticmethod
    def solve(verbose=False):
        def solver(mesh):
            f, jacobian = pyfvm.discretize(Bratu(), mesh)
            u0 = numpy.zeros(len(mesh.node_coords))
            u = pyfvm.newton(f.eval, jacobian.get_matrix, u0, verbose=True)
            return u

        return helpers.perform_convergence_tests(
            solver,
            exact_sol,
            get_mesh,
            range(3),
            verbose=verbose
            )

    def test(self):
        H, error_norm_1, error_norm_inf, order_1, order_inf = self.solve()

        expected_order = 2
        tol = 2.0e-1
        self.assertGreater(order_1[-1], expected_order - tol)
        self.assertGreater(order_inf[-1], expected_order - tol)

        return


if __name__ == '__main__':
    from matplotlib import pyplot as plt

    H, error_norm_1, error_norm_inf, order_1, order_inf = \
        ConvergenceBratu3dBallTest.solve(verbose=True)

    helpers.plot_error_data(H, error_norm_1, error_norm_inf)
    plt.show()
