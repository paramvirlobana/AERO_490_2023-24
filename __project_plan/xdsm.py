from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNC, LEFT, RIGHT

x = XDSM(use_sfmath=True)


x.add_system("airfoil_selection", FUNC, "Airfoil \; Selection")
x.add_system("wing_geomtry", FUNC, "Wing \; Geometry")
x.add_system("constraint_diagram", FUNC, "Constraint \; Diagram")
x.add_system("geom_size", FUNC, r"Geometry \; Sizing \; (Fuselage, Tail, etc)")

x.add_input("airfoil_selection", "Requirements\;  2, 3, 12")
x.add_input("wing_geomtry", "Requirements\;  1, 2, 3, 12")
x.add_input("constraint_diagram", "Mission \; Profile")

x.connect("airfoil_selection", "wing_geomtry", "c_l, c_d")
x.connect("wing_geomtry", "constraint_diagram", " C_L, C_D, Span")
x.connect("constraint_diagram", "geom_size", "T/W, \; W/S")

x.connect("constraint_diagram", "wing_geomtry", "Wing \; Loading")
x.connect("geom_size", "wing_geomtry", "MTOW, Range")
x.connect("wing_geomtry", "airfoil_selection", "Efficiency")
x.add_output("geom_size", r"Conceptual \; Design", side=RIGHT)
x.add_output("airfoil_selection", r"\alpha, Re", side=LEFT)
x.write("mdf")
