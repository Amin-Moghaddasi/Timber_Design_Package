from math import pow
from math import sqrt

class Section_Tools:  # Error checks for unsuitable vlues are added to each function
    def __init__(self, breadth, height, c_x, c_y):
        """

        :param breadth: Breadth of the rectangular section
        :param height: Height of the rectangular section
        :param c_x: Distance between extreme fibers and neutral axis (around x-axis)
        :param c_y: Distance between extreme fibers and neutral axis (around y-axis)
        """
        self.breadth = breadth
        self.height = height
        self.c_x = c_x
        self.c_y = c_y
    def Rect_I_x(self):
        height = self.height
        breadth = self.breadth
        Ix = (breadth * pow(height, 3)) / 12
        return Ix

    def Rect_I_y(self):
        height = self.height
        breadth = self.breadth
        Iy = (breadth * pow(height, 3)) / 12
        return Iy

    def section_modulus_x(self):
        I = self.Rect_I_x()
        if self.c_x == 0:
            print(" Section_Tools:section_modulus_x: "
                  "Error! division by Zero is happening! Check the c_x value!")
            S = None
        else:
            S = I / self.c_x
        return S
    def section_modulus_y(self):
        I = self.Rect_I_y()
        if self.c_x == 0:
            print("Section_Tools:section_modulus_y:"
                  " Error! division by Zero is happening! Check the c_y value!")
            S = None
        else:
            S = I / self.c_y
        return S
    def Rect_A(self):
        if self.breadth == 0:
            print(" Section_Tools:Rect_A:"
                  " Error! entered value for breadth is zero! Check the breadth value!")
            A = None
        elif self.height == 0:
            print("Section_Tools:Rect_A:"
                  " Error! entered value for height is zero! Check the height value!")
            A = None
        else:
            A = self.breadth * self.height
        return A
    def Rect_Q_x(self):
        if self.breadth == 0:
            print("Section_Tools:Rect_Q_x:"
                  "Error! entered value for breadth is zero! Check the breadth value!")
            Q_x= None
        elif self.height == 0:
            print("Section_Tools:Rect_Q_x:"
                  "Error! entered value for height is zero! Check the height value!")
            Q_x = None
        else:
            Q_x = (self.breadth * pow(self.height, 2)) / 2
        return Q_x
    def Rect_Q_y(self):
        if self.breadth == 0:
            print("Section_Tools:Rect_Q_y:"
                  "Error! entered value for breadth is zero! Check the breadth value!")
            Q_y= None
        elif self.height == 0:
            print("Section_Tools:Rect_Q_y:"
                  "Error! entered value for height is zero! Check the height value!")
            Q_y = None
        else:
            Q_y = (self.height * pow(self.breadth, 2)) / 2
        return Q_y

class Modified_E_min: # Error checks for unsuitable vlues are added to each function
    def __init__(self, temperature, Incision_status, E_min):
        """
        :param: temperature: working temperature of the member in degrees of Fahrenheit
        :param Incision_status: An identifier showing whether the section is incised or not
        :param: E_min: Modulus of elasticity for beam and column stability
        """
        self.C_M = 0.9
        self.temperature = temperature
        self.Incision_status = Incision_status
        self.E_min = E_min
        self.Kf = 1.76

        return None
    def C_t_E_min(self):
        """
        Returns temperature factor for E_min according to table 2.3.3 of NDS 2024
        """
        temperature = self.temperature
        if temperature <= 100:
            C_t_E_min = 1.0
        elif 100 < temperature <= 150:
            C_t_E_min = 0.9
        else:
            print('Modified_E_min:C_t_E_min:'
                  'Error! the entered temperature is not within range!')
            C_t_E_min = None
            return 1
        return C_t_E_min
    def C_i_E_min(self):
        """
        Returns incision factor for E_min according to Table 4.3.8 of NDS 2024
        """
        if self.Incision_status:
            C_i_E_min = 0.95
        else:
            C_i_E_min = 1.0
        return C_i_E_min
    def E_min_prime(self):
        """
         Returns modified modulus of elasticity for beam and column stability
        """
        if self.C_t_E_min() == None:
            E_min_prime = None
            print('Modified_E_min:E_min_prime:'
                  'Error! Check the temperature!','\n',
                  'Entered temperature : {temp}'.format(temp=self.temperature),
                  '\n','It is only allowed to be from 0 to 150 degrees')
            return self.E_min
        else:
            E_min_prime = self.E_min * self.C_t_E_min() * self.C_i_E_min() * self.C_M * self.Kf
        return E_min_prime

