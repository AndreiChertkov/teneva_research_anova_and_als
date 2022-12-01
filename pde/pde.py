try:
    import fenics
    WITH_FENICS = True
except Exception as e:
    WITH_FENICS = False


import matplotlib.pyplot as plt


# The value of PDE coefficient outside the circles:
PARAM_BASE_VALUE = 1.


class Pde():
    """Class represents the PDE-solver based on the fenics package.

    Note:
        Method "get_voi" solves PDE for the given multidimensional parameter
        value and returns the average temperature.

    """
    def __init__(self, mesh):
        self.mesh = mesh

        self.V = fenics.FunctionSpace(self.mesh.mesh, 'P', 1)

        self.f = fenics.Constant(1)

        self.u = fenics.Function(self.V)
        self.v = fenics.TestFunction(self.V)

        def boundary(x, on_boundary):
            e = 1.E-8
            return on_boundary or x[0]<e or x[1]<e or x[0]>1-e or x[1]>1-e
        self.bc = fenics.DirichletBC(self.V, fenics.Constant(0), boundary)

        self.k = None

    def get_voi(self, p=None):
        self.solve(p)
        return fenics.assemble(self.u * fenics.dx)

    def init_k(self, p):
        CIRC_NUM_X = self.mesh.CIRC_NUM_X
        CIRC_DIST = self.mesh.CIRC_DIST
        CIRC_RAD = self.mesh.CIRC_RAD

        class Circ(fenics.UserExpression):
            def eval(self, values, x):
                values[0] = PARAM_BASE_VALUE

                r = CIRC_RAD
                e = 0.

                x0 = 0
                y0 = 0

                for k_x in range(1, CIRC_NUM_X + 1):
                    for k_y in range(1, CIRC_NUM_X + 1):
                        x_c = x0 + k_x * CIRC_DIST + (k_x - 1) * 2 * r + r;
                        y_c = y0 + k_y * CIRC_DIST + (k_y - 1) * 2 * r + r;
                        if (x[0] - x_c)**2 + (x[1] - y_c)**2 <= (r - e)**2:
                            ind = (k_y - 1) + (k_x - 1) * CIRC_NUM_X
                            values[0] = p[ind]
                            return

            def value_shape(self):
                return ()

        self.k = fenics.interpolate(Circ(degree=2), self.V)

    def plot_k(self, with_mesh=False):
        if self.k is None:
            return

        plt.figure(figsize=(10, 10))
        fenics.plot(self.k, title='PDE coefficient')
        if with_mesh:
            fenics.plot(self.mesh.mesh)
        plt.show()

    def plot_mesh(self, with_mesh=False):
        plt.figure(figsize=(10, 10))
        fenics.plot(self.mesh.mesh, title='PDE mesh')
        plt.show()

    def plot_u(self, with_mesh=False):
        plt.figure(figsize=(10, 10))
        fenics.plot(self.u, title='PDE solution')
        if with_mesh:
            fenics.plot(self.mesh.mesh)
        plt.show()

    def solve(self, p=None):
        if p is not None:
            self.init_k(p)

        if self.k is None:
            raise ValueError('PDE coefficient is not set')

        dx = fenics.dx
        du = fenics.grad(self.u)
        dv = fenics.grad(self.v)
        F = fenics.dot(self.k * du, dv) * dx - self.f * self.v * dx
        fenics.solve(F == 0, self.u, self.bc)
