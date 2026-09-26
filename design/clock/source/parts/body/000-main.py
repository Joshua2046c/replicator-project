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
locator_w=param("body_locator_width",12.5)
locator_depth=param("body_locator_depth",1.2)
locator_y=param("body_locator_y",-24.0)
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
# Blind glue pocket, normal to the rear face; leaves 2.3 mm closed back.
pocket=Pos(0,locator_y,-1)*Box(locator_w,locator_w,locator_depth+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
body=Rot(-tilt,0,0)*(shell+ledge-pocket)
body.color=Color(0.94,0.53,0.025)
assert len(body.solids())==1
publish("body",body,"Recessed clock body",material="petg")