class Modified_F_b: # Error checks for unsuitable vlues are added to each function
    def __init__(self, lamda,breadth, height, length, unsupported_length, Grade, MC, Material_type,
                 Fb, temperature, Incision_status, Spacing, Species_Type, Curvature_status,
                 Taper_status, Span_status, Loading_type, E_min_prime):
        """
        :param: lamda : Time effect factor (LRFD only)
        :param breadth: Breadth of the rectangular section (inches)
        :param height: Height of the rectangular section (inches)
        :param length: Length of the member (feet)
        :param: unsupported_length: Laterally unsupported length of the member (feet)
        :param Grade: Grade string representing the type of wooden section :
        'Select' & 'Structural' & 'No.1 & Btr' & 'No.1' & 'No.2' & 'No.3'
        'Stud'
        'Construction' & 'Standard'
        'Utility'
        'Unspecified'
        :param MC: Moisture content
        :param Material_type: 'SL': Sawn Lumber
                            'PIJ': Prefabricated I-Joists
                            'SCL': Structural Composite Lumber
                            'WSP': Wooden Structural Panels
                            'CLT': Cross-Laminated Timber
        :param: Fb: Nominal bending strength
        :param temperature: working temperature in degrees of Fahrenheit
        :param Incision_status: An identifier showing whether the section is incised or not
        :param Spacing: Center-to-center distance between members
        :param: Species_Type: 'Southern Pine' or 'Unspecified'
        :param Curvature_status: Indicates whether the member is curved or not (only for GLT)
        :param Taper_status: Indicates whether the member is tapered or not (only for GLT)
        :param Span_status: 'Cantilever' or 'Single Span'
        :param Loading_type:
        'C': Concentrated load at unsupported end or Concentrated load at center with no intermediate lateral support
        'U': Uniformly distributed load
        'CL': Concentrated load at center with lateral support at center
        'Two_3': Two equal concentrated loads at 1/3 points with lateral support at 1/3 points
        'Three_4': Three equal concentrated loads at 1/4 points with lateral support at 1/4 points
        'Four_5': Four equal concentrated loads at 1/5 points with lateral support at 1/5 points
        'Five_6': Five equal concentrated loads at 1/6 points with lateral support at 1/6 points
        'Six_7': Six equal concentrated loads at 1/7 points with lateral support at 1/7 points
        'Seven or more': Seven or more equal concentrated loads, evenly spaced, with lateral support at points of load application
        'Equal': Equal end moments
        'Unspecified': For or single span or cantilever bending members with loading conditions not specified in Table 3.3.3
        :param: E_min_prime : Modified modulus of elasticity for beam and column stability
        """
        self.lamda = lamda
        self.Phi_b = 0.85  # Resistance Factor (Appendix N Table N2 NDS 2024)
        self.K_f = 2.54  # Format Conversion Factor (Appendix N Table 4.3.1 NDS 2024)
        self.breadth = breadth
        self.height = height
        self.length = length * 12
        self.unsupported_length = unsupported_length * 12
        self.Grade = Grade
        self.MC = MC
        self.Material_type = Material_type
        self.Fb = Fb
        self.temperature = temperature
        self.Incision_status = Incision_status
        self.Spacing = Spacing
        self.Volume = height * breadth * length * 12  # Total volume of member (cubic inches)
        self.Species_Type = Species_Type
        self.Curvature_status = Curvature_status
        self.Taper_status = Taper_status
        self.Span_status = Span_status
        self.Loading_type = Loading_type
        self.E_min_prime = E_min_prime

        return None

    def C_fu(self):
        """
        Returns flat use factor (C_fu) for a given rectangular section
        according to NDS 2024 Table 4A in Supplements section
        """
        breadth = self.breadth
        height = self.height
        if breadth == 2 or breadth == 3:
            if height == 2 or height == 3:
                c_fu = 1.0
            elif height == 4 or height == 5:
                c_fu = 1.1
            elif height == 6 or height == 8:
                c_fu = 1.15
            elif height >= 10:
                c_fu = 1.2
            else:
                c_fu = None
                print("Modified_F_b:C_fu:"
                      "The height value is not within the specified range!", '\n',
                      'The breadth value is correct!')
                return 1
        elif breadth == 4:
            if height == 2 or height == 3:
                print("Modified_F_b:C_fu:"
                      "There is no need for C_fu for this case!",'\n',
                      'Entered height value = {h} inches. There is no need '
                      'for 2 or 3 inches of height to be considered a C_fu value for'.format(h=self.height))
                c_fu = 1.0
            elif height == 4:
                c_fu = 1.0
            elif height == 5 or height == 6 or height == 8:
                c_fu = 1.05
            elif height >= 10:
                c_fu = 1.1
            else:
                c_fu = None
                print("Modified_F_b:C_fu:"
                      "The height value is not within the specified range!", '\n',
                      'The breadth value is correct!')
                return 1
        else:
            c_fu = None
            print('Modified_F_b:C_fu:'
                  'The breadth value is not within range!','\n',
                  'Entered breadth value = {b} inches! The only supported values are '
                  '2,3, and 4 inches!'.format(b=self.breadth))
            return 1
        return c_fu

    def C_F(self):
        """
        Returns the size factor (C_F) for a given rectangular section
        according to NDS 2024 Table 4A in Supplements section
        """
        breadth = self.breadth
        height = self.height
        Grade = self.Grade
        if (Grade == 'Select' or Grade == 'Structural' or Grade == 'No.1 & Btr' or
                Grade == 'No.1' or Grade == 'No.2' or Grade == 'No.3'):
            if breadth == 2 or breadth == 3:
                if height == 2 or height == 3 or height == 4:
                    C_F = 1.50
                elif height == 5:
                    C_F = 1.4
                elif height == 6:
                    C_F = 1.3
                elif height == 8:
                    C_F = 1.2
                elif height == 10:
                    C_F = 1.1
                elif height == 12:
                    C_F = 1.0
                elif height >= 14:
                    C_F = 0.90
                else:
                    C_F = None
                    print('Modified_F_b:C_F:'
                          'The height value is not within the specified range!', '\n',
                          'Entered Grade : {g}, Entered height = {h} inches'.format(g=self.Grade, h=self.height),
                          '\n', 'Acceptable range of values for {g} : '
                                '2,3,4,5,6,8,10,12, 14 and beyond'.format(g=self.Grade))
                    return 1
            elif breadth == 4:
                if height == 2 or height == 3 or height == 4:
                    C_F = 1.50
                elif height == 5:
                    C_F = 1.4
                elif height == 6:
                    C_F = 1.3
                elif height == 8:
                    C_F = 1.3
                elif height == 10:
                    C_F = 1.2
                elif height == 12:
                    C_F = 1.1
                elif height >= 14:
                    C_F = 1.2
                else:
                    C_F = None
                    print('Modified_F_b:C_F:'
                          'The height value is not within the specified range!', '\n',
                          'Entered Grade : {g}, Entered height = {h} inches'.format(g=self.Grade, h=self.height),
                          '\n', 'Acceptable range of values for {g} : '
                                '2,3,4,5,6,8,10,12, 14 and beyond'.format(g=self.Grade))
                    return 1
            else:
                C_F = None
                print('Modified_F_b:C_F:'
                      'The breadth value is not within the specified range!','\n',
                      'Entered breadth value = {b} inches! '
                      'The only supported values are 2,3, and 4 inches.'.format(b=self.breadth))
                return 1
        elif Grade == 'Stud':
            if breadth == 2 or breadth == 3 or breadth == 4:
                if height == 2 or height == 3 or height == 4:
                    C_F = 1.1
                elif height == 5 or height == 6:
                    C_F = 1.0
                elif height == 8:
                    C_F = 0.9
                elif height == 10:
                    C_F = 0.8
                elif height == 12:
                    C_F = 0.7
                elif height >= 14:
                    C_F = 0.6
                else:
                    C_F = None
                    print('Modified_F_b:C_F:'
                          'The height value is not within the specified range!', '\n',
                          'Entered Grade : {g}, Entered height = {h} inches'.format(g=self.Grade, h=self.height),
                          '\n', 'Acceptable range of values for {g} : '
                                '2,3,4,5,6,8,10,12, 14 and beyond'.format(g=self.Grade))
                    return 1
        elif Grade == 'Construction' or Grade == 'Standard':
            if breadth == 2 or breadth == 3 or breadth == 4:
                if height == 2 or height == 3 or height == 4:
                    C_F = 1
                else:
                    C_F = None
                    print('Modified_F_b:C_F:'
                          'The height value is not within the specified range!', '\n',
                          'Entered Grade : {g}, Entered height = {h} inches'.format(g=self.Grade, h=self.height),
                          '\n', 'Acceptable range of values for {g} : '
                                '2,3,4'.format(g=self.Grade))
                    return 1
            else:
                C_F = None
                print('Modified_F_b:C_F:'
                      'The breadth value is not within the specified range!', '\n',
                      'Entered breadth value = {b} inches! '
                      'The only supported values are 2,3, and 4 inches.'.format(b=self.breadth))
                return 1
        elif Grade == 'Utility':
            if breadth == 2 or breadth == 3:
                if height == 2 or height == 3:
                    C_F = 0.4
                elif height == 4:
                    C_F = 1
                else:
                    C_F = None
                    print('Modified_F_b:C_F:'
                          'The height value is not within the specified range!', '\n',
                          'Entered Grade : {g}, Entered height = {h} inches'.format(g=self.Grade, h=self.height),
                          '\n', 'Acceptable range of values for {g} : '
                                '2,3, and 4'.format(g=self.Grade))
                    return 1
            elif breadth == 4:
                if height == 2 or height == 3:
                    C_F = 1.0
                    print('Modified_F_b:C_F:'
                          'There is no need to consider C_F value for this type of section')
                elif height == 4:
                    C_F = 1.0
                else:
                    C_F = None
                    print('Modified_F_b:C_F:'
                          'The height value is not within the specified range!', '\n',
                          'Entered Grade : {g}, Entered height = {h} inches'.format(g=self.Grade, h=self.height),
                          '\n', 'Acceptable range of values for {g} : '
                                '2,3, and 4'.format(g=self.Grade))
                    return 1
        else:
            C_F = None
            print('Modified_F_b:C_F:'
                  'The entered grade is not present in the corresponding table of NDS 2024')
            return 1
        return C_F

    def C_M(self):
        """
        Returns wet service factor (C_M) for sawn lumber
        """
        MC = self.MC
        C_F = self.C_F()
        F_b = self.Fb
        if MC <= 0.19:
            C_M = 1.0
        elif MC > 0.19 and F_b * C_F > 1150:
            C_M = 0.85
        elif MC > 0.19 and F_b * C_F <= 1150:
            C_M = 1.0
        else:
            C_M = None
            print('Modified_F_b:C_M:'
                  'Error! Check the input!')
            return 1
        return C_M

    def Moisture_Condition(self):
        """
        Specifies if the entered material is classified as wet or dry
        """
        Material_type = self.Material_type
        MC = self.MC
        if Material_type == 'SL':
            if MC <= 0.19:
                Wet = False
            else:
                Wet = True
        elif Material_type == 'GLT' or Material_type == 'PIJ' or Material_type == 'SCL' or Material_type == 'WSP' or Material_type == 'CLT':
            if MC <= 0.16:
                Wet = False
            else:
                Wet = True
        return Wet

    def C_t(self):
        """
        Returns temperature factor (C_t) according to NDS 2024 Sec. 2.3.3
        """
        Moisture_Condition = self.Moisture_Condition()
        temperature = self.temperature
        if Moisture_Condition:
            if temperature <= 100:
                C_t = 1.0
            elif 100 < temperature <= 125:
                C_t = 0.7
            elif 125 < temperature <= 150:
                C_t = 0.5
            else:
                C_t = None
                print('Modified_F_b:C_t:'
                      'Error! The entered temperature value is not within range!'
                      ,'\n','The temperature should be between 0 and 150 degrees of fahrenheit'
                      ,'\n','Entered temperature value: {t} '.format(t=self.temperature))
                return 1
        else:
            if temperature <= 100:
                C_t = 1.0
            elif 100 < temperature <= 125:
                C_t = 0.8
            elif 125 < temperature <= 150:
                C_t = 0.7
            else:
                C_t = None
                print('Modified_F_b:C_t:'
                      'Error! The entered temperature value is not within range!'
                      , '\n', 'The temperature should be between 0 and 150 degrees of fahrenheit',
                      '\n', 'Entered temperature value: {t} '.format(t=self.temperature))
        return C_t

    def C_i(self):
        """
        Returns incising factor (C_i) according to Table 4.3.8 in NDS 2024
        """
        Incision_status = self.Incision_status
        if Incision_status:
            C_i = 0.8
        else:
            C_i = 1.0
        return C_i

    def C_r(self):
        """
        Returns Repetitive member factor (C_r) according to NDS 2024 Sec. 4.3.9
        """
        Spacing = self.Spacing
        breadth = self.breadth
        if breadth == 2 or breadth == 3 or breadth == 4:
            if Spacing <= 24:
                C_r = 1.15
            else:
                C_r = 1.0
        else:
            C_r = None
            print('Modified_F_b:C_r:'
                  'C_r is not applicable to this case! as the entered breadth value is {b} inches'
                  'while only 2, 3, and 4 inches are accounted for'.format(b=self.breadth))
            return 1
        return C_r

    def C_V(self):
        Species_Type = self.Species_Type
        Volume = self.Volume
        if Volume < 15498:
            C_V = 1.0
        else:
            if Species_Type == 'Southern Pine':
                C_V = pow((15498 / Volume), (1 / 20))
            else:
                C_V = pow((15498 / Volume), (1 / 10))
        return C_V

    def C_c(self):
        """
        Returns Curvature Factor (C_c)
        """
        Curvature_status = self.Curvature_status
        Material_type = self.Material_type
        if Material_type == 'GLT':
            if Curvature_status:
                C_c = None
                print('Modified_F_b:C_c:'
                      'C_c is not applicable to this case! since this code does not'
                      'consider curved members!')
                return 1
            else:
                C_c = 1.0
        else:
            C_c = None
            print('Modified_F_b:C_c:'
                  'C_c is not applicable to this case! Material is not GLT!')
            return 1
        return C_c

    def C_I(self):
        """
        Returns stress interaction factor (C_I)
        """
        Material_type = self.Material_type
        Taper_status = self.Taper_status
        if Material_type == 'GLT':
            if Taper_status:
                C_I = None
                print('Modified_F_b:C_I:'
                      'C_I is not applicable to this case! since this code does not'
                      'consider tapered members!')
                return 1
            else:
                C_I = 1.0
        else:
            C_I = None
            print('Modified_F_b:C_I:'
                  'C_I is not applicable to this case! Material is not GLT!')
            return 1
        return C_I

    def l_e(self):
        """
        Return effective length (le) according to Table 3.3.3 of NDS 2024
        """
        height = self.height
        breadth = self.breadth
        unsupported_length = self.unsupported_length * 12
        Span_status = self.Span_status
        Loading_type = self.Loading_type
        if height >= breadth and (unsupported_length / height) < 7:
            if Span_status == 'Cantilever':
                if Loading_type == 'C':
                    le = 1.87 * unsupported_length
                elif Loading_type == 'U':
                    le = 1.33 * unsupported_length
                else:
                    le = 2.06 * unsupported_length
            else:
                if Loading_type == 'C':
                    le = 1.80 * unsupported_length
                elif Loading_type == 'U':
                    le = 2.06 * unsupported_length
                elif Loading_type == 'CL':
                    le = 1.111 * unsupported_length
                elif Loading_type == 'Two_3' or Loading_type == 'Four_5':
                    le = 1.68 * unsupported_length
                elif Loading_type == 'Three_4':
                    le = 1.54 * unsupported_length
                elif Loading_type == 'Five_6':
                    le = 1.73 * unsupported_length
                elif Loading_type == 'Six_7':
                    le = 1.78 * unsupported_length
                elif Loading_type == 'Seven or more' or Loading_type == 'Equal':
                    le = 1.84 * unsupported_length
                else:
                    le = 2.06 * unsupported_length
        else:
            if Span_status == 'Cantilever':
                if Loading_type == 'U':
                    le = (0.9 * unsupported_length) + (3 * height)
                else:
                    le = (1.44 * unsupported_length) + (3 * height)
            elif Span_status == 'Single Span':
                if Loading_type == 'C':
                    le = (1.37 * unsupported_length) + (3 * height)
                elif Loading_type == 'U':
                    le = (1.63 * unsupported_length) + (3 * height)
                elif Loading_type == 'CL':
                    le = 1.111 * unsupported_length
                elif Loading_type == 'Two_3' or Loading_type == 'Four_5':
                    le = 1.68 * unsupported_length
                elif Loading_type == 'Three_4':
                    le = 1.54 * unsupported_length
                elif Loading_type == 'Five_6':
                    le = 1.73 * unsupported_length
                elif Loading_type == 'Six_7':
                    le = 1.78 * unsupported_length
                elif Loading_type == 'Seven or more' or Loading_type == 'Equal':
                    le = 1.84 * unsupported_length
                else:
                    if (unsupported_length / height) <= 14.3:
                        le = (1.63 * unsupported_length) + (3 * height)
                    else:
                        le = 1.84 * unsupported_length
            return le

    def R_B(self):
        """
        Returns slenderness ratio of a given member
        """
        if self.height == self.breadth:
            effective_length = self.l_e()
            R_b = sqrt(effective_length / self.breadth)
        else:
            effective_length = self.l_e()
            R_b = sqrt((effective_length * self.height) / pow(self.breadth, 2))
        if R_b <= 50:
            print('\n','$$$$$$$$','\n',
                  'Modified_F_b:R_B: Current slenderness ratio '
                  '(for bending only) = {rb} <= 50.   '
                  'Ratio Check : O. K.'.format(rb=R_b),'\n')
        else:
            print('\n','$$$$$$$$','\n',
                  'Modified_F_b:R_B: Current slenderness ratio'
                  ' (for bending only) = {rb} > 50.   '
                  'Ratio Check : Error! Slenderness ratio is out of bounds!'
                  'consider redesigning the section!'.format(rb=R_b),'\n')
        return R_b
    def F_b_E(self):
        """
        Returns elastic buckling stress
        """
        F_b_E = (1.2 * self.E_min_prime) / (pow(self.R_B(),2))
        return F_b_E
    def F_b_asterisk(self):
        if self.C_V() is None:
            F_b_asterisk = self.lamda * self.Fb * self.K_f * self.Phi_b * self.C_M() * self.C_t() * self.C_F() * self.C_i() * self.C_r()
        elif self.C_V() <= 1.0:
            F_b_asterisk = self.lamda * self.Fb * self.K_f * self.Phi_b * self.C_M() * self.C_t() * self.C_c() * self.C_I() * self.C_i() * self.C_r()
        else:
            F_b_asterisk = self.lamda * self.Fb * self.K_f * self.Phi_b * self.C_M() * self.C_t() * self.C_c() * self.C_I() * self.C_i() * self.C_r() * self.C_V()
        return  F_b_asterisk
    def C_L(self):
        """
        Returns beam stability factor (C_L)
        """
        temp = ((1 + (self.F_b_E()/self.F_b_asterisk())) / 1.9)
        temp1 = ( (self.F_b_E()/self.F_b_asterisk()) / 0.95)
        C_L = temp + sqrt(pow(temp, 2) - temp1)
        return C_L
    def F_b_n_prime(self):
        """
        Returns the modified bending capacity of a member (F_b_n_prime) LRDF only
        """
        if self.C_V() is None:
            F_b_n_prime = self.Fb * self.lamda * self.K_f * self.Phi_b * self.C_M() * self.C_t() * self.C_L() * self.C_F() * self.C_fu() * self.C_c() * self.C_I() * self.C_i() * self.C_r()
        else:
            F_b_n_prime = self.Fb * self.lamda * self.K_f * self.Phi_b * self.C_M() * self.C_t() * self.C_L() * self.C_V() * self.C_fu() * self.C_c() * self.C_I() * self.C_i() * self.C_r()
        return F_b_n_prime
