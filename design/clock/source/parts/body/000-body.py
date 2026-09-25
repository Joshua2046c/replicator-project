dia=param("body_diameter",240.0)
depth=param("body_depth",32.0)
wall=param("body_wall",2.7)
back=param("body_back_thickness",3.5)
seat_z=param("body_seat_height",25.8)
seat_thick=param("body_seat_thickness",2.8)
seat_width=param("body_seat_width",5.3)
rear_bevel=param("body_rear_chamfer",7.0)
front_bevel=param("body_front_chamfer",1.0)
tilt=param("body_tilt_angle",8.0)
neck_w=param("body_neck_width",56.0)
neck_h=param("body_neck_height",18.0)
neck_reach=param("body_neck_reach",36.0)
neck_y=param("body_neck_vertical",-50.0)
neck_root=param("body_neck_root_depth",12.0)
neck_blend=param("body_neck_corner_radius",4.0)
tenon=param("body_tenon_width",20.0)
tenon_l=param("body_tenon_length",25.0)
tenon_offset=param("body_tenon_rear_offset",18.0)
# Disc is angled relative to the upright tenon within this rigid part.
r=dia/2
with BuildPart() as blank:
    with BuildSketch(Plane.XZ):
        with BuildLine():
            Polyline((0,0),(r-rear_bevel,0),(r,rear_bevel),(r,depth-front_bevel),(r-front_bevel,depth),(0,depth),close=True)
        make_face()
    revolve(axis=Axis.Z)
inner_r=r-wall
inner_start=r-rear_bevel-back
ramp=inner_r-inner_start
cavity=Pos(0,0,back)*Cone(inner_start,inner_r,ramp,align=(Align.CENTER,Align.CENTER,Align.MIN))
cavity=cavity+Pos(0,0,back+ramp)*Cylinder(inner_r,depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
shell=blank.part-cavity
ledge=Pos(0,0,seat_z-seat_thick)*extrude(Circle(inner_r)-Circle(inner_r-seat_width),amount=seat_thick)
shell=Rot(-tilt,0,0)*(shell+ledge)
neck=Pos(0,neck_y+neck_h/2,(neck_root-neck_reach)/2)*Box(neck_w,neck_h,neck_reach+neck_root)
neck=fillet(neck.edges(),radius=neck_blend)
pin=Pos(0,neck_y-tenon_l,-tenon_offset)*Box(tenon,tenon_l+neck_h/2,tenon,align=(Align.CENTER,Align.MIN,Align.CENTER))
# Preserve the seating ledge; hollow only the support where it enters the existing cavity.
body=shell+((neck+pin)-(Rot(-tilt,0,0)*cavity))
body.color=Color(0.94,0.53,0.025)
assert len(body.solids())==1
publish("body",body,"Closed clock body",material="petg")