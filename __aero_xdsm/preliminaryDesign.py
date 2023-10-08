# This file creates the XDSM diagram for the preliminary design phase that will be followed in the aero capstone class.

from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNC, LEFT, RIGHT

x = XDSM(use_sfmath=True)


## ADD ALL SYSTEMS VARIABLE FUNCTIONS
cd = "constraint_diagram"
perf_para = "perf_para"
ref_wing_des = "ref_wing_des"
tail_size = "tail_size"
fuse_size = "fuse_size"
UAV_geom = "UAV_geom"

## ADD ALL THE SYSTEMS
x.add_system(cd, FUNC, "Constraint \; Diagram")
x.add_system(perf_para, FUNC, "Performance \; Parameters")
x.add_system(ref_wing_des, FUNC, "Refined \; Wing \; Design")
x.add_system(tail_size, FUNC, "Tail \; Sizing")
x.add_system(fuse_size, FUNC, "Fuselage \; Sizing")
x.add_system(UAV_geom, FUNC, "UAV \; Configuration")


## ADD ALL THE INPUTS AND OUTPUTS
x.add_input(tail_size, (r"\text{Tail Config from Baseline}",
                         r"\bar{V}_H, \bar{V}_V, S_{h}, S_{v}, l_{opt},\text{etc}"),stack=True)

x.add_input(fuse_size, (r"\text{Battery Volume}",
                         r"\text{Fuse Config from Baseline}",
                         r"\text{Mission Specific Requirments}"),
                         stack=True)




# ADD ALL THE CONNECTIONS
x.connect(cd, perf_para, r"W_{TO}")
x.connect(cd, ref_wing_des, r"S_{ref}, T, P, C_{L_{max}}")
x.connect(ref_wing_des, tail_size, r"C_{L_{C}}")

## Write PDF
x.write("pdXDSM")


