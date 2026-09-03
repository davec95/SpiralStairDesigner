"""SpiralStairDesigner
Units: inches, converted to mm at FreeCAD API boundary.
Clockwise ascent viewed from above (left-handed helix). Counter-clockwise descent.
Pole is on the walker's RIGHT.
17 regular annular-sector treads (indices 0–16) + 1 square landing (upper floor, NOT a pie).
θ = 24.6° going (NOT 30°, NOT 24.5°, NOT 12 treads/rev).  Treads/rev = 360/24.6 ≈ 14.634146.
Total rise (finished floor to finished floor): 138.07 in.
NUM_RISES = 18 floor-to-floor including the last rise onto the platform.
h = TOTAL_RISE / 18 = 138.07/18 ≈ 7.670556 in on EVERY riser (pie-to-pie AND pie 17 → landing).
Last pie (17) walking Z = 17 × h ≈ 130.399444 in.
Landing walking Z = TOTAL_RISE = 138.07 in (designer platform / upper floor).
Last riser (pie 17 → landing) = h (EQUAL). Do NOT use leftover dump. Do NOT use 18 pies / N = 19.
Walking Z of regular tread i (i = 0..16) = (i + 1) × h
  17th tread (index 16) walking Z ≈ 130.399444
  Landing walking Z = 138.07
Pie-tread thickness = 3.0 in soffit to walking surface.
Landing plate thickness = 3.0 in (same soffit-to-surface; not 1.0).
Welded steel.  Part workbench primitives only.

IRC / walkline (comments only; construction radii stay 2 in inner / 36 in outer):
  r_wl = pole EDGE + 12 in = 14 in  (NOT 6 in)
  L_going = 14 × 24.6 × π/180 ≈ 6.011 in  (PASS 6.00 IRC R311.7.9)
  L_phys  = L_going + 1.00 ≈ 7.011 in
  θ = 24.6° is authoritative from the numbered spec.

Headroom (must be ≥ 78 in):
  Helix stacking gross = (360/24.6)×h ≈ 112.25 in PASS.
  Landing 3 in plate, soffit Z = 135.07.  90° square shadow in plan.
  First wrap (CW − from +X): [−58.2°, −148.2°]
  IMPACT (under landing): steps 3–7.  Step 7 = 81.38 in PASS.
  Step 8 going starts after the wrap (not under plate).
    1  Z=  7.6706  [   0.0,  −24.6]  HR_land=127.3994
    2  Z= 15.3411  [ −24.6,  −49.2]  HR_land=119.7289
    3  Z= 23.0117  [ −49.2,  −73.8]  HR_land=112.0583  IMPACT (partial 15.6°)
    4  Z= 30.6822  [ −73.8,  −98.4]  HR_land=104.3878  IMPACT
    5  Z= 38.3528  [ −98.4, −123.0]  HR_land= 96.7172  IMPACT
    6  Z= 46.0233  [−123.0, −147.6]  HR_land= 89.0467  IMPACT
    7  Z= 53.6939  [−147.6, −172.2]  HR_land= 81.3761  IMPACT (0.6° of wrap)
    8  Z= 61.3644  [−172.2, −196.8]  HR_land= 73.7056  no (starts after wrap)
   9–17 not under the plate (open well).  Landing is the upper floor.

Landing geometry:
  36×36×3 square. Local (0,0) = right-front corner at the pole axis.
  Extra 65.4° clockwise about the pole after the 17th pie-wedge nose
  (90° − 24.6°; was 60° when θ was 30°, 65.5° when θ was 24.5°):
    a_lead_land = a_lead_17 − 90°
  Posts/rails on RIGHT (X=0, pole radial) and FRONT (Y=0, leading edge).
  LEFT (X=36) is the EXIT. BACK (Y=36) stays open (arrival).
  Full 36 in guarded edges at 4 in OC. Skip pole (0,0) and 17th shared post (0,36).
  Platform rails: L on right+front. Helix stops at a_lead_17.
  Total pie rotation −418.2°; landing nose 90° CW past 17th.
"""

import math
import FreeCAD
import Part
from FreeCAD import Base

doc = FreeCAD.ActiveDocument
if doc is None:
    doc = FreeCAD.newDocument("SpiralStairDesigner")

INCH = 25.4

# ═══════════════════════════════════════════════════════════════
# Constants  (all in inches unless noted)
# ═══════════════════════════════════════════════════════════════