class Modified_F_v: # Error checks for unsuitable vlues are added to ech function
    def __init__(self, lamda, MC, Material_type,
                 Fv, temperature, Incision_status):
        """

        :param lamda: Time effect factor (LRFD only)
        :param MC: Moisture content
        :param Material_type: 'SL': Sawn Lumber
                            'PIJ': Prefabricated I-Joists
                            'SCL': Structural Composite Lumber
                            'WSP': Wooden Structural Panels
                            'CLT': Cross-Laminated Timber
        :param Fv: Nominal shear strength
        :param temperature: working temperature in degrees of Fahrenheit
        :param Incision_status: An identifier showing whether the section is incised or not
        """
        self.lamda = lamda
        self.Phi_v = 0.75  # Resistance Factor (Appendix N Table N2 NDS 2024)
        self.K_f = 2.88  # Format Conversion Factor (Appendix N Table 4.3.1 NDS 2024)
        self.MC = MC
        self.Material_type = Material_type
        self.F_v = Fv
        self.temperature = temperature
        self.Incision_status = Incision_status
    def C_i(self):
        """
        Returns incising factor (C_i) according to Table 4.3.8 in NDS 2024
        """
        Incision_status = self.Incision_status
        if Incision_status:
            C_i = 0.8
        else:
            C_i = 1.0
        return C_i
    def C_M (self):
        """
        :return: Returns CM for shear only
        """
        if self.MC <= 0.19:
            C_M = 1.0
        else:
            C_M = 0.97
        return C_M
    def Moisture_Condition(self):
        """
        Specifies if the entered material is classified as wet or dry
        """
        Material_type = self.Material_type
        MC = self.MC
        if Material_type == 'SL':
            if MC <= 0.19:
                Wet = False
            else:
                Wet = True
        elif (Material_type == 'GLT' or Material_type == 'PIJ' or
              Material_type == 'SCL' or Material_type == 'WSP' or Material_type == 'CLT'):
            if MC <= 0.16:
                Wet = False
            else:
                Wet = True
        else:
            print("Modified_F_v:Moisture_Condition:"
                  "Error! Check the material type!",'\n',
                  'Entered Material Type : {mt}'.format(mt=self.Material_type),'\n',
                  'Only SL, GLT, SCL, PIJ, WSP, and CLT are supported!')
            Wet = None
        return Wet
    def C_t(self):
        if self.Moisture_Condition():
            if self.temperature < 100:
                C_t = 1.0
            elif 100 <= self.temperature < 125:
                C_t = 0.7
            else:
                C_t = 0.5
        else:
            if self.temperature < 100:
                C_t = 1.0
            elif 100 <= self.temperature < 125:
                C_t = 0.8
            else:
                C_t = 0.7
        return C_t
    def C_i(self):
        if self.Incision_status:
            C_i = 0.8
        else:
            C_i = 1.0
        return C_i
    def C_vr(self):
        if self.Material_type =='GLT' or self.Material_type =='Glulam':
            C_vr = 0.72
        else:
            print('Modified_F_v:C_vr:'
                  'Warning! Check the Material type!','\n',
                  'Entered Material Type : {mt}'.format(mt=self.Material_type),'\n',
                  'Only GLT and Glulam are accounted for!')
            C_vr = 1.0
        return C_vr
    def F_v_n_prime(self):
        F_v_n_prime = self.F_v * self.Phi_v * self.K_f * self.lamda * self.C_M() * self.C_t() * self.C_i() * self.C_vr()
        return F_v_n_prime
