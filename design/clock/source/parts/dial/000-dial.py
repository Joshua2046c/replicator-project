diameter=param("dial_diameter",234.0)
flat_diameter=param("dial_flat_diameter",216.0)
thickness=param("dial_thickness",2.4)
rise=param("dial_edge_rise",3.0)
hole=param("dial_shaft_hole_diameter",10.0)
r=diameter/2
f=flat_diameter/2
width=r-f
curve_radius=(width*width+rise*rise)/(2*rise)
midrise=curve_radius-(curve_radius*curve_radius-(width/2)**2)**0.5
with BuildPart() as plate:
    with BuildSketch(Plane.XZ):
        with BuildLine():
            Polyline((hole/2,0),(r,0),(r,thickness+rise))
            ThreePointArc((r,thickness+rise),(f+width/2,thickness+midrise),(f,thickness))
            Polyline((f,thickness),(hole/2,thickness),(hole/2,0))
        make_face()
    revolve(axis=Axis.Z)
dial=plate.part
dial.color=Color(1.0,0.68,0.045)
assert len(dial.solids())==1
assert flat_diameter/2>102
publish("dial",dial,"Nested dial",material="petg")