# recovery_step: exact solid 1 from STEP SHA256 5ace57df0fda9a15847270cbe66048984c366595415927b0751c0765d7b14559.
# Embedded analytic topology preserves curved surfaces and avoids a duplicate published import.
from io import BytesIO
import base64, zlib, hashlib
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Shape

_raw_brep=zlib.decompress(base64.b64decode(_encoded_brep))
assert hashlib.sha256(_raw_brep).hexdigest()=="8e370b4c1ebb51b0a0fe3e35457ddad1998467da301a0a0a599b680c3e885050"
_wrapped=TopoDS_Shape()
BRepTools.Read_s(_wrapped,BytesIO(_raw_brep),BRep_Builder())
source=Solid(_wrapped)
assert source.is_valid and len(source.solids())==1
pocket_d=param("body_magnet_pocket_diameter",7.1)
pocket_depth=param("body_magnet_pocket_depth",1.1)
magnet_y=param("body_magnet_center_offset",23.0)
# Imported geometry is fixed evidence; patch the original 7.26 x 1.26 blind pocket.
original_y=23.0
mouth=2.5
original_floor=3.76
plug=Pos(0,original_y,mouth)*Cylinder(3.68,original_floor-mouth+0.02,align=(Align.CENTER,Align.CENTER,Align.MIN))
bore=Pos(0,magnet_y,mouth-0.02)*Cylinder(pocket_d/2,pocket_depth+0.02,align=(Align.CENTER,Align.CENTER,Align.MIN))
from build123d import SkipClean
with SkipClean():
    shell=source+plug
    shell=shell-bore
assert len(shell.solids())==1 and shell.is_valid
assert 5.6-mouth-pocket_depth>=1.9
shell.color=srgb("#F5A313")
publish("body",shell,"钟壳",material="petg")
