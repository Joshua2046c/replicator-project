import math
w=param("base_width",84.0)
d=param("base_depth",90.0)
h=param("base_height",160.0)
wall=param("base_wall",3.0)
floor=param("base_floor",6.0)
cr=param("base_corner_radius",18.0)
pocket_front=param("base_storage_front",38.0)
lip=param("base_lip_radius",0.8)
tilt=param("base_contact_angle",16.0)
foot=param("base_front_foot_extension",10.0)
waist=param("base_neck_inset",24.0)
neck_z=param("base_neck_underside_height",114.0)
rear_inset=param("base_rear_inset",8.0)
loc_w=param("base_locator_width",12.5)
loc_depth=param("base_locator_depth",4.2)
loc_drop=param("base_locator_drop",15.069719297)
slope=math.tan(math.radians(tilt))
neck_front=(neck_z-h)*slope
# Continuous side profile: splayed foot, concave throat, forward neck.
p0=(-foot,0)
p1=(waist*0.8,neck_z-30)
p2=(neck_front,neck_z)
with BuildPart() as blank:
    with BuildSketch(Plane.YZ):
        with BuildLine():
            Line(p0,p1)
            Bezier(p1,(waist*1.45,neck_z+1),(waist*0.4,neck_z+1),p2)
            Polyline(p2,(0,h),(d,h),(d-rear_inset,0),p0)
        make_face()
    extrude(amount=w/2,both=True)
shell=blank.part
# Round the two side boundaries, preserving the flat top and foot.
side_edges=[e for e in shell.edges() if abs(abs(e.center().X)-w/2)<0.001 and e.center().Z>0.001 and e.center().Z<h-0.001]
shell=fillet(side_edges,radius=cr)
def inner_section(z,front):
    rear=d-rear_inset*(1-z/h)-wall
    return Pos(0,(front+rear)/2,z)*RectangleRounded(w-2*wall,rear-front,cr-wall)
inner_floor_front=max(pocket_front,waist+wall+cr/2)
pocket=loft([inner_section(floor,inner_floor_front),inner_section(h,pocket_front),inner_section(h+1,pocket_front)],ruled=True)
shell=shell-pocket
rim=[e for e in shell.edges() if abs(e.center().Z-h)<0.001]
shell=fillet(rim,radius=lip)
loc_z=h-loc_drop
loc_y=-loc_drop*slope
# Blind recess normal to the mating surface, fully covered after bonding.
pocket_cut=Pos(0,loc_y,loc_z)*Rot(90-tilt,0,0)*Pos(0,0,-loc_depth)*Box(loc_w,loc_w,loc_depth+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
shell=shell-pocket_cut
shell.color=Color(0.96,0.58,0.035)
assert len(shell.solids())==1
publish("base",shell,"Extended neck base",material="petg")