w=param("base_width",92.0)
d=param("base_depth",94.0)
h=param("base_height",170.0)
wall=param("base_wall",4.0)
floor=param("base_floor",6.0)
cr=param("base_corner_radius",12.0)
pocket_front=param("base_storage_front",42.0)
socket=param("base_socket_width",20.5)
socket_depth=param("base_socket_depth",25.5)
socket_y=param("base_socket_y",18.0)
# Local origin at centre of front edge on the desk.
shell=extrude(Pos(0,d/2)*RectangleRounded(w,d,cr),amount=h)
pocket_d=d-wall-pocket_front
pocket=Pos(0,pocket_front+pocket_d/2,floor)*extrude(RectangleRounded(w-2*wall,pocket_d,cr-wall),amount=h)
shell=shell-pocket
shell=shell-Pos(0,socket_y,h-socket_depth)*Box(socket,socket,socket_depth+1,align=(Align.CENTER,Align.CENTER,Align.MIN))
shell.color=Color(0.96,0.58,0.035)
assert len(shell.solids())==1
publish("base",shell,"Storage base",material="petg")