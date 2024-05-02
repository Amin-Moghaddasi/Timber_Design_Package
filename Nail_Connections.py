# Calculates reference design values for nail fasteners (Z)
from math import pow , sqrt
class Single_shear_reference_Z:
    def __init__(self, D, nail_length, t_m, t_s, side_member_type, G_s,
                 G_m, Fe_s, nail_thread_status):
        """
        :param: D : Diameter of nail
        :param: nail_length : Length of nail
        :param: t_m : Thickness of the main member
        :param: t_s : Thickness of the side member
        :param: side_member_type: 'W': Wood / engineered wood products
                                    'S': Steel
        :param: G_s : Specific gravity of the side member
        :param: G_m : Specific gravity of the main member
        :param: F_es : Bearing strength of the side member
        :param: nail_thread_status: Indicates the existence of threads ond nail shank
        """
        if D <= 0.263:
            self.D = D
        else:
            self.D = 0.263
            print("Warning! the entered nail diameter is out of bounds! ({d} > 0.263)".format(d=D)
                  ,'\n','The largest possible nail diameter (0.263 in.) '
                        'was chosen automatically!')
        self.nail_length = nail_length
        self.t_m = t_m
        self.t_s = t_s
        self.Fe_m = 16600 * pow(G_m, 1.84)
        if side_member_type == 'W':
            self.Fe_s = 16600 * pow(G_s, 1.84)
        else:
            self.Fe_s = 1.375 * Fe_s
        self.l_s = t_s
        self.R_e = self.Fe_m / self.Fe_s
        self.thread_status = nail_thread_status


    def penetration(self):
        p = self.nail_length - self.t_s
        if p >= (6 * self.D):
            print('The minimum penetration criteria satisfied!','\n')
        else:
            print('Error! The minimum penetration criteria not satisfied!'
                  '\n','Consider choosing different length value for the nail!')
            return None
        return p
    def l_m(self):
        lm = self.nail_length - self.t_s -self.D
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
    def R_t(self):
        Rt = self.l_m() / self.l_s
        return Rt
    def F_yb(self):
        if self.thread_status:
            Fyb = (1.30 * (130.4 - 213.90 * self.D)) * 1000
        else:
            Fyb = (130.4 - 213.90 * self.D) * 1000
        return Fyb
    def k1(self):
        a = sqrt((self.R_e) + (2 * pow(self.R_e,2)) * (1 + self.R_t() + pow(self.R_t(), 2))
                 + (pow(self.R_t(), 2) * pow(self.R_e, 3)))
        b = self.R_e * (1 + self.R_t())
        c = 1 + self.R_e
        k_1 = (a - b) / c
        return k_1
    def k2(self):
        a = (2 * self.F_yb()) * (1 + (2 * self.R_e)) * pow(self.D, 2)
        b = (3 * self.Fe_m * pow(self.l_m(), 2))
        c = 2 * (1 + self.R_e)
        k_2 = -1 + sqrt(c + (a / b))
        return k_2
    def k3(self):
        a = 2 * (1 + self.R_e)
        b = (2 * self.F_yb()) * (1 + (2 * self.R_e)) * pow(self.D, 2)
        c = (3 * self.Fe_m * pow(self.l_s, 2))
        k_3 = -1 + sqrt((a / self.R_e) + (b / c))
        return k_3
    def Z_I_m(self):
        Z_I_m_ = (self.D * self.l_m() * self.Fe_m) / self.K_D()
        return Z_I_m_
    def Z_I_s(self):
        Z_I_s_ = (self.D * self.l_s * self.Fe_s) / self.K_D()
        return Z_I_s_
    def Z_II(self):
        Z_II_ = (self.k1() * self.D * self.l_s * self.Fe_s) / self.K_D()
        return Z_II_
    def Z_III_m(self):
        Z_III_m_ = ((self.k2() * self.D * self.l_m() * self.Fe_m) /
                    ((1 + (2 * self.R_e)) * self.K_D()))
        return Z_III_m_
    def Z_III_s(self):
        Z_III_s_ = (self.k3() * self.D * self.l_s * self.Fe_m) / ((2 + self.R_e) * self.K_D())
        return Z_III_s_
        return Z_III_s_
    def Z_IV(self):
        a = 2 * self.Fe_m * self.F_yb()
        b = 3 * (1 + self.R_e)
        Z_IV_ = (pow(self.D , 2) / self.K_D()) * sqrt(a / b)
        return Z_IV_
    def reference_Z(self):
        Z = [self.Z_I_m(),self.Z_I_s(),self.Z_II(),self.Z_III_m(),self.Z_III_s(),self.Z_IV()]
        Z.sort(key=None,reverse=False)
        return Z[0]

