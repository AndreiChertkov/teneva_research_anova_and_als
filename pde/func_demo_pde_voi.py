import numpy as np
import teneva


from mesh import Mesh
from pde import Pde


class FuncDemoPDEVOI(teneva.Func):
    def __init__(self, d=9, name=None):
        """Black box function representing the average PDE solution.

        This class is based on the "Func" class from the "teneva" package,
        which implements the interface for multivariable function (black box)
        with various methods (including TT-ALS, TT-ANOVA and TT-CROSS) for
        constructing its low-rank tensor approximation in the TT-format and
        utilities for building datasets (train, validation, test), check the
        accuracy, etc. Call "get_f_poi" to calculate the function in the given
        spatial point(s). Method "get_f_ind" may be used for function evaluation
        on the tensor grid.

        This class represents the black box function which is the average
        temperature (solution) for the parametric PDE. The function arguments
        are 9 parameters of the PDE, representing the values of the thermal
        conductivity coefficient in the corresponding regions of space. See
        "pde/pde.py" for more details.

        Args:
            d (int): number of dimensions.

        Note:
            Call "prep_pde" method before the main usage to build the spatial
            mesh and initialize the PDE class instance.

        """
        super().__init__(d, name=name or 'PDE-VOI')

        if self.d != 9:
            raise ValueError('FuncDemoPDEVOI is available only for 9-d case')

        self.set_lim(0.01, 1.)
        self.pde = None

    def prep_pde(self, size=0.005, kind='circ', gmsh_path=None):
        mesh = Mesh(size, kind, gmsh_path)
        self.pde = Pde(mesh)

    def _calc(self, x):
        if self.pde is None:
            raise ValueError('PDE is not set. Run "prep_pde" before')

        return self.pde.get_voi(x)
