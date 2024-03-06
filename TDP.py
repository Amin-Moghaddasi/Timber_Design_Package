from math import pow
from math import sqrt
class Section_Tools:
    def Rect_I_x(self, breadth, height):
        """
        Returns moment of inertia around strong axis of a rectangular section
        :param breadth: Breadth of the rectangular section
        :param height: Height of the rectangular section
        """
        Ix = (breadth * pow(height, 3)) / 12
        return Ix
    def Rect_I_y(self, breadth, height):
        """
        Returns moment of inertia around weak axis of a rectangular section
        :param breadth: Breadth of the rectangular section
        :param height: Height of the rectangular section
        """
        Iy = (breadth * pow(height, 3)) / 12
        return Iy
    def section_modulus(self, I, c):
      """

      :param I: Moment of inertia around an arbitrary axis
      :param c: Distance between extreme fibers and neutral axis
      :return:
      """
      S = I / c
      return S
class Bending_Modification_Factors:
    def __init__(self):
        self.Phi_b = 0.85  # Resistance Factor (Appendix N Table N2 NDS 2024)
        self.K_f = 2.54  # Format Conversion Factor (Appendix N Table 4.3.1 NDS 2024)
        return 0
    def C_fu(self, breadth, height):
        """
        Returns flat use factor (C_fu) for a given rectangular section
        according to NDS 2024 Table 4A in Supplements section
        :param breadth: Breadth of the rectangular section
        :param height: Height of the rectangular section
        """
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
                print("The height value is not within the specified range!",'\n',
                      'The breadth value is correct!')
        elif breadth == 4:
            if height == 2 or height == 3:
                print("There is no need for C_fu for this case!")
                c_fu = 1.0
            elif height == 4:
                c_fu = 1.0
            elif height == 5 or height == 6 or height == 8:
                c_fu = 1.05
            elif height >= 10:
                c_fu = 1.1
            else:
                c_fu = None
                print("The height value is not within the specified range!",'\n',
                      'The breadth value is correct!')
        else:
            c_fu = None
            print('The breadth value is not within range!')
        return c_fu
    def C_F(self, Grade, breadth, height):
        """
        Returns the size factor (C_F) for a given rectangular section
        according to NDS 2024 Table 4A in Supplements section
        :param Grade: Grade string representing the type of wooden section
        :param breadth: Breadth of the rectangular section
        :param height: Height of the rectangular section
        """
        if Grade == 'Select' or Grade == 'Structural' or Grade == 'No.1 & Btr' or Grade == 'No.1' or Grade == 'No.2' or Grade == 'No.3':
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
                    print('The height value is not within the specified range!','\n',
                          'The breadth value is correct!')
            elif breadth == 4 :
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
                    print('The height value is not within the specified range!','\n',
                          'The breadth value is correct!')
            else:
                C_F = None
                print('The breadth value is not within the specified range!')
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
                    print('The height value is not within the specified range!','\n',
                          'The breadth value is correct!')
        elif Grade == 'Construction' or Grade == 'Standard':
            if breadth == 2 or breadth == 3 or breadth == 4:
                if height == 2 or height == 3 or height == 4:
                    C_F = 1
                else:
                    C_F = None
                    print('The height value is not within the specified range!', '\n',
                          'The breadth value is correct!')
            else:
                C_F = None
                print('The breadth value is not within the specified range!')
        elif Grade == 'Utility':
            if breadth == 2 or breadth == 3:
                if height == 2 or height ==3:
                    C_F = 0.4
                elif height == 4:
                    C_F = 1
                else:
                    C_F = None
                    print('The height value is not within the specified range!', '\n',
                          'The breadth value is correct!')
            elif breadth == 4:
                if height == 2 or height == 3:
                    C_F = 1.0
                    print('There is no need to consider C_F value for this type of section')
                elif height == 4:
                    C_F = 1.0
                else:
                    C_F = None
                    print('The height value is not within the specified range!', '\n',
                          'The breadth value is correct!')
        else:
            C_F = None
            print('The entered grade is not present in the corresponding table of NDS 2024')
        return  C_F
    def C_M(self, MC, C_F, F_b):
        """
        Returns wet service factor (C_M) for sawn lumber
        :param MC: Moisture content
        :param C_F: Size factor
        :param F_b: nominal Bending strength
        """
        if MC <= 0.19:
            C_M = 1.0
        elif MC > 0.19 and F_b * C_F > 1150:
            C_M = 0.85
        elif MC > 0.19 and F_b * C_F <= 1150:
            C_M = 1.0
        else:
            C_M = None
            print('Error! Check the input!')
        return C_M
    def Moisture_Condition(self, Material_type, MC):
        """
        Specifies if the entered material is classified as wet or dry
        :param Material_type: 'SL': Sawn Lumber
                            'PIJ': Prefabricated I-Joists
                            'SCL': Structural Composite Lumber
                            'WSP': Wooden Structural Panels
                            'CLT': Cross-Laminated Timber
        :param MC: Moisture Content
        """
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
    def C_t(self, Moisture_Condition, temperature):
        """
        Returns temperature factor (C_t) according to NDS 2024 Sec. 2.3.3
        :param Moisture_Condition: wet or dry identifier
        :param temperature: working temperature in degrees of Fahrenheit
        """
        if Moisture_Condition == True:
            if temperature <= 100:
                C_t =1.0
            elif temperature > 100 and temperature <= 125:
                C_t = 0.7
            elif temperature > 125 and temperature <= 150:
                C_t = 0.5
            else:
                C_t = None
                print('Error! The entered temperature value is not within range!')
        else:
            if temperature <= 100:
                C_t =1.0
            elif temperature > 100 and temperature <= 125:
                C_t = 0.8
            elif temperature > 125 and temperature <= 150:
                C_t = 0.7
            else:
                C_t = None
                print('Error! The entered temperature value is not within range!')
        return C_t
    def C_i(self, Incision_status):
        """
        Returns incising factor (C_i) according to Table 4.3.8 in NDS 2024
        :param Incision_status: An identifier showing weather the section is incised or not
        """
        if Incision_status == True:
            C_i = 0.8
        else:
            C_i = 1.0
        return C_i
    def C_r(self, breadth, Spacing):
        """
        Returns Repetitive member factor (C_r) according to NDS 2024 Sec. 4.3.9
        :param breadth: Breadth of the rectangular section
        :param Spacing: Center-to-center distance between members
        """
        if breadth == 2 or breadth == 3 or breadth == 4:
            if Spacing <= 24:
                C_r = 1.15
            else:
                C_r = 1.0
        else:
            C_r = None
            print('C_r is not applicable to this case!')
        return C_r
    def C_V(self, Volume, Species_Type):
        if Volume < 15498:
            C_V = 1.0
        else:
            if Species_Type == 'Southern Pine':
                C_V = pow((15498 / Volume), (1/20))
            else:
                C_V = pow((15498 / Volume), (1/10))
        return  C_V
    def C_c(self, Material_type, Curvature_status):
        """
        Returns Curvature Factor (C_c)
        :param Material_type: 'GLT' glued laminated timber
        :param Curvature_status: Indicates weather the member is curved or not
        """
        if Material_type == 'GLT':
            if Curvature_status == True:
                C_c = None
                print('C_c is not applicable to this case!')
            else:
                C_c = 1.0
        else:
            C_c = None
            print('C_c is not applicable to this case!')
        return C_c
    def C_I(self, Material_type, Taper_status):
        """
        Returns stress interaction factor (C_I)
        :param Material_type: 'GLT' : glued laminated timber
        :param Taper_status: Indicates weather the member is tapered or not
        """
        if Material_type == 'GLT':
            if Taper_status == True:
                C_I = None
                print('C_I is not applicable in this case!')
            else:
                C_I = 1.0
        else:
            C_I = None
            print('C_I is not applicable in this case!')
        return C_I
    def l_e(self, breadth, height, unsupported_length, Span_status, Loading_type):
        """
        Return effective length (le) according to Table 3.3.3 of NDS 2024
        :param breadth: Breadth of the rectangular section
        :param height: Height of the rectangular section
        :param unsupported_length: Laterally unsupported length of the member
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
        """
        if height > breadth and (unsupported_length/height) < 7:
            if Span_status =='Cantilever':
                if Loading_type == 'C':
                    le = 1.87 * unsupported_length
                elif Loading_type == 'U':
                    le = 1.33 * unsupported_length
                else:
                    le = 2.06 * unsupported_length
            elif Span_status == 'Single Span':
                if Loading_type == 'C':
                    le = 1.80 * unsupported_length
                elif Loading_type == 'U':
                    le = 2.06 * unsupported_length
                elif Loading_type == 'CL':
                    le = 1.111 * unsupported_length
                elif Loading_type =='Two_3' or Loading_type == 'Four_5':
                    le = 1.68 * unsupported_length
                elif Loading_type == 'Three_4':
                    le = 1.54 * unsupported_length
                elif Loading_type == 'Five_6':
                    le = 1.73 * unsupported_length
                elif Loading_type == 'Six_7':
                    le = 1.78 * unsupported_length
                elif Loading_type =='Seven or more' or Loading_type == 'Equal':
                    le = 1.84 * unsupported_length
                else:
                    le = 2.06 * unsupported_length
        elif height > breadth and (unsupported_length/height) >= 7:
            if Span_status =='Cantilever':
                if Loading_type == 'U':
                    le = (0.9 * unsupported_length) + (3 * height)
                elif Loading_type == 'C':
                    le = (1.44 * unsupported_length)+ (3 * height)
            elif Span_status == 'Single Span':
                if Loading_type == 'C':
                    le = (1.37 * unsupported_length) + (3 * height)
                elif Loading_type == 'U':
                    le = (1.63 * unsupported_length) + (3 * height)
                elif Loading_type == 'CL':
                    le = 1.111 * unsupported_length
                elif Loading_type =='Two_3' or Loading_type == 'Four_5':
                    le = 1.68 * unsupported_length
                elif Loading_type == 'Three_4':
                    le = 1.54 * unsupported_length
                elif Loading_type == 'Five_6':
                    le = 1.73 * unsupported_length
                elif Loading_type == 'Six_7':
                    le = 1.78 * unsupported_length
                elif Loading_type =='Seven or more' or Loading_type == 'Equal':
                    le = 1.84 * unsupported_length
                else:
                    if (unsupported_length/height)<= 14.3:
                        le = (1.63 * unsupported_length) + (3 * height)
                    else:
                        le = 1.84 * unsupported_length
        return le
    def R_B(self, effective_length, breadth, height):
        """
        Returns slenderness ratio of a given member
        :param effective_length: Effective length (le) according to Table 3.3.3 of NDS 2024
        :param breadth: Breadth of the rectangular section
        :param height: Height of the rectangular section
        """
        R_b = sqrt((effective_length * height) / pow(breadth,2))
        return R_b
