class Design_check:
    def __init__(self, M_x_max,
                 M_y_max, V_x_max, V_y_max,N_max, T_max, F_b_n_prime,
                 F_c_perp_n_prime, F_c_parallel_n_prime, F_v_n_prime, F_t_n_prime,
                 I_x, I_y, c_x, c_y, Q_x, Q_y, breadth, height):
        """
        :param M_x_max:
        :param M_y_max:
        :param V_x_max:
        :param V_y_max:
        :param N_max:
        :param T_max:
        :param F_b_n_prime:
        :param F_c_perp_n_prime:
        :param F_c_parallel_n_prime:
        :param F_v_n_prime:
        :param F_t_n_prime:
        :param I_x:
        :param I_y:
        :param c_x:
        :param c_y:
        :param Q_x:
        :param Q_y:
        :param breadth:
        :param height:
        """
        self.Fb = F_b_n_prime
        self.Fv = F_v_n_prime
        self.Fc_perp = F_c_perp_n_prime
        self.Fc = F_c_parallel_n_prime
        self.Ft = F_t_n_prime
        self.M_x_max = M_x_max
        self.M_y_max = M_y_max
        self.V_x_max = V_x_max
        self.V_y_max = V_y_max
        self.N_max = N_max
        self.T_max = T_max
        self.I_x = I_x
        self.I_y = I_y
        self.c_x = c_x
        self.c_y = c_y
        self.Q_x = Q_x
        self.Q_y = Q_y
        self.breadth = breadth
        self.height = height
    def Bending_Design_Check_x(self):
        F_b_x = (self.M_x_max * self.c_x) / self.I_x
        if F_b_x <= self.Fb:
            print('*************************************')
            print("Bending capacity check (x-Axis): O. K.",'\n'
                  ,'F_b_n_prime = {fbn} psi >'.format(fbn=self.Fb),
                  'Bending stress = {bc} psi'.format(bc=F_b_x))
            Bending_Design_Check = True
        else:
            print('*************************************')
            print("Bending capacity check (x-Axis): Failed ", '\n'
                  , 'F_b_n_prime = {fbn} psi <'.format(fbn=self.Fb),
                  'Bending stress = {bc} psi'.format(bc=F_b_x))
            Bending_Design_Check = False
        return Bending_Design_Check
    def Bending_Design_Check_y(self):
        F_b_y = (self.M_y_max * self.c_y) / self.I_y
        if F_b_y <= self.Fb:
            print('*************************************')
            print("Bending capacity check (y-Axis): O. K.",'\n'
                  ,'F_b_n_prime = {fbn} psi >'.format(fbn=self.Fb),
                  'Bending stress = {bc} psi'.format(bc=F_b_y))
            Bending_Design_Check = True
        else:
            print('*************************************')
            print("Bending capacity check (y-Axis): Failed ", '\n'
                  , 'F_b_n_prime = {fbn} psi <'.format(fbn=self.Fb),
                  'Bending stress = {bc} psi'.format(bc=F_b_y))
            Bending_Design_Check = False

        return Bending_Design_Check
    def Shear_Design_Check_x(self):
        F_v_x = (self.V_x_max * self.Q_x) / (self.I_x * self.breadth)
        if F_v_x <= self.Fv:
            print('*************************************')
            print("Shear capacity check (x-Axis): O. K.",'\n'
                  ,'F_v_n_prime = {fvn} psi >'.format(fvn=self.Fv),
                  'Shearing stress = {tao} psi'.format(tao=F_v_x))
            Shear_Design_Check = True
        else:
            print('*************************************')
            print("Shear capacity check (x-Axis): Failed ", '\n'
                  , 'F_v_n_prime = {fvn} psi <'.format(fvn=self.Fv),
                  'Shear stress = {tao} psi'.format(tao=F_v_x))
            Shear_Design_Check = False
        return Shear_Design_Check
    def Shear_Design_Check_y(self):
        F_v_y = (self.V_y_max * self.Q_y) / (self.I_y * self.height)
        if F_v_y <= self.Fv:
            print('*************************************')
            print("Shear capacity check (y-Axis): O. K.",'\n'
                  ,'F_v_n_prime = {fvn} psi >'.format(fvn=self.Fv),
                  'Shearing stress = {tao} psi'.format(tao=F_v_y))
            Shear_Design_Check = True
        else:
            print('*************************************')
            print("Shear capacity check (y-Axis): Failed ", '\n'
                  , 'F_v_n_prime = {fvn} psi <'.format(fvn=self.Fv),
                  'Shear stress = {tao} psi'.format(tao=F_v_y))
            Shear_Design_Check = False
        return Shear_Design_Check
    def Axial_Compressive_Design_Check(self):
        F_c_parallel = (self.N_max) / (self.breadth * self.height)
        if F_c_parallel <= self.Fc:
            print('*************************************')
            print("Axial compressive capacity check : O. K.",'\n'
                  ,'F_c_n_prime_parallel = {fcn} psi >'.format(fcn=self.Fc)
                  ,'Axial stress = {sigma} psi'.format(sigma=F_c_parallel))
            Axial_Compressive_Design_Check = True
        else:
            print('*************************************')
            print("Axial compressive capacity check : Failed ", '\n'
                  ,'F_c_n_prime = {fcn} psi <'.format(fcn=self.Fc)
                  ,'Axial stress = {tao} psi'.format(tao=F_c_parallel))
            Axial_Compressive_Design_Check = False
        return Axial_Compressive_Design_Check
    def Axial_Tensile_Design_Check(self):
        F_t = (self.T_max) / (self.breadth * self.height)
        if F_t <= self.Ft:
            print('*************************************')
            print("Axial tensile capacity check : O. K.",'\n'
                  ,'F_t_n_prime = {ftn} psi >'.format(ftn=self.Ft)
                  ,'Axial stress = {sigma} psi'.format(sigma=F_t))
            Axial_Tensile_Design_Check = True
        else:
            print('*************************************')
            print("Axial Tensile capacity check : Failed ", '\n'
                  ,'F_t_n_prime = {ftn} psi <'.format(ftn=self.Ft)
                  ,'Axial stress = {sigma} psi'.format(tao=F_t))
            Axial_Tensile_Design_Check = False
        return Axial_Tensile_Design_Check