TOTAL_RISE          = 138.07        # finished floor to finished floor
NUM_RISES           = 18            # floor-to-floor including onto platform
NUM_REGULAR_TREADS  = NUM_RISES - 1 # 17 pies, indices 0–16
RISE_PER_TREAD      = TOTAL_RISE / float(NUM_RISES)  # 138.07/18 ≈ 7.670556
LAST_PIE_Z          = NUM_REGULAR_TREADS * RISE_PER_TREAD   # ≈ 130.399444
LANDING_Z           = TOTAL_RISE                            # 138.07  (upper floor)
LAST_RISER          = LANDING_Z - LAST_PIE_Z                # = h (equal)
THETA_DEG           = 24.6
TREADS_PER_REV      = 360.0 / THETA_DEG                     # ≈ 14.634146  (NOT 12)

CENTER_POLE_DIAM    = 4.0
CENTER_POLE_RADIUS  = 2.0

OUTER_DIAM          = 72.0
OUTER_RADIUS        = 36.0

TREAD_THICKNESS     = 3.0           # soffit to walking surface (pies)
TREAD_OVERLAP       = 0.5           # plan nose/heel at r = 36 in
TREAD_EXTRUSION     = TREAD_THICKNESS               # 3.0 — not 1.5
LANDING_THICKNESS   = 3.0           # square plate (spec 6, same as pies)

POLE_EXTENSION      = 36.0          # above uppermost walking surface (landing)

BALUSTER_DIAM       = 0.5
BALUSTER_RADIUS     = 0.25
BALUSTERS_PER_TREAD = 5

HANDRAIL_HEIGHT     = 36.0          # above walking surface (platform / helix end)
HANDRAIL_DIAM       = 1.5
HANDRAIL_RADIUS     = 0.75

LANDING_SIZE        = 36.0          # square landing, side length
LANDING_EXTRA_CW    = math.radians(90.0 - THETA_DEG)  # 65.4°
LANDING_POST_OC     = 4.0           # on-center spacing of landing posts
LANDING_POSTS_PER_SIDE = int(LANDING_SIZE / LANDING_POST_OC) + 1   # 10
LANDING_POST_HEIGHT = HANDRAIL_HEIGHT - HANDRAIL_RADIUS   # 35.25

WALKLINE_RADIUS     = CENTER_POLE_RADIUS + 12.0   # 14 in IRC
WALKLINE_GOING      = WALKLINE_RADIUS * math.radians(THETA_DEG)  # ≈ 6.011
WALKLINE_PHYS       = WALKLINE_GOING + 1.0                       # ≈ 7.011

# ═══════════════════════════════════════════════════════════════
# Derived values
# ═══════════════════════════════════════════════════════════════

ANGLE_PER_TREAD     = math.radians(THETA_DEG)                     # 24.6°
OUTER_GOING         = OUTER_RADIUS * ANGLE_PER_TREAD              # ≈ 15.457
OUTER_ARC_LENGTH    = OUTER_GOING + 1.0                           # ≈ 16.457 plate
OVERLAP_EACH_RAD    = TREAD_OVERLAP / OUTER_RADIUS                # 0.5 / 36
TREAD_ANGULAR_SPAN  = ANGLE_PER_TREAD + 2.0 * OVERLAP_EACH_RAD    # ≈ 26.19155°

# 17th tread (index 16) leading-edge (nose), then extra 65.4° CW → 90° square
# Clockwise = negative angles from +X.
A_START_LAST        = -float(NUM_REGULAR_TREADS - 1) * ANGLE_PER_TREAD  # −16 * 24.6°
A_LEAD_LAST         = A_START_LAST - TREAD_ANGULAR_SPAN
A_LEAD_18           = A_LEAD_LAST   # alias kept for landing VERIFY prints
A_LEAD_LAND         = A_LEAD_LAST - math.radians(90.0)
A_RIGHT_LAND        = A_LEAD_LAST                                       # square right side = 17th nose

# Helix covers first-tread start through the 17th last post (shared with landing).
# Does NOT continue across the landing. CW = negative angles.
A_START_0           = 0.0
TOTAL_ANGLE_MAG     = abs(A_LEAD_LAST - A_START_0)                      # stop at a_lead_17
TOTAL_ANGLE         = A_LEAD_LAST - A_START_0                           # negative (CW)

CENTER_POLE_HEIGHT  = LANDING_Z + POLE_EXTENSION                        # 174.07