class Modified_Z_Value:
    def __init__(self, P,lamda, Z, Moisture_content_fab,
                 Moisture_content_service, D, temperature, grain_status, Nail_angle):
        """
        :param: P: Lateral imposed force
        :param: lamda : Time effect factor (LRFD only)
        :param: Z: Reference lateral design value for nails
        :param: Moisture_content_fab: 19 % or less is dry at the time of fabrication
        :param: Moisture_content_service: 19 % or less is dry at service
        :param: D : Diameter of nails
        :param: temperature: Working temperature in degrees of Fahrenheit
        :param: grain_status: Indicates whether the connection is side grain or not
        :param: Nail_angle : Angle of nail with respect to horizon
        """
        self.P = P
        self.lamda = lamda
        self.Phi_z = 0.65
        self.K_F = 3.32
        self.MC_fab = Moisture_content_fab
        self.MC_svc = Moisture_content_service
        self.D = D
        self.temperature = temperature
        self.Z = Z
        if Nail_angle == 90:
            self.C_tn = 1.00
        else:
            self.C_tn = 0.83
        if self.MC_svc <= 0.19:
            self.Moisture_condition = False
        else:
            self.Moisture_condition = True
        if grain_status:
            self.C_eg = 1.00
        else:
            self.C_eg = 0.67
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
    def Z_n_Prime(self):
        Z_n = self.Z * self.K_F
        Z_n_prime = (Z_n * self.lamda * self.Phi_z * self.C_M() *
                     self.C_eg * self.C_t() * self.C_tn)
        return Z_n_prime
    def Number_of_nails(self):
        N = int(self.P / self.Z_n_Prime()) + 1
        return N
class Modified_W_Values:
    def __init__(self, P,lamda, Moisture_content_fab,
                 Moisture_content_service, D, D_H, W, W_H,
                 temperature, grain_status, Nail_angle, nail_length, t_s):
        """
        :param: P: Lateral imposed force
        :param: lamda : Time effect factor (LRFD only)
        :param: Moisture_content_fab: 19 % or less is dry at the time of fabrication
        :param: Moisture_content_service: 19 % or less is dry at service
        :param: D : Diameter of nails
        :param: D_H : Diameter of nail heads
        :param: W : Reference withdrawal force value (per single nail)
        :param: W_H: Reference head pull force value (per single nail)
        :param: temperature: Working temperature in degrees of Fahrenheit
        :param: grain_status: Indicates whether the connection is side grain or not
        :param: Nail_angle : Angle of nail with respect to horizon
        :param: nail_length : Length of the nail
        :param: t_s: Thickness of the side member
        """
        self.P = P
        self.lamda = lamda
        self.Phi_z = 0.65
        self.K_F = 3.32
        self.MC_fab = Moisture_content_fab
        self.MC_svc = Moisture_content_service
        self.D = D
        self.D_H = D_H
        self.W = W
        self.W_H = W_H
        self.temperature = temperature
        if Nail_angle == 90:
            self.C_tn = 1.00
        else:
            self.C_tn = 0.67
        if self.MC_svc <= 0.19:
            self.Moisture_condition = False
        else:
            self.Moisture_condition = True
        if grain_status:
            self.C_eg = 1.00
        else:
            self.C_eg = 0.67
        self.t_s = t_s
        self.nail_length = nail_length
    def penetration(self):
        p = self.nail_length - self.t_s
        return p
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
    def W_H_n_prime(self):
        W_H_n = self.K_F * self.W_H * self.penetration()
        W_H_n_prime = W_H_n * self.lamda * self.C_M() * self.C_t() * self.C_tn * self.C_eg
        return  W_H_n_prime
    def W_n_prime(self):
        W_n = self.K_F * self.W * self.penetration()
        W_n_prime = W_n * self.lamda * self.C_M() * self.C_t() * self.C_tn * self.C_eg
        return W_n_prime
    def Number_of_nails_withdrawal(self):
        N = int (self.P / self.W_n_prime()) + 1
        return N
    def Number_of_nails_head_pull(self):
        N = int (self.P / self.W_H_n_prime()) + 1
        return N
    def final_number_of_nails(self):
        if self.Number_of_nails_withdrawal() >= self.Number_of_nails_head_pull():
            N = self.Number_of_nails_withdrawal()
            print('Withdrawal happens sooner than head pull ({W} => {W_H} '
                  .format(W=self.W_n_prime(),W_H=self.W_H_n_prime()))
        else:
            N = self.Number_of_nails_head_pull()
            print('Head pull happens sooner than withdrawal ({W_H} => {W} '
                  .format(W=self.W_n_prime(), W_H=self.W_H_n_prime()))
        return N
