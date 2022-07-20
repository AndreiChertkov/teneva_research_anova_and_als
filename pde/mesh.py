import fenics
import subprocess


class Mesh():
    """Class represents the spatial grid for PDE.

    Note:
        The attribute self.mesh is the mesh in the fenics format and it may be
        used in the PDE solver.

    """
    def __init__(self, size=0.005, kind='circ', gmsh_path=None):
        self.size = size
        self.kind = kind
        self.gmsh_path = gmsh_path or 'gmsh'

        if kind == 'circ':
            mesh_geo = self.prepare_mesh_circ_geo()
        else:
            raise ValueError(f'Unsupported mesh kind "{kind}"')

        self.build_mesh_from_geo(mesh_geo)

    def build_mesh_from_geo(self, mesh_geo):
        try:
            cmd = 'rm -rf ./tmp_gmsh'
            res = subprocess.run(cmd, shell=True)
        except Exception as e:
            pass

        cmd = 'mkdir ./tmp_gmsh'
        res = subprocess.run(cmd, shell=True)

        with open('./tmp_gmsh/mesh.geo', 'w', encoding='UTF-8') as f:
            f.write(mesh_geo)

        cmd = self.gmsh_path
        cmd += ' -2 ./tmp_gmsh/mesh.geo -o ./tmp_gmsh/mesh.msh -format msh2'
        res = subprocess.run(cmd, shell=True)

        cmd = 'dolfin-convert ./tmp_gmsh/mesh.msh ./tmp_gmsh/mesh.xml'
        res = subprocess.run(cmd, shell=True)

        self.mesh = fenics.Mesh('./tmp_gmsh/mesh.xml')

        cmd = 'rm -r ./tmp_gmsh'
        res = subprocess.run(cmd, shell=True)

    def prepare_mesh_circ_geo(self):
        self.CIRC_NUM_X = 3
        self.CIRC_NUM_Y = 3
        self.CIRC_NUM = self.CIRC_NUM_X * self.CIRC_NUM_Y
        self.CIRC_RAD = 1. / (4. * self.CIRC_NUM_X + 2.)
        self.CIRC_DIST = 1. - self.CIRC_NUM_X * 2 * self.CIRC_RAD
        self.CIRC_DIST /= self.CIRC_NUM_X + 1

        mesh = '''
            // -----------------------------------------------------------------
            // --- Common constants:

            l = 1.;
            l_x = l;
            l_y = l;

            m = 3;
            rad_circ = 1. / (4. * m + 2.);
            dist_circ = (l - m * 2 * rad_circ) / (m + 1);

            cl_rect = MESH_SIZE;
            cl_circ = MESH_SIZE;

            // -----------------------------------------------------------------
            // --- Main area (rectangle):

            x0 = 0;
            x1 = l_x;
            y0 = 0;
            y1 = l_y;
            cl = cl_rect;

            If (x0 >= x1 || y0 >= y1)
            Printf("Error!");
            // Exit;
            EndIf

            Point(1) = {x0, y0, 0, cl};
            Point(2) = {x1, y0, 0, cl};
            Point(3) = {x0, y1, 0, cl};
            Point(4) = {x1, y1, 0, cl};

            Line(1) = {1, 2};
            Line(2) = {1, 3};
            Line(3) = {2, 4};
            Line(4) = {3, 4};

            Line Loop(100) = {1, 3, -4, -2};


            // -----------------------------------------------------------------
            // --- Clipping area # 1 (circle):

            k_x = 1;
            k_y = 1;
            x_c = x0 + k_x * dist_circ + (k_x - 1) * 2 * rad_circ + rad_circ;
            y_c = y0 + k_y * dist_circ + (k_y - 1) * 2 * rad_circ + rad_circ;
            rad = rad_circ;
            cl = cl_circ;

            If (2 * rad >= x1 - x0 || 2 * rad >= y1 - y0)
            Printf("Error! Diameter is too large!");
            // Exit;
            EndIf

            Point(10) = {x_c, y_c, 0, cl};
            Point(11) = {x_c-rad, y_c, 0, cl};
            Point(12) = {x_c+rad, y_c, 0, cl};
            Point(13) = {x_c, y_c-rad, 0, cl};
            Point(14) = {x_c, y_c+rad, 0, cl};

            Circle(11) = {11, 10, 13};
            Circle(12) = {13, 10, 12};
            Circle(13) = {12, 10, 14};
            Circle(14) = {14, 10, 11};

            Line Loop(101) = {11, 12, 13, 14};


            // -----------------------------------------------------------------
            // --- Clipping area # 2 (circle):

            k_x = 1;
            k_y = 2;
            x_c = x0 + k_x * dist_circ + (k_x - 1) * 2 * rad_circ + rad_circ;
            y_c = y0 + k_y * dist_circ + (k_y - 1) * 2 * rad_circ + rad_circ;
            rad = rad_circ;
            cl = cl_circ;

            If (2 * rad >= x1 - x0 || 2 * rad >= y1 - y0)
            Printf("Error! Diameter is too large!");
            // Exit;
            EndIf

            Point(20) = {x_c, y_c, 0, cl};
            Point(21) = {x_c-rad, y_c, 0, cl};
            Point(22) = {x_c+rad, y_c, 0, cl};
            Point(23) = {x_c, y_c-rad, 0, cl};
            Point(24) = {x_c, y_c+rad, 0, cl};

            Circle(21) = {21, 20, 23};
            Circle(22) = {23, 20, 22};
            Circle(23) = {22, 20, 24};
            Circle(24) = {24, 20, 21};

            Line Loop(102) = {21, 22, 23, 24};


            // -----------------------------------------------------------------
            // --- Clipping area # 3 (circle):

            k_x = 1;
            k_y = 3;
            x_c = x0 + k_x * dist_circ + (k_x - 1) * 2 * rad_circ + rad_circ;
            y_c = y0 + k_y * dist_circ + (k_y - 1) * 2 * rad_circ + rad_circ;
            rad = rad_circ;
            cl = cl_circ;

            If (2 * rad >= x1 - x0 || 2 * rad >= y1 - y0)
            Printf("Error! Diameter is too large!");
            // Exit;
            EndIf

            Point(30) = {x_c, y_c, 0, cl};
            Point(31) = {x_c-rad, y_c, 0, cl};
            Point(32) = {x_c+rad, y_c, 0, cl};
            Point(33) = {x_c, y_c-rad, 0, cl};
            Point(34) = {x_c, y_c+rad, 0, cl};

            Circle(31) = {31, 30, 33};
            Circle(32) = {33, 30, 32};
            Circle(33) = {32, 30, 34};
            Circle(34) = {34, 30, 31};

            Line Loop(103) = {31, 32, 33, 34};


            // -----------------------------------------------------------------
            // --- Clipping area # 4 (circle):

            k_x = 2;
            k_y = 1;
            x_c = x0 + k_x * dist_circ + (k_x - 1) * 2 * rad_circ + rad_circ;
            y_c = y0 + k_y * dist_circ + (k_y - 1) * 2 * rad_circ + rad_circ;
            rad = rad_circ;
            cl = cl_circ;

            If (2 * rad >= x1 - x0 || 2 * rad >= y1 - y0)
            Printf("Error! Diameter is too large!");
            // Exit;
            EndIf

            Point(40) = {x_c, y_c, 0, cl};
            Point(41) = {x_c-rad, y_c, 0, cl};
            Point(42) = {x_c+rad, y_c, 0, cl};
            Point(43) = {x_c, y_c-rad, 0, cl};
            Point(44) = {x_c, y_c+rad, 0, cl};

            Circle(41) = {41, 40, 43};
            Circle(42) = {43, 40, 42};
            Circle(43) = {42, 40, 44};
            Circle(44) = {44, 40, 41};

            Line Loop(104) = {41, 42, 43, 44};


            // -----------------------------------------------------------------
            // --- Clipping area # 5 (circle):

            k_x = 2;
            k_y = 2;
            x_c = x0 + k_x * dist_circ + (k_x - 1) * 2 * rad_circ + rad_circ;
            y_c = y0 + k_y * dist_circ + (k_y - 1) * 2 * rad_circ + rad_circ;
            rad = rad_circ;
            cl = cl_circ;

            If (2 * rad >= x1 - x0 || 2 * rad >= y1 - y0)
            Printf("Error! Diameter is too large!");
            // Exit;
            EndIf

            Point(50) = {x_c, y_c, 0, cl};
            Point(51) = {x_c-rad, y_c, 0, cl};
            Point(52) = {x_c+rad, y_c, 0, cl};
            Point(53) = {x_c, y_c-rad, 0, cl};
            Point(54) = {x_c, y_c+rad, 0, cl};

            Circle(51) = {51, 50, 53};
            Circle(52) = {53, 50, 52};
            Circle(53) = {52, 50, 54};
            Circle(54) = {54, 50, 51};

            Line Loop(105) = {51, 52, 53, 54};


            // -----------------------------------------------------------------
            // --- Clipping area # 6 (circle):

            k_x = 2;
            k_y = 3;
            x_c = x0 + k_x * dist_circ + (k_x - 1) * 2 * rad_circ + rad_circ;
            y_c = y0 + k_y * dist_circ + (k_y - 1) * 2 * rad_circ + rad_circ;
            rad = rad_circ;
            cl = cl_circ;

            If (2 * rad >= x1 - x0 || 2 * rad >= y1 - y0)
            Printf("Error! Diameter is too large!");
            // Exit;
            EndIf

            Point(60) = {x_c, y_c, 0, cl};
            Point(61) = {x_c-rad, y_c, 0, cl};
            Point(62) = {x_c+rad, y_c, 0, cl};
            Point(63) = {x_c, y_c-rad, 0, cl};
            Point(64) = {x_c, y_c+rad, 0, cl};

            Circle(61) = {61, 60, 63};
            Circle(62) = {63, 60, 62};
            Circle(63) = {62, 60, 64};
            Circle(64) = {64, 60, 61};

            Line Loop(106) = {61, 62, 63, 64};


            // -----------------------------------------------------------------
            // --- Clipping area # 7 (circle):

            k_x = 3;
            k_y = 1;
            x_c = x0 + k_x * dist_circ + (k_x - 1) * 2 * rad_circ + rad_circ;
            y_c = y0 + k_y * dist_circ + (k_y - 1) * 2 * rad_circ + rad_circ;
            rad = rad_circ;
            cl = cl_circ;

            If (2 * rad >= x1 - x0 || 2 * rad >= y1 - y0)
            Printf("Error! Diameter is too large!");
            // Exit;
            EndIf

            Point(70) = {x_c, y_c, 0, cl};
            Point(71) = {x_c-rad, y_c, 0, cl};
            Point(72) = {x_c+rad, y_c, 0, cl};
            Point(73) = {x_c, y_c-rad, 0, cl};
            Point(74) = {x_c, y_c+rad, 0, cl};

            Circle(71) = {71, 70, 73};
            Circle(72) = {73, 70, 72};
            Circle(73) = {72, 70, 74};
            Circle(74) = {74, 70, 71};

            Line Loop(107) = {71, 72, 73, 74};


            // -----------------------------------------------------------------
            // --- Clipping area # 8 (circle):

            k_x = 3;
            k_y = 2;
            x_c = x0 + k_x * dist_circ + (k_x - 1) * 2 * rad_circ + rad_circ;
            y_c = y0 + k_y * dist_circ + (k_y - 1) * 2 * rad_circ + rad_circ;
            rad = rad_circ;
            cl = cl_circ;

            If (2 * rad >= x1 - x0 || 2 * rad >= y1 - y0)
            Printf("Error! Diameter is too large!");
            // Exit;
            EndIf

            Point(80) = {x_c, y_c, 0, cl};
            Point(81) = {x_c-rad, y_c, 0, cl};
            Point(82) = {x_c+rad, y_c, 0, cl};
            Point(83) = {x_c, y_c-rad, 0, cl};
            Point(84) = {x_c, y_c+rad, 0, cl};

            Circle(81) = {81, 80, 83};
            Circle(82) = {83, 80, 82};
            Circle(83) = {82, 80, 84};
            Circle(84) = {84, 80, 81};

            Line Loop(108) = {81, 82, 83, 84};


            // -----------------------------------------------------------------
            // --- Clipping area # 9 (circle):

            k_x = 3;
            k_y = 3;
            x_c = x0 + k_x * dist_circ + (k_x - 1) * 2 * rad_circ + rad_circ;
            y_c = y0 + k_y * dist_circ + (k_y - 1) * 2 * rad_circ + rad_circ;
            rad = rad_circ;
            cl = cl_circ;

            If (2 * rad >= x1 - x0 || 2 * rad >= y1 - y0)
            Printf("Error! Diameter is too large!");
            // Exit;
            EndIf

            Point(90) = {x_c, y_c, 0, cl};
            Point(91) = {x_c-rad, y_c, 0, cl};
            Point(92) = {x_c+rad, y_c, 0, cl};
            Point(93) = {x_c, y_c-rad, 0, cl};
            Point(94) = {x_c, y_c+rad, 0, cl};

            Circle(91) = {91, 90, 93};
            Circle(92) = {93, 90, 92};
            Circle(93) = {92, 90, 94};
            Circle(94) = {94, 90, 91};

            Line Loop(109) = {91, 92, 93, 94};


            // -----------------------------------------------------------------
            // --- Surfaces:

            Plane Surface(0) = {100, 101, 102, 103, 104, 105, 106, 107, 108, 109};
            Plane Surface(1) = {101};
            Plane Surface(2) = {102};
            Plane Surface(3) = {103};
            Plane Surface(4) = {104};
            Plane Surface(5) = {105};
            Plane Surface(6) = {106};
            Plane Surface(7) = {107};
            Plane Surface(8) = {108};
            Plane Surface(9) = {109};


            // -----------------------------------------------------------------
            // --- Physical entities:

            Physical Line(5001) = {1};    // Bottom boundary line
            Physical Line(5002) = {2};    // Left boundary line
            Physical Line(5003) = {3};    // Right boundary line
            Physical Line(5004) = {4};    // Top boundary line

            Physical Surface(6000) = {0}; // Square except circles
            Physical Surface(6001) = {1}; // Circle 1
            Physical Surface(6002) = {2}; // Circle 2
            Physical Surface(6003) = {3}; // Circle 3
            Physical Surface(6004) = {4}; // Circle 4
            Physical Surface(6005) = {5}; // Circle 5
            Physical Surface(6006) = {6}; // Circle 6
            Physical Surface(6007) = {7}; // Circle 7
            Physical Surface(6008) = {8}; // Circle 8
            Physical Surface(6009) = {9}; // Circle 9
        '''

        mesh = mesh.replace('        ', '')
        mesh = mesh.replace('MESH_SIZE', str(self.size))

        return mesh