HANDRAIL_HELIX_RADIUS = OUTER_RADIUS
# Rise of helix = LANDING_Z so rail Z at a_lead_18 equals platform rail Z (174.07)
HANDRAIL_HELIX_HEIGHT = LANDING_Z
HANDRAIL_HELIX_PITCH  = HANDRAIL_HELIX_HEIGHT / (TOTAL_ANGLE_MAG / (2.0 * math.pi))
HANDRAIL_START_Z      = HANDRAIL_HEIGHT
PLATFORM_RAIL_Z       = LANDING_Z + HANDRAIL_HEIGHT   # 174.07

# ═══════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════

def inch(val):
    return val * INCH


def handrail_z(angle_rad):
    """Helical handrail centreline Z (inches) at a given CW-negative angle."""
    frac = abs(angle_rad / TOTAL_ANGLE)
    return HANDRAIL_START_Z + frac * HANDRAIL_HELIX_HEIGHT


def land_xy(lx, ly):
    """Box-local (inches) → global XY (inches). Standard rotate(Z, A_LEAD_LAND); no Y-mirror."""
    c = math.cos(A_LEAD_LAND)
    s = math.sin(A_LEAD_LAND)
    return lx * c - ly * s, lx * s + ly * c


def annular_sector(inner_r, outer_r, a_start, a_end, thickness):
    """Annular-sector solid (all dims in inches). CW: a_end < a_start (negative)."""
    ir = inch(inner_r)
    o_r = inch(outer_r)
    th = inch(thickness)

    a1 = min(a_start, a_end)
    a2 = max(a_start, a_end)
    a1d = math.degrees(a1)
    a2d = math.degrees(a2)

    origin  = Base.Vector(0, 0, 0)
    z_axis  = Base.Vector(0, 0, 1)

    outer_arc = Part.makeCircle(o_r, origin, z_axis, a1d, a2d)
    inner_arc = Part.makeCircle(ir, origin, z_axis, a2d, a1d)

    cos1, sin1 = math.cos(a_start), math.sin(a_start)
    cos2, sin2 = math.cos(a_end),   math.sin(a_end)
    ro1 = Base.Vector(o_r * cos1, o_r * sin1, 0)
    ri1 = Base.Vector(ir * cos1, ir * sin1, 0)
    ro2 = Base.Vector(o_r * cos2, o_r * sin2, 0)
    ri2 = Base.Vector(ir * cos2, ir * sin2, 0)

    wire = Part.Wire([outer_arc, Part.makeLine(ro2, ri2),
                      inner_arc, Part.makeLine(ri1, ro1)])
    return Part.Face(wire).extrude(Base.Vector(0, 0, th))


def make_baluster(angle, z_base):
    """Spiral baluster at outer-radius position for a given angle and base Z (inches)."""
    z_rail = handrail_z(angle)
    h = z_rail - z_base - HANDRAIL_RADIUS
    if h <= 0.0:
        h = 0.1
    x = inch(OUTER_RADIUS * math.cos(angle))
    y = inch(OUTER_RADIUS * math.sin(angle))
    z = inch(z_base)
    return Part.makeCylinder(inch(BALUSTER_RADIUS), inch(h),
                             Base.Vector(x, y, z), Base.Vector(0, 0, 1)), h


def make_landing_post(lx, ly):
    """Level landing post at box-local (lx, ly) inches. Height meets platform rail underside."""
    gx, gy = land_xy(lx, ly)
    return Part.makeCylinder(inch(BALUSTER_RADIUS), inch(LANDING_POST_HEIGHT),
                             Base.Vector(inch(gx), inch(gy), inch(LANDING_Z)),
                             Base.Vector(0, 0, 1))


def make_straight_rail(lx0, ly0, lx1, ly1):
    """Horizontal 1.5 in tube between two box-local points at PLATFORM_RAIL_Z."""
    x0, y0 = land_xy(lx0, ly0)
    x1, y1 = land_xy(lx1, ly1)
    dx = inch(x1 - x0)
    dy = inch(y1 - y0)
    seg_len = math.sqrt(dx * dx + dy * dy)
    return Part.makeCylinder(
        inch(HANDRAIL_RADIUS), seg_len,
        Base.Vector(inch(x0), inch(y0), inch(PLATFORM_RAIL_Z)),
        Base.Vector(dx / seg_len, dy / seg_len, 0.0),
    )


def baluster_index(tread_i, local_j):
    return tread_i * (BALUSTERS_PER_TREAD - 1) + local_j


# ═══════════════════════════════════════════════════════════════
# 1.  Centre pole
# ═══════════════════════════════════════════════════════════════

pole = Part.makeCylinder(inch(CENTER_POLE_RADIUS), inch(CENTER_POLE_HEIGHT),
                         Base.Vector(0, 0, 0), Base.Vector(0, 0, 1))
