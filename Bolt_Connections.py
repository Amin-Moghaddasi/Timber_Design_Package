# Calculates reference design values for bolt fasteners (Z) + failure modes associated with bolted connections (Z_NT, Z_GT, and Z_RT)
from math import pow , sqrt, sin, cos, radians
class Single_shear_reference_Z:
    def __init__(self, D, bolt_length, t_m, t_s, side_member_type, G_s, F_e_s_um,
                 G_m , main_member_orientation ,side_member_orientation,
                 side_member_forge_type, angle_to_grain):
        """
        :param: D : Diameter of nail
        :param: bolt_length : Length of single bolt
        :param: t_m : Thickness of the main member
        :param: t_s : Thickness of the side member
        :param: side_member_type: 'W': Wood / engineered wood products
                                    'S': Steel
                                    'C': Concrete
        :param: G_s : Specific gravity of the side member
        :param: G_m : Specific gravity of the main member
        :param: F_e_s_um : Bearing strength of the side member (only steel and raw value)
        :param: main_member_orientation: Angle of main member relative to imposed force
        :param: side_member_orientation: Angle of side member relative to imposed force
        :param: side_member_forge_type: 'Cold' for cold formed; 'Hot' for hot rolled
        :param: angle_to_grain: Indicates the angle of force applied on the fastener to grain
        """
        if D <= 1:
            self.D = D
        else:
            self.D = 1
            print("Warning! the entered bolt diameter is out of bounds! ({d} > 1)".format(d=D)
                  ,'\n','The largest possible bolt diameter (1 in.) '
                        'was chosen automatically!')
        self.bolt_length = bolt_length
        self.t_m = t_m
        self.t_s = t_s
        self.l_s = t_s
        self.theta = angle_to_grain
        self.Theta_m = main_member_orientation
        self.Theta_s = side_member_orientation
        self.s_type = side_member_type
        self.G_s = G_s
        self.G_m = G_m
        self.s_forge_type = side_member_forge_type
        self.F_e_s_um = F_e_s_um
        self.F_yb = 45000


    def F_em(self):
        if self.D < 0.25:
            F_em_ = 16600 * pow(self.G_m, 1.84)
        elif self.Theta_m == 90:
            F_em_ = 6100 * pow(self.G_m, 1.45) * pow(self.D, -0.5)
        elif self.Theta_m == 0:
            F_em_ = 11200 * self.G_m
        else:
            F_em_par = 11200 * self.G_m
            F_em_perp = 6100 * pow(self.G_m, 1.45) * pow(self.D, -0.5)
            numerator = F_em_perp * F_em_par
            denominator = ((F_em_par * pow(sin(radians(self.Theta_m)),2)) +
                           (F_em_perp) * pow(cos(radians(self.Theta_m)),2))
            F_em_ = numerator / denominator
        return F_em_

    def F_es(self):
        if self.s_type == 'W':
            if self.D < 0.25:
                F_es_ = 16600 * pow(self.G_s, 1.84)
            elif self.Theta_s == 90:
                F_es_ = 6100 * pow(self.G_s, 1.45) * pow(self.D, -0.5)
            elif self.Theta_s == 0:
                F_es_ = 11200 * self.G_s
            else:
                F_es_par = 11200 * self.G_s
                F_es_perp = 6100 * pow(self.G_s, 1.45) * pow(self.D, -0.5)
                numerator = F_es_perp * F_es_par
                denominator = ((F_es_par * pow(sin(radians(self.Theta_m)), 2)) +
                               (F_es_perp) * pow(cos(radians(self.Theta_m)), 2))
                F_es_ = numerator / denominator
        elif self.s_type == 'S':
            if self.s_forge_type =='Hot':
                F_es_ = 1.50 * self.F_e_s_um
            else:
                F_es_ = 1.375 * self.F_e_s_um
        else:
            F_es_ = 7500
        return F_es_
    def R_e(self):
        R_e_ = self.F_em() / self.F_es()
        return R_e_
    def penetration(self):
        p = self.bolt_length - self.t_s
        if p >= (6 * self.D):
            print('The minimum penetration criteria satisfied!','\n')
        else:
            print('Error! The minimum penetration criteria not satisfied!'
                  '\n','Consider choosing different length value for the bolt!')
            return None
        return p
    def l_m(self):
        lm = self.t_m
        return lm
    def K_D(self):
        if self.D <= 0.17:
            KD = 2.20
        elif 0.17 < self.D < 0.25:
            KD = (10 * self.D) + 0.5
        else:
            print('Warning! Reduction factor (K_D) is not included! ({D} => 0.25 inches)'
                  .format(D=self.D),'\n','K_D = 1.00')
            KD = 1.00
        return KD
    def K_theta(self):
        K_theta_ = 1 + (0.25 * (self.theta / 90))
        return K_theta_
    def R_t(self):
        Rt = self.l_m() / self.l_s
        return Rt
    def k1(self):
        a = sqrt((self.R_e()) + (2 * pow(self.R_e(),2)) * (1 + self.R_t() + pow(self.R_t(), 2))
                 + (pow(self.R_t(), 2) * pow(self.R_e(), 3)))
        b = self.R_e() * (1 + self.R_t())
        c = 1 + self.R_e()
        k_1 = (a - b) / c
        return k_1
    def k2(self):
        a = (2 * self.F_yb) * (1 + (2 * self.R_e())) * pow(self.D, 2)
        b = (3 * self.F_em() * pow(self.l_m(), 2))
        c = 2 * (1 + self.R_e())
        k_2 = -1 + sqrt(c + (a / b))
        return k_2
    def k3(self):
        a = 2 * (1 + self.R_e())
        b = (2 * self.F_yb) * (1 + (2 * self.R_e())) * pow(self.D, 2)
        c = (3 * self.F_em() * pow(self.l_s, 2))
        k_3 = -1 + sqrt((a / self.R_e()) + (b / c))
        return k_3
    def Z_I_m(self):
        if self.D < 0.25:
            Z_I_m_ = (self.D * self.l_m() * self.F_em()) / self.K_D()
        elif 0.25 <= self.D <= 1:
            Z_I_m_ = (self.D * self.l_m() * self.F_em()) / (4 * self.K_theta())
        else:
            print('Error! Bolt diameter is larger than 1 inch!')
            Z_I_m_ = 0
        return Z_I_m_
    def Z_I_s(self):
        if self.D < 0.25:
            Z_I_s_ = (self.D * self.l_s * self.F_es()) / self.K_D()
        elif 0.25 <= self.D <= 1:
            Z_I_s_ = (self.D * self.l_s * self.F_es()) / (4 * self.K_theta())
        else:
            print('Error! Bolt diameter is larger than 1 inch!')
            Z_I_s_ = 0
        return Z_I_s_
    def Z_II(self):
        if self.D < 0.25:
            Z_II_ = (self.k1() * self.D * self.l_s * self.F_es()) / self.K_D()
        elif 0.25 <= self.D <= 1:
            Z_II_ = (self.k1() * self.D * self.l_s * self.F_es()) / (3.6 * self.K_theta())
        else:
            print('Error! Bolt diameter is larger than 1 inch!')
            Z_II_ = 0
        return Z_II_
    def Z_III_m(self):
        if self.D < 0.25:
            Z_III_m_ = ((self.k2() * self.D * self.l_m() * self.F_em()) /
                        ((1 + (2 * self.R_e())) * self.K_D()))
        elif 0.25 <= self.D <= 1:
            Z_III_m_ = ((self.k2() * self.D * self.l_m() * self.F_em()) /
                        ((1 + (2 * self.R_e())) * (3.2 * self.K_theta())))
        else:
            print('Error! Bolt diameter is larger than 1 inch!')
            Z_III_m_ = 0
        return Z_III_m_
    def Z_III_s(self):
        if self.D < 0.25:
            Z_III_s_ = ((self.k3() * self.D * self.l_s * self.F_em()) /
                        ((2 + self.R_e()) * self.K_D()))
        elif 0.25 <= self.D <= 1:
            Z_III_s_ = ((self.k3() * self.D * self.l_s * self.F_em()) /
                        ((2 + self.R_e()) * (3.2 * self.K_theta())))
        else:
            print('Error! Bolt diameter is larger than 1 inch!')
            Z_III_s_ = 0
        return Z_III_s_
    def Z_IV(self):
        a = 2 * self.F_em() * self.F_yb
        b = 3 * (1 + self.R_e())
        if self.D < 0.25:
            Z_IV_ = (pow(self.D , 2) / self.K_D()) * sqrt(a / b)
        elif 0.25 <= self.D <= 1:
            Z_IV_ = (pow(self.D, 2) / (3.2 * self.K_theta())) * sqrt(a / b)
        else:
            print('Error! Bolt diameter is larger than 1 inch!')
            Z_IV_ = 0
        return Z_IV_
    def reference_Z(self):
        Z = [self.Z_I_m(),self.Z_I_s(),self.Z_II(),self.Z_III_m(),self.Z_III_s(),self.Z_IV()]
        Z.sort(key=None,reverse=False)
        return Z[0]
