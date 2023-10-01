from atmosphere import Atmosphere

# Writing for the cruise condition
altitude = 500 # [m]

l = 0.33 # [m]
air = Atmosphere(altitude, altitude_in_feet=False)
rho = air.density
nu = air.kinematic_viscosity
velocity = 55 # [m/s]

Re = (velocity * l) / nu
print(Re)

