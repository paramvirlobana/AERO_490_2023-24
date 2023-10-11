import numpy as np
import openmdao.api as om
from openaerostruct.geometry.utils import generate_mesh
from openaerostruct.geometry.geometry_group import Geometry
from openaerostruct.aerodynamics.aero_groups import AeroPoint

prob = om.Problem()

indep_var_comp = om.IndepVarComp()
indep_var_comp.add_output("v", val=248.136, units="m/s")  # Freestream Velocity
indep_var_comp.add_output("alpha", val=5.0, units="deg")  # Angle of Attack
indep_var_comp.add_output("beta", val=0.0, units="deg")  # Sideslip angle
indep_var_comp.add_output("omega", val=np.zeros(3), units="deg/s")  # Rotation rate
indep_var_comp.add_output("Mach_number", val=0.0)  # Freestream Mach number
indep_var_comp.add_output("re", val=1.0e6, units="1/m")  # Freestream Reynolds number
indep_var_comp.add_output("rho", val=0.38, units="kg/m**3")  # Freestream air density
indep_var_comp.add_output("cg", val=np.zeros((3)), units="m")  # Aircraft center of gravity
prob.model.add_subsystem("flight_vars", indep_var_comp, promotes=["*"])

half_span = 3.56/2
kink_location = half_span/2

root_chord = 0.356
tip_chord = 0.3
kink_chord = (root_chord + tip_chord)/2

inboard_LE_sweep = 0 
outboard_LE_sweep = 0

# Specify Mesh
nx = 10 # Chordwise nodal points
ny_outboard, ny_inboard = 10, 10 # Spanwise nodal points

mesh = np.zeros((nx, ny_inboard + ny_outboard - 1, 3))

mesh[:, :ny_outboard, 1] = np.linspace(half_span, kink_location, ny_outboard)
# Inboard
mesh[:, ny_outboard : ny_outboard + ny_inboard, 1] = np.linspace(kink_location, 0, ny_inboard)[1:]

x_LE = np.zeros(ny_inboard + ny_outboard - 1)
array_for_inboard_leading_edge_x_coord = np.linspace(0, kink_location, ny_inboard) * np.tan(
    inboard_LE_sweep / 180.0 * np.pi
)

array_for_outboard_leading_edge_x_coord = (
    np.linspace(0, half_span - kink_location, ny_outboard) * np.tan(outboard_LE_sweep / 180.0 * np.pi)
    + np.ones(ny_outboard) * array_for_inboard_leading_edge_x_coord[-1]
)

x_LE[:ny_inboard] = array_for_inboard_leading_edge_x_coord
x_LE[ny_inboard : ny_inboard + ny_outboard] = array_for_outboard_leading_edge_x_coord[1:]

# Then the trailing edge
x_TE = np.zeros(ny_inboard + ny_outboard - 1)

array_for_inboard_trailing_edge_x_coord = np.linspace(
    array_for_inboard_leading_edge_x_coord[0] + root_chord,
    array_for_inboard_leading_edge_x_coord[-1] + kink_chord,
    ny_inboard,
)

array_for_outboard_trailing_edge_x_coord = np.linspace(
    array_for_outboard_leading_edge_x_coord[0] + kink_chord,
    array_for_outboard_leading_edge_x_coord[-1] + tip_chord,
    ny_outboard,
)

x_TE[:ny_inboard] = array_for_inboard_trailing_edge_x_coord
x_TE[ny_inboard : ny_inboard + ny_outboard] = array_for_outboard_trailing_edge_x_coord[1:]

# # Quick plot to check leading and trailing edge x-coords
# plt.plot(x_LE, np.arange(0, ny_inboard+ny_outboard-1), marker='*')
# plt.plot(x_TE, np.arange(0, ny_inboard+ny_outboard-1), marker='*')
# plt.show()
# exit()

for i in range(0, ny_inboard + ny_outboard - 1):
    mesh[:, i, 0] = np.linspace(np.flip(x_LE)[i], np.flip(x_TE)[i], nx)

