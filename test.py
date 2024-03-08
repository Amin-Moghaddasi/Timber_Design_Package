from TDP import Modified_E_min as me
from TDP import Modified_F_b as mfb
working_temperature = 99
properties = me(temperature=working_temperature, Incision_status=False, E_min=11200)
e_min_prime = properties.E_min_prime()
section = mfb(lamda=0.8, breadth=4, height=16, length=20, unsupported_length=1.3, Grade='No.1',
              MC=0.20, Material_type='SL', Fb= 1100, temperature=working_temperature
              , Incision_status=False,Spacing= 48, Species_Type='Hem-Fir',
              Curvature_status=False,Taper_status=False,Span_status='Single Span',
              Loading_type='U',E_min_prime=e_min_prime)
print('F_be:',section.F_b_E(),'F_b_*: ',section.F_b_asterisk())
print('phi:',section.Phi_b,'kf:', section.K_f,'C_I:', section.C_I(),'C_c:',section.C_c(),
      'C_fu:',section.C_fu(),'C_V:',section.C_V(),'C_M:',section.C_M(),'C_t:', section.C_t()
      ,'C_i:',section.C_i(), 'C_L:',section.C_L(), 'C_r:',section.C_r())
print("F_b_n_prime:",section.F_b_n_prime())
