import math
radius=param("markings_tick_radius",101.0)
hour_len=param("markings_hour_length",8.0)
hour_w=param("markings_hour_width",4.0)
minute_len=param("markings_minute_length",6.0)
minute_w=param("markings_minute_width",0.9)
relief=param("markings_relief_height",0.6)
pieces=[]
# Fixed clock divisions: 60 minutes and 12 hours.
for i in range(60):
    angle=-i*6
    is_hour=(i%5==0)
    shape=Rectangle(hour_w if is_hour else minute_w,hour_len if is_hour else minute_len)
    tick=Rot(0,0,angle)*Pos(0,radius)*extrude(shape,amount=relief)
    pieces.extend(tick.solids())
for piece in pieces:
    piece.color=Color(1,1,1)
markings=Compound(children=pieces)
markings.color=Color(1,1,1)
publish("markings",markings,"White raised ticks",material="petg")