#Define the airfoil
# fmt: off
upper_x = np.array([0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6], dtype="complex128")
lower_x = np.array([0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 0.6], dtype="complex128")
upper_y = np.array([ 0.0447,  0.046,  0.0472,  0.0484,  0.0495,  0.0505,  0.0514,  0.0523,  0.0531,  0.0538, 0.0545,  0.0551,  0.0557, 0.0563,  0.0568, 0.0573,  0.0577,  0.0581,  0.0585,  0.0588,  0.0591,  0.0593,  0.0595,  0.0597,  0.0599,  0.06,    0.0601,  0.0602,  0.0602,  0.0602,  0.0602,  0.0602,  0.0601,  0.06,    0.0599,  0.0598,  0.0596,  0.0594,  0.0592,  0.0589,  0.0586,  0.0583,  0.058,   0.0576,  0.0572,  0.0568,  0.0563,  0.0558,  0.0553,  0.0547,  0.0541], dtype="complex128")  # noqa: E201, E241
lower_y = np.array([-0.0447, -0.046, -0.0473, -0.0485, -0.0496, -0.0506, -0.0515, -0.0524, -0.0532, -0.054, -0.0547, -0.0554, -0.056, -0.0565, -0.057, -0.0575, -0.0579, -0.0583, -0.0586, -0.0589, -0.0592, -0.0594, -0.0595, -0.0596, -0.0597, -0.0598, -0.0598, -0.0598, -0.0598, -0.0597, -0.0596, -0.0594, -0.0592, -0.0589, -0.0586, -0.0582, -0.0578, -0.0573, -0.0567, -0.0561, -0.0554, -0.0546, -0.0538, -0.0529, -0.0519, -0.0509, -0.0497, -0.0485, -0.0472, -0.0458, -0.0444], dtype="complex128")
# fmt: on

# Define input surface dictionary for our wing
surface = {
    # Wing definition
    "name": "wing",  # name of the surface
    "symmetry": True,  # if true, model one half of wing
    # reflected across the plane y = 0
    "S_ref_type": "wetted",  # how we compute the wing area,
    # can be 'wetted' or 'projected'
    "fem_model_type": "tube",
    "twist_cp": np.array([0.0, 0.0, 0.0, 0.0]),
    "mesh": mesh,
    "data_x_upper": upper_x,
    "data_x_lower": lower_x,
    "data_y_upper": upper_y,
    "data_y_lower": lower_y,
    # Aerodynamic performance of the lifting surface at
    # an angle of attack of 0 (alpha=0).
    # These CL0 and CD0 values are added to the CL and CD
    # obtained from aerodynamic analysis of the surface to get
    # the total CL and CD.
    # These CL0 and CD0 values do not vary wrt alpha.
    "CL0": 0.0,  # CL of the surface at alpha=0
    "CD0": 0.015,  # CD of the surface at alpha=0
    # Airfoil properties for viscous drag calculation
    "k_lam": 0.05,  # percentage of chord with laminar
    # flow, used for viscous drag
    "t_over_c_cp": np.array([0.15]),  # thickness over chord ratio (NACA0015)
    "c_max_t": 0.303,  # chordwise location of maximum (NACA0015)
    # thickness
    "with_viscous": True,  # if true, compute viscous drag
    "with_wave": False,  # if true, compute wave drag
} # end of surface dictionary




# Create the OpenMDAO problem
prob = om.Problem()

# Create an independent variable component that will supply the flow
# conditions to the problem.
indep_var_comp = om.IndepVarComp()
indep_var_comp.add_output("v", val=24.136, units="m/s")
indep_var_comp.add_output("alpha", val=5.0, units="deg")
indep_var_comp.add_output("Mach_number", val=0.162)
indep_var_comp.add_output("re", val=500000, units="1/m")
indep_var_comp.add_output("rho", val=0.8, units="kg/m**3")
indep_var_comp.add_output("cg", val=np.zeros((3)), units="m")

# Add this IndepVarComp to the problem model
prob.model.add_subsystem("prob_vars", indep_var_comp, promotes=["*"])

# Create and add a group that handles the geometry for the
# aerodynamic lifting surface
geom_group = Geometry(surface=surface)
prob.model.add_subsystem(surface["name"], geom_group)

# Create the aero point group, which contains the actual aerodynamic
# analyses
aero_group = AeroPoint(surfaces=[surface])
point_name = "aero_point_0"
prob.model.add_subsystem(
    point_name, aero_group, promotes_inputs=["v", "alpha", "Mach_number", "re", "rho", "cg"]
)

name = surface["name"]

# Connect the mesh from the geometry component to the analysis point
prob.model.connect(name + ".mesh", point_name + "." + name + ".def_mesh")

# Perform the connections with the modified names within the
# 'aero_states' group.
prob.model.connect(name + ".mesh", point_name + ".aero_states." + name + "_def_mesh")

prob.model.connect(name + ".t_over_c", point_name + "." + name + "_perf." + "t_over_c")

# Import the Scipy Optimizer and set the driver of the problem to use
# it, which defaults to an SLSQP optimization method
prob.driver = om.ScipyOptimizeDriver()
prob.driver.options["tol"] = 1e-9


recorder = om.SqliteRecorder("omg.db")
prob.driver.add_recorder(recorder)
prob.driver.recording_options["record_derivatives"] = True
prob.driver.recording_options["includes"] = ["*"]

# Setup problem and add design variables, constraint, and objective
prob.model.add_design_var("wing.twist_cp", lower=-10.0, upper=15.0)
prob.model.add_constraint(point_name + ".wing_perf.CL", equals=0.5)
prob.model.add_objective(point_name + ".wing_perf.CD", scaler=1e4)

# Set up and run the optimization problem
prob.setup()

prob.run_driver()