# This file creates the XDSM diagram for the preliminary design phase that will be followed in the aero capstone class.

from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNC, LEFT, RIGHT

x = XDSM(use_sfmath=True)


## ADD ALL SYSTEMS VARIABLE FUNCTIONS
cd = "conceptial_design"
perf_para = "perf_para"
ref_wing_des = "ref_wing_des"
tail_size = "tail_size"
fuse_size = "fuse_size"
UAV_geom = "UAV_geom"

## ADD ALL THE SYSTEMS
x.add_system(cd, FUNC, "Conceptual \; Design")
x.add_system(perf_para, FUNC, "Performance \; Analysis")
x.add_system(ref_wing_des, FUNC, "Wing \ Sizing")
x.add_system(tail_size, FUNC, "Tail \; Sizing")
x.add_system(fuse_size, FUNC, "Fuselage \; Sizing")
x.add_system(UAV_geom, FUNC, "Preliminary \ Design")


## ADD ALL THE INPUTS AND OUTPUTS
x.add_input(tail_size, (r"\text{Tail Config from Baseline}",
                         r"\bar{V}_H, \bar{V}_V, S_{h}, S_{v}, l_{opt},\text{etc}"),stack=True)

x.add_input(fuse_size, (r"\text{Payload Dimensions}",
                         r"\text{Design Requirements/Constraints}",
                         r"\text{Mission Specific Requirements}"),
                         stack=True)

x.add_input(perf_para, r"\text{Initial Guesses}")
#x.add_input(ref_wing_des, r"\text{Airfoil}")


# ADD ALL THE CONNECTIONS
x.connect(cd, perf_para, r"W_{TO}")
x.connect(perf_para, tail_size, r"\text{Aircraft CG}")
x.connect(cd, ref_wing_des, r"S_{ref}, T, P, C_{L_{max}}")
x.connect(ref_wing_des, tail_size, r"C_{L_{C}}, C_{m}, MAC, i_w")
x.connect(ref_wing_des, fuse_size, r"\text{Wing Placement}")
x.connect(tail_size, fuse_size, "Tail \ Placement, L_f")
x.connect(ref_wing_des, perf_para, r"\text{Stability Analysis}")
x.connect(tail_size, perf_para, r"\text{Stability Analysis}")
x.connect(UAV_geom, perf_para, r"\text{Revised Requirements}")
x.connect(fuse_size, UAV_geom, r"Fuselage\ Geometry")
x.connect(fuse_size, perf_para, r"C_{L_{UAV}}, C_{D_{UAV}}")
x.connect(perf_para, ref_wing_des, r"Design \ Requirements")
x.connect(UAV_geom, ref_wing_des, r"UAV \ Lift ")

# Results
x.connect(ref_wing_des, UAV_geom, r"Wing \ Geometry")
x.connect(tail_size, UAV_geom, r"Tail\ Geometry")
x.connect(fuse_size, UAV_geom, r"Fuselage\ Geometry")

x.add_output(UAV_geom, "Outer \ Mold \ Line ")
## Write PDF
x.write("pdXDSM")