class Double_shear_reference_Z:
    def __init__(self, D, bolt_length, t_m, t_s, side_member_type, G_s, F_e_s_um,
                 G_m , main_member_orientation ,side_member_orientation,
                 side_member_forge_type, angle_to_grain):
        """
        :param: D : Diameter of nail
        :param: bolt_length : Length of single bolt
        :param: t_m : Thickness of the main member
        :param: t_s : Thickness of the side member
        :param: side_member_type: 'W': Wood / engineered wood products
                                    'S': Steel
                                    'C': Concrete
        :param: G_s : Specific gravity of the side member
        :param: G_m : Specific gravity of the main member
        :param: F_e_s_um : Bearing strength of the side member (only steel and raw value)
        :param: main_member_orientation: Angle of main member relative to imposed force
        :param: side_member_orientation: Angle of side member relative to imposed force
        :param: side_member_forge_type: 'Cold' for cold formed; 'Hot' for hot rolled
        :param: angle_to_grain: Indicates the angle of force applied on the fastener to grain
        """
        if D <= 1:
            self.D = D
        else:
            self.D = 1
            print("Warning! the entered bolt diameter is out of bounds! ({d} > 1)".format(d=D)
                  ,'\n','The largest possible bolt diameter (1 in.) '
                        'was chosen automatically!')
        self.bolt_length = bolt_length
        self.t_m = t_m
        self.t_s = t_s
        self.l_s = t_s
        self.theta = angle_to_grain
        self.Theta_m = main_member_orientation
        self.Theta_s = side_member_orientation
        self.s_type = side_member_type
        self.G_s = G_s
        self.G_m = G_m
        self.s_forge_type = side_member_forge_type
        self.F_e_s_um = F_e_s_um
        self.F_yb = 45000


    def F_em(self):
        if self.D < 0.25:
            F_em_ = 16600 * pow(self.G_m, 1.84)
        elif self.Theta_m == 90:
            F_em_ = 6100 * pow(self.G_m, 1.45) * pow(self.D, -0.5)
        elif self.Theta_m == 0:
            F_em_ = 11200 * self.G_m
        else:
            F_em_par = 11200 * self.G_m
            F_em_perp = 6100 * pow(self.G_m, 1.45) * pow(self.D, -0.5)
            numerator = F_em_perp * F_em_par
            denominator = ((F_em_par * pow(sin(radians(self.Theta_m)),2)) +
                           (F_em_perp) * pow(cos(radians(self.Theta_m)),2))
            F_em_ = numerator / denominator
        return F_em_

    def F_es(self):
        if self.s_type == 'W':
            if self.D < 0.25:
                F_es_ = 16600 * pow(self.G_s, 1.84)
            elif self.Theta_s == 90:
                F_es_ = 6100 * pow(self.G_s, 1.45) * pow(self.D, -0.5)
            elif self.Theta_s == 0:
                F_es_ = 11200 * self.G_s
            else:
                F_es_par = 11200 * self.G_s
                F_es_perp = 6100 * pow(self.G_s, 1.45) * pow(self.D, -0.5)
                numerator = F_es_perp * F_es_par
                denominator = ((F_es_par * pow(sin(radians(self.Theta_m)), 2)) +
                               (F_es_perp) * pow(cos(radians(self.Theta_m)), 2))
                F_es_ = numerator / denominator
        elif self.s_type == 'S':
            if self.s_forge_type =='Hot':
                F_es_ = 1.50 * self.F_e_s_um
            else:
                F_es_ = 1.375 * self.F_e_s_um
        else:
            F_es_ = 7500
        return F_es_
    def R_e(self):
        R_e_ = self.F_em() / self.F_es()
        return R_e_
    def penetration(self):
        p = self.bolt_length - self.t_s
        if p >= (6 * self.D):
            print('The minimum penetration criteria satisfied!','\n')
        else:
            print('Error! The minimum penetration criteria not satisfied!'
                  '\n','Consider choosing different length value for the bolt!')
            return None
        return p
    def l_m(self):
        lm = self.t_m
        return lm
    def K_D(self):
        if self.D <= 0.17:
            KD = 2.20
        elif 0.17 < self.D < 0.25:
            KD = (10 * self.D) + 0.5
        else:
            print('Warning! Reduction factor (K_D) is not included! ({D} => 0.25 inches)'
                  .format(D=self.D),'\n','K_D = 1.00')
            KD = 1.00
        return KD
    def K_theta(self):
        K_theta_ = 1 + (0.25 * (self.theta / 90))
        return K_theta_
    def R_t(self):
        Rt = self.l_m() / self.l_s
        return Rt
    def k1(self):
        a = sqrt((self.R_e()) + (2 * pow(self.R_e(),2)) * (1 + self.R_t() + pow(self.R_t(), 2))
                 + (pow(self.R_t(), 2) * pow(self.R_e(), 3)))
        b = self.R_e() * (1 + self.R_t())
        c = 1 + self.R_e()
        k_1 = (a - b) / c
        return k_1
    def k2(self):
        a = (2 * self.F_yb) * (1 + (2 * self.R_e())) * pow(self.D, 2)
        b = (3 * self.F_em() * pow(self.l_m(), 2))
        c = 2 * (1 + self.R_e())
        k_2 = -1 + sqrt(c + (a / b))
        return k_2
    def k3(self):
        a = 2 * (1 + self.R_e())
        b = (2 * self.F_yb) * (2 +  self.R_e()) * pow(self.D, 2)
        c = (3 * self.F_em() * pow(self.l_s, 2))
        k_3 = -1 + sqrt((a / self.R_e()) + (b / c))
        return k_3
    def Z_I_m(self):
        if self.D < 0.25:
            Z_I_m_ = (self.D * self.l_m() * self.F_em()) / self.K_D()
        elif 0.25 <= self.D <= 1:
            Z_I_m_ = (self.D * self.l_m() * self.F_em()) / (4 * self.K_theta())
        else:
            print('Error! Bolt diameter is larger than 1 inch!')
            Z_I_m_ = 0
        return Z_I_m_
    def Z_I_s(self):
        if self.D < 0.25:
            Z_I_s_ = (2 * self.D * self.l_s * self.F_es()) / self.K_D()
        elif 0.25 <= self.D <= 1:
            Z_I_s_ = (2 * self.D * self.l_s * self.F_es()) / (4 * self.K_theta())
        else:
            print('Error! Bolt diameter is larger than 1 inch!')
            Z_I_s_ = 0
        return Z_I_s_
    def Z_III_s(self):
        if self.D < 0.25:
            Z_III_s_ = ((2 * self.k3() * self.D * self.l_s * self.F_em()) /
                        ((2 + self.R_e()) * self.K_D()))
        elif 0.25 <= self.D <= 1:
            Z_III_s_ = ((2 * self.k3() * self.D * self.l_s * self.F_em()) /
                        ((2 + self.R_e()) * (3.2 * self.K_theta())))
        else:
            print('Error! Bolt diameter is larger than 1 inch!')
            Z_III_s_ = 0
        return Z_III_s_
    def Z_IV(self):
        a = 2 * self.F_em() * self.F_yb
        b = 3 * (1 + self.R_e())
        if self.D < 0.25:
            Z_IV_ = (2 * pow(self.D , 2) / self.K_D()) * sqrt(a / b)
        elif 0.25 <= self.D <= 1:
            Z_IV_ = (2 * pow(self.D, 2) / (3.2 * self.K_theta())) * sqrt(a / b)
        else:
            print('Error! Bolt diameter is larger than 1 inch!')
            Z_IV_ = 0
        return Z_IV_
    def reference_Z(self):
        Z = [self.Z_I_m(),self.Z_I_s(),self.Z_III_s(),self.Z_IV()]
        Z.sort(key=None,reverse=False)
        return Z[0]