class Modified_F_c_perpendicular: # Error checks for unsuitable vlues are added to each function
    def __init__(self, MC, Material_type, temperature, F_c_perp):
        """

        :param MC: Moisture content
        :param Material_type: 'SL': Sawn Lumber
                            'PIJ': Prefabricated I-Joists
                            'SCL': Structural Composite Lumber
                            'WSP': Wooden Structural Panels
                            'CLT': Cross-Laminated Timber
        :param temperature: working temperature in degrees of Fahrenheit
        :param F_c_perp: Nominal parallel to grain compressive strength (bearing strength)
        """
        self.Phi_c = 0.9
        self.Kf = 1.67
        self.MC = MC
        self.Material_type = Material_type
        self.temperature = temperature
        self.C_i = 1.0
        self.C_b = 1.0  # Conservative design
        self.F_c_perp = F_c_perp
    def C_M(self):
        if self.MC <= 0.19:
            C_M = 1.0
        else:
            C_M = 0.67
        return C_M
    def Moisture_condition(self):
        if self.Material_type == 'SL':
            if self.MC <= 0.19:
                Wet = False
            else:
                Wet = True
        else:
            print('Modified_F_c_perpendicular:Moisture_condition:'
                  'Warning! Entered Material Type : {mt}'.format(mt=self.Material_type),'\n',
                  'Enter SL if you meant Sawn Lumber')
            if self.MC <= 0.16:
                Wet = False
            else:
                Wet = True
        return Wet

    def C_t(self):
        if self.Moisture_Condition():
            if self.temperature < 100:
                C_t = 1.0
            elif 100 <= self.temperature < 125:
                C_t = 0.7
            else:
                C_t = 0.5
        else:
            if self.temperature < 100:
                C_t = 1.0
            elif 100 <= self.temperature < 125:
                C_t = 0.8
            else:
                C_t = 0.7
        return C_t
    def F_c_n_perpendicular_prime(self):
        F_c_n_perp_prime = self.F_c_perp * self.Kf * self.Phi_c * self.C_M() * self.C_t() * self.C_i * self.C_b
        return F_c_n_perp_prime
