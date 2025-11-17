import numpy as np

# TODO: Optimize code with arrays

# Get circuit info
R1_str = input("R1: ")
R1 = float(R1_str)
R2_str = input("R2: ")
R2 = float(R2_str)
R3_str = input("R3: ")
R3 = float(R3_str)
R4_str = input("R4: ")
R4 = float(R4_str)
R5_str = input("R5: ")
R5 = float(R5_str)
E1_str = input("E1: ")
E1 = float(E1_str)
E2_str = input("E2: ")
E2 = float(E2_str)
S1 = input("Is S1 open or closed: ")
S2 = input("Is S2 open or closed: ")


# Calculate matrices needed for loop currents
# R matrix derived from mesh current method
# I are loop currents, all counter-clockwise from left to right of circuit
# RI = V, so I = inv(R) * V. Do matrix multiplication.
R = np.array([[-R1 - R2, R2, 0],
     [R2, -R2 - R3 - R4, R4],
     [0, R4, -R4 - R5]])
V = np.transpose(np.atleast_2d([-E1, E2, 0]))

# Initialize real currents
I1 = 0
I2 = 0
I3 = 0
I4 = 0
I5 = 0

# Modify matrices based on S1 and S2

open1 = (S1 == "open")
open2 = (S2 == "open")

# Both S1 and S2 are open
# Remove rows 0 and 2, cols 0 and 2 of R, and remove rows 0 and 2 of V
if (open1 & open2):
    R = R[1, 1]
    V = V[1]
    I = np.matmul(np.linalg.inv(R), V)
    # Calculate real currents
    # Matrix indices reduced by 1
    I1 = 0
    I2 = -I[0]
    I3 = -I[0]
    I4 = -I[0]
    I5 = 0

# S1 is open, S2 is closed
# Remove row 0, col 0 of R, and remove row 0 of V
elif (open1):
    R = R[1:, 1:] # Numpy array slicing
    V = V[1:]
    I = np.matmul(np.linalg.inv(R), V)
    # Calculate real currents
    # Matrix indices reduced by 1
    I1 = 0
    I2 = -I[0]
    I3 = -I[0]
    I4 = I[1] - I[0]
    I5 = -I[1][0]

# S1 is closed, S2 is open
# Remove row 2, col 2 of R, and remove row 2 of V
elif (open2):
    R = R[:2, :2]
    V = V[:2]
    I = np.matmul(np.linalg.inv(R), V)
    # Calculate real currents
    I1 = I[0][0]
    I2 = I[0] - I[1]
    I3 = -I[1]
    I4 = -I[1]
    I5 = 0

# Both S1 and S2 are closed
else:
    I = np.matmul(np.linalg.inv(R), V)
    # Calculate real currents
    I1 = I[0][0]
    I2 = I[0] - I[1]
    I3 = -I[1]
    I4 = I[2] - I[1]
    I5 = -I[2][0]

# Turn remaining 1x1 arrays into literals
I2 = I2[0]
I3 = I3[0]
I4 = I4[0]

# Calculate voltages relative to point f
Va = E1 - I1 * R1
Vb = I2 * R2
Vc = E2 - I4 * R4
Vd = E2 - I5 * R5
Ve = E2
Vf = 0

# Calculate power of each component. 
# Resistor, I^2 * R. Emf source, -I * V.
# P > 0, absorbs energy. P < 0, gives energy to the circuit.
# Net power should be 0 W.
PR1 = pow(I1, 2) * R1
PR2 = pow(I2, 2) * R2
PR3 = pow(I3, 2) * R3
PR4 = pow(I4, 2) * R4
PR5 = pow(I5, 2) * R5
PE1 = -E1 * I1
PE2 = -E2 * (I2 - I1)
Pnet = PR1 + PR2 + PR3 + PR4 + PR5 + PE1 + PE2

# Print results
# Negative currents indicate the real current flows in the opposite direction
I1_str = str(round(I1, 4))
I2_str = str(round(I2, 4))
I3_str = str(round(I3, 4))
I4_str = str(round(I4, 4))
I5_str = str(round(I5, 4))

Va_str = str(round(Va, 4))
Vb_str = str(round(Vb, 4))
Vc_str = str(round(Vc, 4))
Vd_str = str(round(Vd, 4))
Ve_str = str(round(Ve, 4))
Vf_str = str(round(Vf, 4))

PR1_str = str(round(PR1, 4))
PR2_str = str(round(PR2, 4))
PR3_str = str(round(PR3, 4))
PR4_str = str(round(PR4, 4))
PR5_str = str(round(PR5, 4))
PE1_str = str(round(PE1, 4))
PE2_str = str(round(PE2, 4))
Pnet_str = str(round(Pnet, 4))


print("\nI1: " + I1_str + " A")
print("I2: " + I2_str + " A")
print("I3: " + I3_str + " A")
print("I4: " + I4_str + " A")
print("I5: " + I5_str + " A")

print("\nVa: " + Va_str + " V")
print("Vb: " + Vb_str + " V")
print("Vc: " + Vc_str + " V")
print("Vd: " + Vd_str + " V")
print("Ve: " + Ve_str + " V")
print("Vf: " + Vf_str + " V")

print("\nPR1: " + PR1_str + " W")
print("PR2: " + PR2_str + " W")
print("PR3: " + PR3_str + " W")
print("PR4: " + PR4_str + " W")
print("PR5: " + PR5_str + " W")
print("PE1: " + PE1_str + " W")
print("PE2: " + PE2_str + " W")
print("Pnet: " + Pnet_str + " W")