import math
number_radius=param("numerals_radius",77.0)
number_h=param("numerals_height",28.0)
relief=param("numerals_relief_height",0.6)
pieces=[]
for hour in range(1,13):
    a=math.radians(hour*30)
    glyph=Text(str(hour),font_size=number_h,font="Arial",align=(Align.CENTER,Align.CENTER))
    glyph=scale(glyph,by=number_h/glyph.bounding_box().size.Y)
    bb=glyph.bounding_box()
    glyph=Pos(-(bb.min.X+bb.max.X)/2,-(bb.min.Y+bb.max.Y)/2)*glyph
    number=Pos(number_radius*math.sin(a),number_radius*math.cos(a))*extrude(glyph,amount=relief)
    assert len(number.solids())==len(str(hour))
    pieces.extend(number.solids())
assert len(pieces)==15
for piece in pieces:
    piece.color=Color(1,1,1)
numerals=Compound(children=pieces)
numerals.color=Color(1,1,1)
publish("numerals",numerals,"White raised numerals",material="petg")