class Modified_F_c_parallel: # Error checks for unsuitable vlues are added to each function
    def __init__(self, lamda, height, breadth, Member_type, Grade, MC, Material_type,
                 Fc, temperature, Incision_status, E_min_prime,
                 length, base_support, top_support):
        """
                :param: lamda : Time effect factor (LRFD only)
                :param height: Height of the rectangular section (inches)
                :param: breadth: Breadth f the rectangular section (inches)
                :param: Member_type: Designates whether a beam or column is being analyzed
                'B' for beam
                'C' for column
                :param Grade: Grade string representing the type of wooden section :
                'Select' & 'Structural' & 'No.1 & Btr' & 'No.1' & 'No.2' & 'No.3'
                'Stud'
                'Construction' & 'Standard'
                'Utility'
                'Unspecified'
                :param MC: Moisture content
                :param Material_type: 'SL': Sawn Lumber
                                    'PIJ': Prefabricated I-Joists
                                    'SCL': Structural Composite Lumber
                                    'WSP': Wooden Structural Panels
                                    'CLT': Cross-Laminated Timber
                :param: Fc: Nominal compressive strength (parallel to grain)
                :param temperature: working temperature in degrees of Fahrenheit
                :param Incision_status: An identifier showing whether the section is incised or not
                :param: E_min_prime : Modified modulus of elasticity for beam and column stability
                :param: length: Length of a column (feet)
                :param: base_support: Supports conditions at the base of the column
                'Fixed' for fixed support
                'Pinned' for pinned support
                :param: top_support: Supports conditions at the top of the column
                'Fixed' for fixed support
                'Pinned' for pinned support
                'Roller' for roller support
                'Cantilever' for free top end
                """
        self.length = length
        self.lamda = lamda
        self.Phi_c = 0.9
        self.Kf = 2.40
        self.height = height
        self.breadth = breadth
        self.Member_type = Member_type
        self.Grade = Grade
        self.MC = MC
        self.Material_type = Material_type
        self.F_c = Fc
        self.temperature = temperature
        self.Incision_status = Incision_status
        self.E_min_prime = E_min_prime
        self.base_support = base_support
        self.top_support = top_support
        self.length = length * 12
        if self.Material_type == 'SL':
            self.c = 0.80
        else:
            self.c = 0.90
        return None
    def K(self):
        base_support = self.base_support
        top_support = self.top_support
        if base_support == 'Fixed':
            if top_support =='Fixed':
                K = 0.65
            elif top_support =='Pinned':
                K = 0.8
            elif top_support == 'Roller':
                K = 1.20
            elif top_support =='Cantilever':
                K = 2.10
            else:
                print("Modified_F_c_parallel:K:"
                      "Error! Base support is {b} while top support is {t}!"
                      " These two do not go together!".format(b=self.base_support, t=self.top_support))
                K = 2.40
        elif base_support == 'Pinned':
            if top_support == 'Pinned':
                K = 1.0
            else:
                print("Modified_F_c_parallel:K:"
                      "Error! Base support is {b} while top support is {t}!"
                      " These two do not go together!".format(b=self.base_support, t=self.top_support))
                K = 2.4
        else:
            print("Modified_F_c_parallel:K:"
                  "Error! Base support is {b} while top support is {t}!"
                  " These two do not go together!".format(b=self.base_support, t=self.top_support))
            K = 2.4
        return K
    def l_e(self):
        l_e = self.length * self.K()
        return l_e
    def R_B(self):
        R_b = self.l_e() / self.height
        if R_b <= 50:
            print('\n','$$$$$$$$','\n',
                  'Modified_F_c_parallel:R_B: Current slenderness ratio '
                  '(for compression only) = {rb} <= 50.   '
                  'Ratio Check : O. K. for both design and construction'.format(rb=R_b),'\n')
        elif 50 < R_b <= 75:
            print('\n','$$$$$$$$','\n',
                  'Modified_F_c_parallel:R_B: Current slenderness ratio '
                  '(for compression only) = 50 <= {rb} < 75.   '
                  'Ratio Check : O. K. for construction only!'.format(rb=R_b),'\n')
        else:
            print('\n','$$$$$$$$','\n',
                  'Modified_F_c_parallel:R_B: Current slenderness ratio '
                  '(for compression only) = 75 < {rb} .   '
                  'Ratio Check : Failed! for both design and construction!'
                  'consider redesigning the section!'.format(rb=R_b),'\n')

        return R_b
    def C_F(self):
        """
                Returns the size factor (C_F) for a given rectangular section
                according to NDS 2024 Table 4A in Supplements section
                """
        height = self.height
        Grade = self.Grade
        if (Grade == 'Select' or Grade == 'Structural' or Grade == 'No.1 & Btr' or
                Grade == 'No.1' or Grade == 'No.2' or Grade == 'No.3'):
            if height == 2 or height == 3 or height == 4:
                C_F = 1.15
            elif height == 5 or height == 6:
                C_F = 1.1
            elif height == 8:
                C_F = 1.05
            elif height == 10 or height == 12:
                C_F = 1.0
            elif height >= 14:
                C_F = 0.90
            else:
                C_F = None
                print('Modified_F_c_parallel:C_F:'
                      'The height value is not within the specified range!','\n',
                      'Entered Grade : {g}, Entered height = {h} inches'.format(g=self.Grade, h=self.height),
                      '\n', 'Acceptable range of values for {g} : '
                      '2,3,4,5,6,8,10,12, 14 and beyond'.format(g=self.Grade))
                return 1
        elif Grade == 'Stud':
            if height == 2 or height == 3 or height == 4:
                C_F = 1.05
            elif height == 5 or height == 6:
                C_F = 1.0
            elif height >= 8:
                C_F = 0.95
            else:
                C_F = None
                print('Modified_F_c_parallel:C_F:'
                      'The height value is not within the specified range!', '\n',
                      'Entered Grade : {g}, Entered height = {h} inches'.format(g=self.Grade, h=self.height),
                      '\n', 'Acceptable range of values for {g} : '
                            '2,3,4,5,6,8 and beyond'.format(g=self.Grade))
                return 1
        elif Grade == 'Construction' or Grade == 'Standard':
            if height == 2 or height == 3 or height == 4:
                C_F = 1.0
            else:
                C_F = None
                print('Modified_F_c_parallel:C_F:'
                      'The height value is not within the specified range!', '\n',
                      'Entered Grade : {g}, Entered height = {h} inches'.format(g=self.Grade, h=self.height),
                      '\n', 'Acceptable range of values for {g} : '
                            '2,3, and 4'.format(g=self.Grade))
                return 1
        elif Grade == 'Utility':
            if height == 2 or height == 3:
                C_F = 0.6
            elif height == 4:
                C_F = 1
            else:
                C_F = None
                print('Modified_F_c_parallel:C_F:'
                      'The height value is not within the specified range!', '\n',
                      'Entered Grade : {g}, Entered height = {h} inches'.format(g=self.Grade, h=self.height),
                      '\n', 'Acceptable range of values for {g} : '
                            '2,3, and 4'.format(g=self.Grade))
                return 1
        return C_F
    def C_i(self):
        if self.Incision_status:
            C_i = 0.8
        else:
            C_i = 1.0
        return C_i
    def Moisture_condition(self):
        if self.Material_type == 'SL':
            if self.MC <= 0.19:
                Wet = False
            else:
                Wet = True
        else:
            if self.MC <= 0.16:
                Wet = False
            else:
                Wet = True
        return Wet
    def C_M(self):
        if self.Moisture_condition() == False or self.F_c * self.C_F() <= 750:
            C_M = 1.0
        else:
            C_M = 0.8
        return C_M
    def C_t(self):
        if self.Moisture_condition():
            if self.temperature < 100:
                C_t = 1.0
            elif 100 <= self.temperature < 125:
                C_t = 0.7
            else:
                C_t = 0.5
        else:
            if self.temperature < 100:
                C_t = 1.0
            elif 100 <= self.temperature < 125:
                C_t = 0.8
            else:
                C_t = 0.7
        return C_t
    def F_c_n_parallel_asterisk(self):
        F_c_n_parallel_asterisk = self.F_c * self.Kf * self.lamda * self.Phi_c * self.C_M() * self.C_F() * self.C_t() * self.C_i()
        return F_c_n_parallel_asterisk
    def F_c_Euler_n(self):
        if self.breadth >= self.height:
            d = self.height
        else:
            d = self.breadth
        F_c_Euler_n = 0.822 * (self.E_min_prime / pow((self.l_e() / d), 2))
        return F_c_Euler_n
    def C_P(self):
        a = (1 + (self.F_c_Euler_n()/self.F_c_n_parallel_asterisk()) / (2 * self.c))
        b = pow (a,2) - ((self.F_c_Euler_n()/self.F_c_n_parallel_asterisk())/self.c)
        C_P = a - sqrt(b)
        return C_P
    def F_c_n_parallel_prime(self):
        if self.Member_type == 'C':
            F_c_n_parallel_prime = self.F_c * self.Kf * self.lamda * self.Phi_c * self.C_M() * self.C_F() * self.C_t() * self.C_i() * self.C_P()
        else:
            F_c_n_parallel_prime = self.F_c * self.Kf * self.lamda * self.Phi_c * self.C_M() * self.C_F() * self.C_t() * self.C_i()
        return F_c_n_parallel_prime
