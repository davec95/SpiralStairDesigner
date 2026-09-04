"""SpiralStairDesigner
Units: inches, converted to mm at FreeCAD API boundary.
Clockwise ascent viewed from above (left-handed helix). Counter-clockwise descent.
Pole is on the walker's RIGHT.
18 regular annular-sector treads (indices 0–17) + 1 square landing (upper floor, NOT a pie).
θ = 24.5° going (NOT 30°, NOT 24.6°, NOT 12 treads/rev).  Treads/rev = 360/24.5 ≈ 14.693878.
Total rise (finished floor to finished floor): 138.07 in.
NUM_RISES = 19 floor-to-floor including the last rise onto the platform.
h = TOTAL_RISE / 19 = 138.07/19 ≈ 7.266842 in on EVERY riser (pie-to-pie AND pie 18 → landing).
Last pie (18) walking Z = 18 × h ≈ 130.803158 in.
Landing walking Z = TOTAL_RISE = 138.07 in (designer platform / upper floor).
Last riser (pie 18 → landing) = h (EQUAL). Do NOT use leftover dump. Do NOT use 17 pies / N = 18.
Walking Z of regular tread i (i = 0..17) = (i + 1) × h
  18th tread (index 17) walking Z ≈ 130.803158
  Landing walking Z = 138.07
Pie-tread thickness = 3.0 in soffit to walking surface.
Landing plate thickness = 3.0 in (same soffit-to-surface; not 1.0).
Welded steel.  Part workbench primitives only.

IRC / walkline:
  r_inner = pole radius + 0.25 in gap = 2.25 in
  r_wl = r_inner + 12 in = 14.25 in
  L_going = 14.25 × 24.5 × π/180 ≈ 6.093 in  (PASS 6.00 IRC R311.7.9)
  L_phys  = L_going + 1.00 ≈ 7.093 in
  θ = 24.5° is authoritative from the numbered spec.

Headroom (must be ≥ 78 in):
  Helix stacking gross = (360/24.5)×h ≈ 106.78 in PASS.
  Landing 3 in plate, soffit Z = 135.07.  90° square shadow in plan.
  First wrap (CW − from +X): [−81.0°, −171.0°]
  IMPACT (under landing): steps 4–7.  Step 7 = 84.20 in PASS.
  Step 8 going starts after the wrap (not under plate).
    1  Z=  7.2668  [   0.0,  −24.5]  HR_land=127.8032
    4  Z= 29.0674  [ −73.5,  −98.0]  HR_land=106.0026  IMPACT (partial 17.0°)
    7  Z= 50.8679  [−147.0, −171.5]  HR_land= 84.2021  IMPACT (partial 24.0°)
    8  Z= 58.1347  [−171.5, −196.0]  HR_land= 76.9353  no (starts after wrap)
   8–18 not under the plate (open well).  Landing is the upper floor.

Landing geometry:
  36×36×3 square. Local (0,0) = right-front corner at the pole axis.
  Extra 65.5° clockwise about the pole after the 18th pie-wedge nose
  (90° − 24.5°; was 60° when θ was 30°, 65.4° when θ was 24.6°):
    a_lead_land = a_lead_18 − 90°
  Posts/rails on FRONT (Y=0, walker's right as they step on) and LEFT (X=36).
  RIGHT (X=0, last-pie nose) is the ARRIVAL — no posts. BACK (Y=36) is the EXIT after a 90° left.
  Skip pole (0,0). Helix still ends at the 18th shared post (0,36).
  Total pie rotation −441.0°; landing nose 90° CW past 18th.
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
NUM_RISES           = 19            # floor-to-floor including onto platform
NUM_REGULAR_TREADS  = NUM_RISES - 1 # 18 pies, indices 0–17
RISE_PER_TREAD      = TOTAL_RISE / float(NUM_RISES)  # 138.07/19 ≈ 7.266842
LAST_PIE_Z          = NUM_REGULAR_TREADS * RISE_PER_TREAD   # ≈ 130.803158
LANDING_Z           = TOTAL_RISE                            # 138.07  (upper floor)
LAST_RISER          = LANDING_Z - LAST_PIE_Z                # = h (equal)
THETA_DEG           = 24.5
TREADS_PER_REV      = 360.0 / THETA_DEG                     # ≈ 14.693878  (NOT 12)

CENTER_POLE_DIAM    = 4.0
CENTER_POLE_RADIUS  = 2.0
POLE_TO_TREAD_GAP   = 0.25          # spec 4
TREAD_INNER         = CENTER_POLE_RADIUS + POLE_TO_TREAD_GAP  # 2.25

OUTER_DIAM          = 72.0
OUTER_RADIUS        = 36.0

TREAD_THICKNESS     = 3.0           # soffit to walking surface (pies)
TREAD_OVERLAP       = 0.5           # plan nose/heel at r = 36 in
TREAD_EXTRUSION     = TREAD_THICKNESS               # 3.0 — not 1.5
LANDING_THICKNESS   = 3.0           # square plate (spec 7, same as pies)

POLE_EXTENSION      = 36.0          # above uppermost walking surface (landing)

BALUSTER_DIAM       = 0.5
BALUSTER_RADIUS     = 0.25
BALUSTERS_PER_TREAD = 5

HANDRAIL_HEIGHT     = 36.0          # above walking surface (platform / helix end)
HANDRAIL_DIAM       = 1.5
HANDRAIL_RADIUS     = 0.75

LANDING_SIZE        = 36.0          # square landing, side length
LANDING_EXTRA_CW    = math.radians(90.0 - THETA_DEG)  # 65.5°
LANDING_POST_OC     = 4.0           # on-center spacing of landing posts
LANDING_POSTS_PER_SIDE = int(LANDING_SIZE / LANDING_POST_OC) + 1   # 10
LANDING_POST_HEIGHT = HANDRAIL_HEIGHT - HANDRAIL_RADIUS   # 35.25

WALKLINE_RADIUS     = TREAD_INNER + 12.0          # 14.25 in IRC
WALKLINE_GOING      = WALKLINE_RADIUS * math.radians(THETA_DEG)  # ≈ 6.093
WALKLINE_PHYS       = WALKLINE_GOING + 1.0                       # ≈ 7.093

# ═══════════════════════════════════════════════════════════════
# Derived values
# ═══════════════════════════════════════════════════════════════

ANGLE_PER_TREAD     = math.radians(THETA_DEG)                     # 24.5°
OUTER_GOING         = OUTER_RADIUS * ANGLE_PER_TREAD              # ≈ 15.394
OUTER_ARC_LENGTH    = OUTER_GOING + 1.0                           # ≈ 16.394 plate
OVERLAP_EACH_RAD    = TREAD_OVERLAP / OUTER_RADIUS                # 0.5 / 36
TREAD_ANGULAR_SPAN  = ANGLE_PER_TREAD + 2.0 * OVERLAP_EACH_RAD    # ≈ 26.09155°

# 18th tread (index 17) leading-edge (nose), then extra 65.5° CW → 90° square
# Clockwise = negative angles from +X.
A_START_LAST        = -float(NUM_REGULAR_TREADS - 1) * ANGLE_PER_TREAD  # −17 * 24.5°
A_LEAD_LAST         = A_START_LAST - TREAD_ANGULAR_SPAN
A_LEAD_18           = A_LEAD_LAST   # last-pie nose (18 pies)
A_LEAD_LAND         = A_LEAD_LAST - math.radians(90.0)
A_RIGHT_LAND        = A_LEAD_LAST                                       # square right side = 18th nose

# Helix covers first-tread start through the 18th last post (shared with landing).
# Does NOT continue across the landing. CW = negative angles.
A_START_0           = 0.0
TOTAL_ANGLE_MAG     = abs(A_LEAD_LAST - A_START_0)                      # stop at a_lead_18
TOTAL_ANGLE         = A_LEAD_LAST - A_START_0                           # negative (CW)

CENTER_POLE_HEIGHT  = LANDING_Z + POLE_EXTENSION                        # 174.07

HANDRAIL_HELIX_RADIUS = OUTER_RADIUS
# Rise of helix = LANDING_Z so rail Z at a_lead_18 (last pie nose) equals platform rail Z (174.07)
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
# 2.  Treads (indices 0–17) with balusters
#     Walking Z = (i + 1) × h  (tread 1 at h, 18th at 18×h)
#     3 in thick: TOP at z_walk, soffit at z_walk − 3.0
#     CW: a_start = −i·θ, a_end = a_start − SPAN
# ═══════════════════════════════════════════════════════════════

tread_count    = 0
baluster_count = 0

for i in range(NUM_REGULAR_TREADS):
    a_start = -float(i) * ANGLE_PER_TREAD
    a_end   = a_start - TREAD_ANGULAR_SPAN
    z_walk  = float(i + 1) * RISE_PER_TREAD

    sector = annular_sector(TREAD_INNER, OUTER_RADIUS,
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
# 3.  Landing (upper floor after pie 18) — 36×36 square, 3 in thick
#     Right-front corner at pole. Extra 65.5° CW past the 18th pie nose.
#     Posts/rails on FRONT (Y=0, walker's right) and LEFT (X=36).
#     RIGHT (X=0) is ARRIVAL from the last pie — keep it clear. BACK (Y=36) is EXIT after 90° left.
# ═══════════════════════════════════════════════════════════════

z_land = LANDING_Z                                 # 138.07

# Box local:
#   (0,0)   right-front = pole
#   (36,0)  left-front  = outer end of leading edge (a_lead_land)
#   (0,36)  right-back  = 18th nose / shared baluster (a_lead_18)
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

# FRONT Y=0 = walker's right as they step on (keep).
# LEFT X=36 = opposite of the arrival edge (moved here so X=0 stays clear).
# Skip pole (0,0). Do NOT post the arrival radial X=0 (that blocked stepping on).
# (36,0) is created once as a FRONT post; LEFT starts at Y>0.
for k in range(LANDING_POSTS_PER_SIDE):
    t = LANDING_SIZE - float(k) * LANDING_POST_OC
    if t > 0.0:
        Part.show(make_landing_post(t, 0.0), "LandingPost_F{}".format(k))
        baluster_count += 1
        Part.show(make_landing_post(LANDING_SIZE, t), "LandingPost_L{}".format(k))
        baluster_count += 1

# L-shaped platform rails: FRONT (walker's right on entry) + LEFT (walker's right after 90° left).
# Arrival X=0 is open; exit is BACK Y=36 after the left turn.
Part.show(make_straight_rail(CENTER_POLE_RADIUS, 0.0, LANDING_SIZE, 0.0),
          "LandingRail_Front")
Part.show(make_straight_rail(LANDING_SIZE, 0.0, LANDING_SIZE, LANDING_SIZE),
          "LandingRail_Left")

# ═══════════════════════════════════════════════════════════════
# 4.  Spiral handrail  (left-handed helix = CW ascent, stops at 18th last post)
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