Part.show(pole, "CenterPole")

# ═══════════════════════════════════════════════════════════════
# 2.  Treads (indices 0–16) with balusters
#     Walking Z = (i + 1) × h  (tread 1 at h, 17th at 17×h)
#     3 in thick: TOP at z_walk, soffit at z_walk − 3.0
#     CW: a_start = −i·θ, a_end = a_start − SPAN
# ═══════════════════════════════════════════════════════════════

tread_count    = 0
baluster_count = 0

for i in range(NUM_REGULAR_TREADS):
    a_start = -float(i) * ANGLE_PER_TREAD
    a_end   = a_start - TREAD_ANGULAR_SPAN
    z_walk  = float(i + 1) * RISE_PER_TREAD

    sector = annular_sector(CENTER_POLE_RADIUS, OUTER_RADIUS,
                            a_start, a_end, TREAD_EXTRUSION)
    sector.translate(Base.Vector(0, 0, inch(z_walk - TREAD_THICKNESS)))
    Part.show(sector, "Tread_{}".format(i + 1))
    tread_count += 1

    for j in range(BALUSTERS_PER_TREAD):
        if i > 0 and j == 0:
            continue          # shared with previous tread's last baluster
        ba = a_start + float(j) * (a_end - a_start) / float(BALUSTERS_PER_TREAD - 1)
        cyl, _h = make_baluster(ba, z_walk)
        Part.show(cyl, "Baluster_{}".format(baluster_index(i, j)))
        baluster_count += 1

# ═══════════════════════════════════════════════════════════════
# 3.  Landing (upper floor after pie 17) — 36×36 square, 3 in thick
#     Right-front corner at pole. Extra 65.4° CW past the 17th pie nose.
#     Posts/rails on RIGHT (X=0) and FRONT (Y=0). LEFT is the exit.
# ═══════════════════════════════════════════════════════════════

z_land = LANDING_Z                                 # 138.07

# Box local:
#   (0,0)   right-front = pole
#   (36,0)  left-front  = outer end of leading edge (a_lead_land)
#   (0,36)  right-back  = 17th nose / shared baluster (a_lead_17)
#   (36,36) left-back
# Standard rotate by a_lead_land (NO Y-mirror, no extra ±90°, no XY translation).
# Translate so TOP face is at z_walk (box height = 3 in).
box = Part.makeBox(inch(LANDING_SIZE), inch(LANDING_SIZE), inch(LANDING_THICKNESS))
box.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), math.degrees(A_LEAD_LAND))
box.translate(Base.Vector(0, 0, inch(z_land - LANDING_THICKNESS)))

# Pole occupies the right-front corner; cut it out so the plate meets the pole wall.
pole_cut = Part.makeCylinder(inch(CENTER_POLE_RADIUS), inch(LANDING_THICKNESS + 2.0),
                             Base.Vector(0, 0, inch(z_land - LANDING_THICKNESS - 1.0)),
                             Base.Vector(0, 0, 1))
try:
    box = box.cut(pole_cut)
except Exception:
    pass

Part.show(box, "Landing")
tread_count += 1

# VERIFY landing corners (inches)
v00x, v00y = land_xy(0.0, 0.0)
v36x, v36y = land_xy(LANDING_SIZE, 0.0)
v03x, v03y = land_xy(0.0, LANDING_SIZE)
print("VERIFY local(0,0)   -> ({:.4f}, {:.4f}, {:.2f})".format(v00x, v00y, z_land))
print("VERIFY local(36,0)  -> ({:.4f}, {:.4f}, {:.2f})".format(v36x, v36y, z_land))
print("VERIFY local(0,36)  -> ({:.4f}, {:.4f}, {:.2f})  a_lead_18={:.4f} deg".format(
    v03x, v03y, z_land, math.degrees(A_LEAD_18)))
print("VERIFY expected (36,0) = ({:.4f}, {:.4f})".format(
    OUTER_RADIUS * math.cos(A_LEAD_LAND), OUTER_RADIUS * math.sin(A_LEAD_LAND)))
print("VERIFY expected (0,36) = ({:.4f}, {:.4f})".format(
    OUTER_RADIUS * math.cos(A_LEAD_18), OUTER_RADIUS * math.sin(A_LEAD_18)))

