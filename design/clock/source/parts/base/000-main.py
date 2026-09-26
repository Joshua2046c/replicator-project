import math
w=param("base_width",84.0)
d=param("base_depth",90.0)
h=param("base_height",160.0)
wall=param("base_wall",3.0)
floor=param("base_floor",6.0)
cr=param("base_corner_radius",18.0)
pocket_front=param("base_storage_front",38.0)
socket=param("base_socket_width",20.5)
socket_depth=param("base_socket_depth",25.5)
socket_y=param("base_socket_y",18.0)
lip=param("base_lip_radius",0.8)
tilt=param("base_contact_angle",16.0)
contact_h=param("base_contact_height",30.0)
root_h=param("base_root_recess_height",15.25)
slope=math.tan(math.radians(tilt))
shoulder=-contact_h*slope
def section(z,front):
    return Pos(0,(d+front)/2,z)*RectangleRounded(w,d-front,cr)
lower=loft([section(0,0),section(h*0.38,0),section(h-contact_h*1.8,shoulder*0.8),section(h-contact_h,shoulder)])
upper=loft([section(h-contact_h,shoulder),section(h,0)],ruled=True)
shell=lower+upper
# Keep the entire base behind the body's rear tangent plane.
clip=Plane.YZ*Polygon((-2*d,-1),(slope*(-1-h),-1),(slope,h+1),(-2*d,h+1),align=None)
shell=shell-extrude(clip,amount=w,both=True)
pocket_d=d-wall-pocket_front
pocket=Pos(0,pocket_front+pocket_d/2,floor)*extrude(RectangleRounded(w-2*wall,pocket_d,cr-wall),amount=h)
shell=shell-pocket
rim=[e for e in shell.edges() if abs(e.center().Z-h)<0.001]
shell=fillet(rim,radius=lip)
shell=shell-Pos(0,socket_y,h-socket_depth)*Box(socket,socket,socket_depth+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Open-front recess is fully concealed by the assembled closed-back disc.
recess_front=shoulder-wall
recess_back=socket_y+socket/2
shell=shell-Pos(0,(recess_front+recess_back)/2,h-root_h)*Box(socket,recess_back-recess_front,root_h+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
shell.color=Color(0.96,0.58,0.035)
assert len(shell.solids())==1
publish("base",shell,"Tangent storage base",material="petg")