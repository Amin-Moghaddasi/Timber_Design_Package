import Nail_Connections as nc
new_connection = nc.Single_shear_reference_Z(D=0.162,nail_length=3.5,t_m=3.5,t_s=1.5,
                                 side_member_type='W',G_m=0.55,G_s=0.55,Fe_s=None,
                                 nail_thread_status=False)
z = new_connection.reference_Z()
theta = 90
p= 1408
mz = nc.Modified_Z_Value(lamda=1,P=p,Z=z,Moisture_content_fab=0.21,Moisture_content_service=0.2,
                         D=0.162, temperature=99, grain_status=True, Nail_angle=theta)
mw = nc.Modified_W_Values(P=p,lamda=1,Moisture_content_fab=0.21,Moisture_content_service=0.2,
                          D=.162,D_H=0.344,W=31,W_H=160,temperature=99,grain_status=True,
                          Nail_angle=theta, nail_length=3.5, t_s=1.5)
print('lm = ',new_connection.l_m())
print('KD =',new_connection.K_D())
print('Re =',new_connection.R_e)
print('Rt',new_connection.R_t())
print('F_yb = ',new_connection.F_yb())
print('Fe_m =',new_connection.Fe_m)
print('Fe_s =',new_connection.Fe_s)
print('k1 =',new_connection.k1())
print('k2 =',new_connection.k2())
print('k3 =',new_connection.k3())
print('Z_I_m =',new_connection.Z_I_m())
print('Z_I_s =',new_connection.Z_I_s())
print('Z_II =',new_connection.Z_II())
print('Z_III_m =',new_connection.Z_III_m())
print('Z_III_s =',new_connection.Z_III_s())
print('Z_IV =',new_connection.Z_IV())
print('Reference Z value =',new_connection.reference_Z())
print('**********************************')
print('C_M =',mz.C_M())
print('C_t =',mz.C_t())
print('C_eg =',mz.C_eg)
print('C_tn =',mz.C_tn)
print('Z_n_prime =',mz.Z_n_Prime())
print('N = ',mz.Number_of_nails())
print('***********************************')
print('W_n_prime =',mw.W_n_prime())
print('W_H_n_prime =',mw.W_H_n_prime())
print('Number of nails for withdrawal = ',mw.Number_of_nails_withdrawal())
print('Number of nails for head pull =',mw.Number_of_nails_head_pull())
print('Chosen Number of nails =',mw.final_number_of_nails())


