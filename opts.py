import sys
import teneva


sys.path.append('./pde')
from func_demo_pde_voi import FuncDemoPDEVOI


from utils import folder_ensure


class Opts:
    def __init__(self, fold='result', gmsh_path=None, d=7, n=10):
        # The path to folder with results:
        self.fold = fold
        folder_ensure(f'{self.fold}')
        folder_ensure(f'{self.fold}/logs')
        folder_ensure(f'{self.fold}/data')

        # The path to gmsh executable file:
        self.gmsh_path = gmsh_path

        # Dimension of the function input:
        self.d = d

        # Number of grid points for all dimensions:
        self.n = n

        # Number of train points (computational budget):
        self.m_trn = int(1.E+4)

        # Number of test points:
        self.m_tst = int(1.E+4)

        # TT-rank:
        self.r = 5

        # Number of TT-ALS sweeps (iterations):
        self.nswp = 50

        # Noise for TT-cores in TT-ANOVA:
        self.noise_ano = 1.E-10

        # Order of ANOVA decomposition:
        self.order = 1

        # Mesh size for PDE (it relates to  48983 vertices):
        self.s = 0.005
        self.k = 48983

        # The value of noise (for "appr_noise" computations)
        self.noise = 1.E-2

        # List of functions for approximation:
        self.funcs_appr = []

        # Number of repetitions of calculations with a random initial
        # approximation (the result is then averaged):
        self.reps = 10

        # Print ALS log to console:
        self.with_log = False

    def get_fpath(self, func, kind='trn_ind'):
        return f'{self.fold}/data/{func.name}_{kind}.npz'

    def info(self):
        text = '\n' + '-' * 74 + '\n'
        text += f'Dimension       = {self.d:-8.0f}  \n'
        text += f'Samples train   = {self.m_trn:-8.1e}  \n'
        text += f'Samples test    = {self.m_tst:-8.1e}  \n'
        text += f'Grid size       = {self.n:-8.0f}      \n'
        text += f'TT-rank         = {self.r:-8.0f}      \n'
        text += f'ALS sweeps      = {self.nswp:-8.0f}   \n'
        text += f'ANO order       = {self.order:-8.0f}  \n'
        text += f'ANO noise       = {self.noise_ano:-8.1e}  \n'
        text += '-' * 74 + '\n' + '\n'
        return text

    def prep_funcs(self):
        self.funcs_appr = teneva.func_demo_all(self.d, with_piston=True)

        for func in self.funcs_appr:
            func.set_grid(self.n, kind='uni')

    def prep_pde(self, size=None, name=None, with_add=True, with_prep=True):
        size = size or self.s
        func = FuncDemoPDEVOI(d=9, name=name)
        func.set_grid(self.n, kind='uni')
        if with_prep:
            func.prep_pde(size, 'circ', self.gmsh_path)

        if with_add:
            self.funcs_appr.append(func)
        else:
            return func