# Guarded edges at 4 in OC. RIGHT X=0 and FRONT Y=0.
# Skip pole (0,0) and 17th shared post (0,36). LEFT and BACK stay open.
for k in range(LANDING_POSTS_PER_SIDE):
    t = LANDING_SIZE - float(k) * LANDING_POST_OC
    if t > 0.0:
        Part.show(make_landing_post(t, 0.0), "LandingPost_F{}".format(k))
        baluster_count += 1
        if t < LANDING_SIZE:
            Part.show(make_landing_post(0.0, t), "LandingPost_R{}".format(k))
            baluster_count += 1

# L-shaped platform rails: FRONT (leading edge) + RIGHT (pole radial). LEFT = exit.
Part.show(make_straight_rail(CENTER_POLE_RADIUS, 0.0, LANDING_SIZE, 0.0),
          "LandingRail_Front")
Part.show(make_straight_rail(0.0, CENTER_POLE_RADIUS, 0.0, LANDING_SIZE),
          "LandingRail_Right")

# ═══════════════════════════════════════════════════════════════
# 4.  Spiral handrail  (left-handed helix = CW ascent, stops at 17th last post)
#     makeHelix(pitch, height, radius, apex_deg=0, left_handed=True)
# ═══════════════════════════════════════════════════════════════

helix = Part.makeHelix(
    inch(HANDRAIL_HELIX_PITCH),
    inch(HANDRAIL_HELIX_HEIGHT),
    inch(HANDRAIL_HELIX_RADIUS),
    0,
    True,
)
helix.translate(Base.Vector(0, 0, inch(HANDRAIL_START_Z)))
helix_wire = Part.Wire(helix.Edges)

profile_center = Base.Vector(inch(HANDRAIL_HELIX_RADIUS), 0, inch(HANDRAIL_START_Z))
profile = Part.makeCircle(inch(HANDRAIL_RADIUS), profile_center, Base.Vector(0, 0, 1))

try:
    pipe = helix_wire.makePipeShell([profile], True, False, 2)
    Part.show(pipe, "Handrail")
    print("Handrail swept via makePipeShell.")
except Exception as exc:
    print("makePipeShell failed ({}) — falling back to fused cylinders.".format(exc))
    n_seg = 300
    compound = None
    for k in range(n_seg):
        f0 = float(k) / float(n_seg)
        f1 = float(k + 1) / float(n_seg)
        a0 = f0 * TOTAL_ANGLE
        a1 = f1 * TOTAL_ANGLE
        z0 = inch(handrail_z(a0))
        z1 = inch(handrail_z(a1))
        x0 = inch(HANDRAIL_HELIX_RADIUS * math.cos(a0))
        y0 = inch(HANDRAIL_HELIX_RADIUS * math.sin(a0))
        x1 = inch(HANDRAIL_HELIX_RADIUS * math.cos(a1))
        y1 = inch(HANDRAIL_HELIX_RADIUS * math.sin(a1))
        dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
        seg_len = math.sqrt(dx * dx + dy * dy + dz * dz)
        if seg_len < 1e-6:
            continue
        cyl = Part.makeCylinder(inch(HANDRAIL_RADIUS), seg_len,
                                Base.Vector(x0, y0, z0),
                                Base.Vector(dx / seg_len, dy / seg_len, dz / seg_len))
        compound = cyl if compound is None else compound.fuse(cyl)
    if compound is not None:
        Part.show(compound, "Handrail")
        print("Handrail built via fused cylinders.")
    else:
        print("ERROR: handrail fallback produced no geometry.")

# ═══════════════════════════════════════════════════════════════
# 5.  Final recompute
# ═══════════════════════════════════════════════════════════════

doc.recompute()
print("Done.  Treads={}  Balusters={}  FTF={}  h={:.6f}  LastPieZ={:.6f}  LandingZ={}  Pole={} in  theta={} deg  a_lead_land={:.2f} deg  railZ={}".format(
    tread_count, baluster_count, TOTAL_RISE, RISE_PER_TREAD, LAST_PIE_Z, LANDING_Z, CENTER_POLE_HEIGHT, THETA_DEG,
    math.degrees(A_LEAD_LAND), PLATFORM_RAIL_Z))
print("Walkline r={} in  L_going={:.3f} in  L_phys={:.3f} in  outer_plate={:.3f} in  tread_th={}  land_th={}  last_riser={:.6f}  equal={}  CW".format(
    WALKLINE_RADIUS, WALKLINE_GOING, WALKLINE_PHYS, OUTER_ARC_LENGTH, TREAD_THICKNESS, LANDING_THICKNESS, LAST_RISER, abs(LAST_RISER - RISE_PER_TREAD) < 1e-9))
