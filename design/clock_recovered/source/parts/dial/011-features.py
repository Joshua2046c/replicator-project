# recovery_step: exact solid 2 from STEP SHA256 5ace57df0fda9a15847270cbe66048984c366595415927b0751c0765d7b14559.
# Embedded analytic topology preserves curved surfaces and avoids a duplicate published import.
from io import BytesIO
import base64, zlib, hashlib
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Shape

_raw_brep=zlib.decompress(base64.b64decode(_encoded_brep))
assert hashlib.sha256(_raw_brep).hexdigest()=="a33a0040aed3a511e676ba3def7fb1d44ebfbfa7ebb9a2500cf50b43dd954122"
_wrapped=TopoDS_Shape()
BRepTools.Read_s(_wrapped,BytesIO(_raw_brep),BRep_Builder())
source=Solid(_wrapped)
assert source.is_valid and len(source.solids())==1
dial_back_z=param("dial_back_height",26.0)
s=Pos(0,0,dial_back_z-26)*source
s.color=srgb("#F5A313")
publish("dial",s,"一体表盘",material="petg")