class Modified_F_t:
    def __init__(self, lamda, height, Grade,
                 Ft, temperature, Incision_status):
        """
                :param: lamda : Time effect factor (LRFD only)
                :param height: Height of the rectangular section (inches)
                :param Grade: Grade string representing the type of wooden section :
                'Select' & 'Structural' & 'No.1 & Btr' & 'No.1' & 'No.2' & 'No.3'
                'Stud'
                'Construction' & 'Standard'
                'Utility'
                'Unspecified'
                :param: Ft: Nominal tensile strength (parallel to grain)
                :param temperature: working temperature in degrees of Fahrenheit
                :param Incision_status: An identifier showing whether the section is incised or not
                """
        self.lamda = lamda
        self.Phi_c = 0.8
        self.Kf = 2.70
        self.height = height
        self.Grade = Grade
        self.F_t = Ft
        self.temperature = temperature
        self.Incision_status = Incision_status
        self.C_M = 1.0
    def C_F(self):
        """
                Returns the size factor (C_F) for a given rectangular section
                according to NDS 2024 Table 4A in Supplements section
                """
        height = self.height
        Grade = self.Grade
        if (Grade == 'Select' or Grade == 'Structural' or
                Grade == 'No.1 & Btr' or Grade == 'No.1' or Grade == 'No.2' or Grade == 'No.3'):
            if height == 2 or height == 3 or height == 4:
                C_F = 1.5
            elif height == 5:
                C_F = 1.4
            elif height == 6:
                C_F = 1.3
            elif height == 8:
                C_F = 1.2
            elif height == 10:
                C_F = 1.1
            elif height == 12:
                C_F = 1.0
            elif height >= 14:
                C_F = 0.90
            else:
                C_F = None
                print('Modified_F_t:C_F:'
                      'The height value is not within the specified range!', '\n',
                      'Entered Grade : {g}, Entered height = {h} inches'.format(g=self.Grade, h=self.height),
                      '\n', 'Acceptable range of values for {g} : '
                            '2,3,4,5,6,8,10,12, 14 and beyond'.format(g=self.Grade))
                return 1
        elif Grade == 'Stud':
            if height == 2 or height == 3 or height == 4:
                C_F = 1.1
            elif height == 5 or height == 6:
                C_F = 1.0
            elif height >= 8:
                C_F = 0.90
            else:
                C_F = None
                print('Modified_F_t:C_F:'
                      'The height value is not within the specified range!', '\n',
                      'Entered Grade : {g}, Entered height = {h} inches'.format(g=self.Grade, h=self.height),
                      '\n', 'Acceptable range of values for {g} : '
                            '2,3,4,5,6,8 and beyond'.format(g=self.Grade))
                return 1
        elif Grade == 'Construction' or Grade == 'Standard':
            if height == 2 or height == 3 or height == 4:
                C_F = 1.0
            else:
                C_F = None
                print('Modified_F_t:C_F:'
                      'The height value is not within the specified range!', '\n',
                      'Entered Grade : {g}, Entered height = {h} inches'.format(g=self.Grade, h=self.height),
                      '\n', 'Acceptable range of values for {g} : '
                            '2,3,4'.format(g=self.Grade))
                return 1
        elif Grade == 'Utility':
            if height == 2 or height == 3:
                C_F = 0.4
            elif height == 4:
                C_F = 1
            else:
                C_F = None
                print('Modified_F_t:C_F:'
                      'The height value is not within the specified range!', '\n',
                      'Entered Grade : {g}, Entered height = {h} inches'.format(g=self.Grade, h=self.height),
                      '\n', 'Acceptable range of values for {g} : '
                            '2,3,4'.format(g=self.Grade))
                return 1
        return C_F
    def C_i(self):
        if self.Incision_status:
            C_i = 0.8
        else:
            C_i = 1.0
        return C_i
    def C_t(self):
        if self.temperature <= 100:
            C_t = 1.0
        else:
            C_t = 0.9
        return C_t
    def F_t_n_prime(self):
        F_t_n_prime = self.F_t * self.Kf * self.lamda * self.Phi_c * self.C_M * self.C_F() * self.C_t() * self.C_i()
        return  F_t_n_prime
