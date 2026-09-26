dia=param("body_diameter",240.0)
depth=param("body_depth",32.0)
wall=param("body_wall",2.7)
back=param("body_back_thickness",3.5)
seat_z=param("body_seat_height",25.8)
seat_thick=param("body_seat_thickness",2.8)
seat_width=param("body_seat_width",5.3)
# Legacy parameter ids retained; these dimensions now drive true tangent radii.
rear_bevel=param("body_rear_chamfer",7.0)
front_bevel=param("body_front_chamfer",1.0)
mouth_radius=param("body_inner_lip_radius",0.8)
tilt=param("body_tilt_angle",8.0)
locator_w=param("body_locator_width",12.5)
locator_depth=param("body_locator_depth",1.2)
locator_y=param("body_locator_y",-24.0)
r=dia/2
blank=Cylinder(r,depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
rear_edges=[e for e in blank.edges() if e.geom_type==GeomType.CIRCLE and abs(e.center().Z)<1e-6]
blank=fillet(rear_edges,radius=rear_bevel)
front_edges=[e for e in blank.edges() if e.geom_type==GeomType.CIRCLE and abs(e.center().Z-depth)<1e-6]
blank=fillet(front_edges,radius=front_bevel)
inner_r=r-wall
inner_start=r-rear_bevel-back
ramp=inner_r-inner_start
cavity=Pos(0,0,back)*Cone(inner_start,inner_r,ramp,align=(Align.CENTER,Align.CENTER,Align.MIN))
cavity=cavity+Pos(0,0,back+ramp)*Cylinder(inner_r,depth,align=(Align.CENTER,Align.CENTER,Align.MIN))
shell=blank-cavity
mouth_edges=[e for e in shell.edges() if e.geom_type==GeomType.CIRCLE and abs(e.center().Z-depth)<1e-6 and abs(e.radius-inner_r)<1e-6]
assert len(mouth_edges)==1
shell=fillet(mouth_edges,radius=mouth_radius)
ledge=Pos(0,0,seat_z-seat_thick)*extrude(Circle(inner_r)-Circle(inner_r-seat_width),amount=seat_thick)
# Blind glue pocket, normal to the rear face; leaves 2.3 mm closed back.
pocket=Pos(0,locator_y,-1)*Box(locator_w,locator_w,locator_depth+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
body=Rot(-tilt,0,0)*(shell+ledge-pocket)
body.color=Color(0.94,0.53,0.025)
assert len(body.solids())==1
publish("body",body,"Recessed clock body",material="petg")