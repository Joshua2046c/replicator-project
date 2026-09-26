diameter=param("dial_diameter",234.0)
flat_diameter=param("dial_flat_diameter",216.0)
thickness=param("dial_thickness",2.4)
rise=param("dial_edge_rise",3.0)
hole=param("dial_shaft_hole_diameter",10.0)
lip_radius=param("dial_lip_radius",1.0)
back_radius=param("dial_back_edge_radius",0.5)
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
lip_edges=[e for e in dial.edges() if e.geom_type==GeomType.CIRCLE and abs(e.center().Z-(thickness+rise))<1e-6]
assert len(lip_edges)==1
dial=fillet(lip_edges,radius=lip_radius)
back_edges=[e for e in dial.edges() if e.geom_type==GeomType.CIRCLE and abs(e.center().Z)<1e-6 and abs(e.radius-r)<1e-6]
assert len(back_edges)==1
dial=fillet(back_edges,radius=back_radius)
# Exact analytic surface partition for portable smooth meshing.
# 3 degree patches retain the same circular surfaces and G1 tangent joins.
# This bounds a possible perimeter chord sag to 0.042 mm at radius 120 mm.
import math
from OCP.ShapeUpgrade import ShapeUpgrade_ShapeDivideAngle
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
def precise_volume(shape):
    props=GProp_GProps()
    BRepGProp.VolumeProperties_s(shape.wrapped,props,1e-9)
    return props.Mass()
_before_volume=precise_volume(dial)
divider=ShapeUpgrade_ShapeDivideAngle(math.radians(3.0),dial.wrapped)
divider.Perform()
dial=Part(divider.Result())
assert len(dial.solids())==1
assert abs(precise_volume(dial)-_before_volume)<0.001, (precise_volume(dial),_before_volume)
dial.color=Color(1.0,0.68,0.045)
assert len(dial.solids())==1
assert flat_diameter/2>102
publish("dial",dial,"Nested dial",material="petg")