"""Demo for PDE solver.

Run it from the root of the project as "python pde/demo_solve.py"

"""
import sys
from time import perf_counter as tpc


from mesh import Mesh
from pde import Pde


def demo(size=0.005, kind='circ', gmsh_path=None):
    # Build the spatial grid for PDE:
    mesh = Mesh(size, kind, gmsh_path)

    # Initialize the PDE class instance:
    pde = Pde(mesh)

    t = tpc()

    # PDE parameter value:
    p = [0.8, 0.3, 0.24, 0.99, 0.8, 0.7, 0.4, 0.04, 0.1]

    # Solve PDE and compute average temperature (VOI):
    voi = pde.get_voi(p)
    vertices = mesh.mesh.num_vertices()

    t = tpc() - t

    print('\n\n')
    print(f'Total time   (sec)      : {t:-8.2f}')
    print(f'Average temperature     : {voi:-8.2e}')
    print(f'Number of mesh vertices : {vertices}')

    print('\n\n')

    # Plot the results:
    pde.plot_mesh()
    pde.plot_k()
    pde.plot_u()


if __name__ == '__main__':
    size = 0.01
    kind = 'circ'

    device = sys.argv[1] if len(sys.argv) > 1 else 'pc'
    gmsh_path = './gmsh/build/gmsh' if device == 'docker' else None

    demo(size, kind, gmsh_path)
