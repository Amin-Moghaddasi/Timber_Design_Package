from Bolt_Connections import Single_shear_reference_Z as ssrz
from Bolt_Connections import  Double_shear_reference_Z as dsrz
from Bolt_Connections import Modified_Z_Value as mzv
from TDP import Modified_F_v, Modified_F_t
new_connection = ssrz(D=5/8,bolt_length=6,t_m=3.5,t_s=0.5,side_member_type='S',
                      G_s=None,G_m=0.43,main_member_orientation=45,side_member_orientation=45,
                      side_member_forge_type='Hot',angle_to_grain=45,F_e_s_um=58000)
F_v_prime = Modified_F_v(lamda=1,MC=0.18,Material_type='GLT',
                     Fv=265,temperature=99,Incision_status=False)
F_t_prime = Modified_F_t(lamda=1,height=12,Grade='Structural',
                         Ft=1100,temperature=99,Incision_status=False)
new_connection_1 = dsrz(D=1,bolt_length=45/8,t_m=41/8,t_s=0.25,G_s=None,F_e_s_um=58000,
                        G_m=0.5,main_member_orientation=0,side_member_orientation=0,
                        side_member_forge_type='Hot',angle_to_grain=0,side_member_type='S')
connection_design = mzv(P=None,lamda=1,Z=new_connection_1,Moisture_content_fab=0.1,
                        Moisture_content_service=0.1,D=1,temperature=99,connection_type='WS',
                        A_m=((41 * 12) / 8),A_s=(0.25 * 6),E_m=1700000,E_s=29000000,
                        n=3, s=4,load_type='T',load_orientation='Par',species_type='SW',
                        l_m=new_connection_1.l_m(),l_s=0.25,end_distance=7,edge_distance=1.5,
                        row_spacing=3,edge_type='UL',bolt_row_list=[3,3],height=12,
                        breadth=41/8, F_v_n_prime=F_v_prime.F_v_n_prime(),
                        F_t_n_prime=F_t_prime.F_t_n_prime())

print('lm = ',new_connection.l_m())
print('Theta_m =',new_connection.Theta_m)
print('Fe_m =',new_connection.F_em())
print('ls = ',new_connection.l_s)
print('Theta_s =',new_connection.Theta_s)
print('Fe_s =',new_connection.F_es())
print('R_e =',new_connection.R_e())
print('R_t =',new_connection.R_t())
print('K_theta =',new_connection.K_theta())
print('k1 =',new_connection.k1())
print('k2 =',new_connection.k2())
print('k3 =',new_connection.k3())
print('Z_I_m =',new_connection.Z_I_m())
print('Z_I_s =',new_connection.Z_I_s())
print('Z_II =',new_connection.Z_II())
print('Z_III_m =',new_connection.Z_III_m())
print('Z_III_s =',new_connection.Z_III_s())
print('Z_IV =',new_connection.Z_IV())
print('Chosen nominal Z value =',new_connection.reference_Z())
print('*********************Main Report*************************')
print('lm = ',new_connection_1.l_m())
print('Theta_m =',new_connection_1.Theta_m)
print('Fe_m =',new_connection_1.F_em())
print('ls = ',new_connection_1.l_s)
print('Theta_s =',new_connection_1.Theta_s)
print('Fe_s =',new_connection_1.F_es())
print('R_e =',new_connection_1.R_e())
print('R_t =',new_connection_1.R_t())
print('K_theta =',new_connection_1.K_theta())
print('k1 =',new_connection_1.k1())
print('k2 =',new_connection_1.k2())
print('k3 =',new_connection_1.k3())
print('Z_I_m =',new_connection_1.Z_I_m())
print('Z_I_s =',new_connection_1.Z_I_s())
print('Z_III_s =',new_connection_1.Z_III_s())
print('Z_IV =',new_connection_1.Z_IV())
print('Chosen Z value =',new_connection_1.reference_Z())
print('***********************************************')
print('F_t_n_prime =',F_t_prime.F_t_n_prime())
print('F_v_n_prime =',F_v_prime.F_v_n_prime())
print('A_net = ',connection_design.A_net)
print('Z_NT_n_prime = ',connection_design.Z_NT_prime())
print('Z_GT_n_prime = ',connection_design.Z_GT_prime())
print('Z_RT_n_prime =',connection_design.Z_RT_prime())
print('A_net_Group =',connection_design.A_net_group)