class Modified_Z_Value:
    def __init__(self, P,lamda, Z, Moisture_content_fab,
                 Moisture_content_service, D, temperature,
                 connection_type, A_m, A_s, E_m, E_s, n, s, load_type, load_orientation,
                 species_type, l_m, l_s, end_distance, edge_distance,
                 row_spacing, edge_type, bolt_row_list, height, breadth, F_v_n_prime,
                 F_t_n_prime):
        """
        :param: P: Lateral imposed force
        :param: lamda : Time effect factor (LRFD only)
        :param: Z: Reference lateral design value for nails
        :param: Moisture_content_fab: 19 % or less is dry at the time of fabrication
        :param: Moisture_content_service: 19 % or less is dry at service
        :param: D : Diameter of nails
        :param: temperature: Working temperature in degrees of Fahrenheit
        :param: connection_type: 'WW': wood-to-wood; 'WS': wood-to-steel
        :param: A_m: Gross cross-sectional area of the main member
        :param: A_s: Gross cross-sectional area of the side member
        :param: E_m: Modulus of elasticity of the main member
        :param: E_s: Modulus of elasticity of the side member
        :param: n: Number of fasteners in a row
        :param: s: Spacing between fasteners in a row
        :param: load_type: 'C' for compression; 'T' for tension
        :param: load_orientation : 'Par' for parallel to grain
                                    'Perp' for perpendicular to grain
        :param: species_type: 'HW' for hardwood ; 'SW' for softwood
        :param: l_m: Length of a single bolt in main member
        :param: l_s: Length of a single bolt in side member
        :param: end_distance: Distance of first bolt from edge (parallel-to-grain)
        :param: edge_distance: Distance of first bolt from edge (perpendicular-to-grain)
        :param: row_spacing: Distance between bolt rows (perpendicular-to-grain)
        :param: edge_type: Indicates whether the edge is loaded ('L' or 'UL')
        :param: bolt_row_list: List containing number of bolts in every row
        :param: height : Height of wooden member
        :param: breadth: breadth of wooden member
        :param: F_t_n_prime : Modified unit tensile capacity of the wooden member
        :param: F_v_n_prime: Modified unit shearing capacity of the wooden member
        """
        self.height = height
        self.breadth = breadth
        self.F_t_n_prime = F_t_n_prime
        self.F_v_n_prime = F_v_n_prime
        self.A_net = breadth * (height - (len(bolt_row_list)*(D + (1 / 16))))
        self.A_net_group = (row_spacing - ((len(bolt_row_list)-1) * (D + (1/16))) ) * breadth
        self.bolt_row_list = bolt_row_list
        self.edge_type = edge_type
        self.end_distance = end_distance
        self.edge_distance = edge_distance
        self.row_spacing = row_spacing
        self.load_type = load_type
        self.load_orientation = load_orientation
        self.species_type = species_type
        self.l_s = l_s
        self.l_m = l_m
        self.A_m = A_m
        self.A_s = A_s
        self.E_m = E_m
        self.E_s = E_s
        self.s = s
        self.n = n
        self.P = P
        if connection_type == 'WW':
            self.gama = 180000 * pow(D, 1.5)
        else:
            self.gama = 270000 * pow(D, 1.5)
        self.lamda = lamda
        self.Phi_z = 0.65
        self.K_F = 3.32
        self.MC_fab = Moisture_content_fab
        self.MC_svc = Moisture_content_service
        self.D = D
        self.temperature = temperature
        self.Z = Z
        if self.MC_svc <= 0.19:
            self.Moisture_condition = False
        else:
            self.Moisture_condition = True
        if self.s >= self.end_distance:
            self.s_crit = self.end_distance
        else:
            self.s_crit = self.s
    def R_EA(self):
        a = (self.E_s * self.A_s) / (self.E_m * self.A_m)
        if a >= (1/a):
            R_EA_ = 1 / a
        else:
            R_EA_ = a
        return R_EA_
    def C_g(self):
        u = 1 + (self.gama * self.s * 0.5 *
                 ((1 / (self.A_s * self.E_s))+(1 / (self.A_m * self.E_m))))
        m = u - sqrt(pow(u, 2) - 1)
        a = m * (1 - (pow(m, (2 * self.n))))
        b = self.n * (((1 + (self.R_EA() * pow(m, self.n)))*(1 + m ))
                      - 1 + (pow(m, (2 * self.n))))
        c = 1 + self.R_EA()
        d = 1 - m
        C_g_ = (a / b) * (c / d)
        return C_g_
    def C_M(self):
        if self.MC_fab <= 0.19:
            if self.MC_svc <= 0.19:
                C_M_ = 1.0
            else:
                C_M_ = 0.7
        elif self.MC_fab > 0.19 and self.MC_svc <= 0.19:
            if self.D <= 0.25 :
                C_M_ = 0.7
            else:
                C_M_ = 0.4
        else:
            C_M_ = 0.7
        return C_M_
    def C_t(self):
        if self.Moisture_condition:
            if self.temperature <= 100:
                C_t_ = 1.00
            elif 100 < self.temperature <= 125:
                C_t_ = 0.70
            else:
                C_t_ = 0.50
        else:
            if self.temperature <= 100:
                C_t_ = 1.00
            elif 100 < self.temperature <= 125:
                C_t_ = 0.80
            else:
                C_t_ = 0.70
        return C_t_
    def bolt_slenderness_ratio(self):
        if self.l_s <= self.l_m:
            sr = self.l_s / self.D
        else:
            sr = self.l_m / self.D
        return sr
    def C_Delta(self):
        if self.load_orientation == 'Par':
            if self.load_type =='T':
                if self.species_type == 'SW':
                    C_Delta_1 = self.end_distance / (3.5 * self.D)
                else:
                    C_Delta_1 = self.end_distance / (2.5 * self.D)
            else:
                C_Delta_1 = self.end_distance / (4 * self.D)
            if self.bolt_slenderness_ratio() <= 6.0:
                C_Delta_2 = self.edge_distance / (1.5 * self.D)
            else:
                if (0.5 * self.s) >= (1.5 * self.D):
                    C_Delta_2 = self.edge_distance / (0.5 * self.s)
                else:
                    C_Delta_2 = self.edge_distance / (1.5 * self.D)
            C_Delta_3 = self.s / (3 * self.D)
            C_Delta_4 = self.row_spacing / (1.5 * self.D)
        else:
            C_Delta_1 = self.end_distance / (2 * self.D)
            if self.edge_type =='L':

                C_Delta_2 = self.edge_distance / (4 * self.D)
            else:
                C_Delta_2 = self.edge_distance / (1.5 * self.D)
            C_Delta_3 = self.s / (3 * self.D)
            if self.bolt_slenderness_ratio() <= 2.0:
                C_Delta_4 = self.row_spacing / (2.5 * self.D)
            else:
                m = ((5 / 8) * self.bolt_slenderness_ratio()) + 1.25
                C_Delta_4 = self.row_spacing / (m * self.D)

        C_Delta_range = [C_Delta_1, C_Delta_2, C_Delta_3, C_Delta_4]
        C_Delta_range.sort(key=None,reverse=False)
        return C_Delta_range [0]
    def Z_n_Prime(self):
        Z_n = self.Z * self.K_F
        Z_n_prime = (Z_n * self.lamda * self.Phi_z * self.C_M() *
                     self.C_g() * self.C_t() * self.C_Delta())
        return Z_n_prime
    def Z_RT_prime(self):
        Z_RT_prime_ = 0
        for i in range(len(self.bolt_row_list)):
            Z_RT_prime_ += (self.bolt_row_list [i] *
                            self.F_v_n_prime * self.breadth * self.s_crit)
        return Z_RT_prime_
    def Z_NT_prime(self):
        Z_NT_prime_ = self.F_t_n_prime * self.A_net
        return Z_NT_prime_
    def Z_GT_prime(self):
        Z_RT_prime_1 = (self.bolt_row_list [0] *
                        self.F_v_n_prime * self.breadth * self.s_crit)
        Z_RT_prime_n = (self.bolt_row_list [-1] *
                        self.F_v_n_prime * self.breadth * self.s_crit)
        Z_GT_prime_ = ((Z_RT_prime_1 / 2) + (Z_RT_prime_n / 2) +
                       (self.F_t_n_prime * self.A_net_group))
        return Z_GT_prime_
    def Number_of_bolts(self):
        N = int(self.P / self.Z_n_Prime()) + 1
        return N
