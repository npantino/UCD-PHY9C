from itertools import permutations

# All 24 possible charge configurations as a 24x4 array
configs = []
charges = [-3, -1, 1, 3]
# Generate all possible configurations
for i in permutations(charges, 4):
    configs.append(list(i))

# Get potential energy distribution from an array
def potEnergy(config):
    U = 0
    # Iterate through all pairs of charges
    for i in range(0, 3):
        for j in range(i + 1, 4):        
            q1 = config[i] # Charge 1
            q2 = config[j] # Charge 2
            d = j - i # Distance between charges
            U += q1*q2/d # Electrostatic potential energy of q1 and q2. For real result, multiply by (q^2)/(4*pi*e0*d)
    return U

# Insert potential energies into 1st element of each config
for config in configs:    
    U = round(potEnergy(config), 3)
    config.insert(0, U)
# Sort configs from low to high
configs.sort()
# Print configs by row
for config in configs:  
    print(config)