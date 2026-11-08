# Allsun - current launcher

The newest Allsun app is in [`Allsun-update-launcher`](Allsun-update-launcher/). Open that folder in VS Code and follow its [run instructions](Allsun-update-launcher/README.md). Run `python3 launcher.py` (macOS/Linux) or `py -3 launcher.py` (Windows), then launch v20 from the local library. Python 3.9+ is required, with no packages to install.

v20 adds the custom sun identity. v19 adds a scripted drone failure, heartbeat detection and survey-route takeover by the second drone. Earlier builds remain selectable in the library. This is a local prototype, not measured radio/hardware behavior. The brief asks for coordination through dropped connections; the particular survey-takeover sequence is our design choice.

The old `SiteLink-update-launcher` folder has been renamed to `Allsun-update-launcher`; its historical versions remain in `builds/` and earlier commits. The repository-root `index.html`, data and tests below remain the earlier teammate prototype, unchanged. The notes below describe that earlier root app, not v20.

---

# SiteLink offline prototype

A single-file site-manager demo for the MIT Energy & Climate Hack Exowatt challenge. All machines, sensors, connections and command responses are simulated on one device. This is an unofficial hackathon project, not affiliated with Exowatt.

## Run

Download `index.html` and open the saved file in Safari, Chrome or Firefox. No build, package installation, server or network connection is needed. Open it in a full browser rather than an attachment preview. The font is embedded; its SIL Open Font License is included in the HTML.

## Site dimensions

Open **Site dimensions** below the map's scene tabs. Set east-west width and north-south height in metres and choose **Apply size**.

- Default: 800 x 500 m. Supported range: 200-5,000 m per side, in 10 m steps.
- This rescales the illustrative layout, positions, routes, charging point and camera views. It does not add equipment or simulate a real site's capacity.
- Coordinates, grid spacing and the scale bar reflect the new physical dimensions. Speeds remain in m/s, so larger routes take longer to travel.
- Existing connection state, queued commands and stale reports are retained. Resizing a stale position is a local scenario edit, not a new robot update.
- Settings are for this open session only. Reloading restores the default scenario.

## Controls

Select a robot, drone or crew member in the map or fleet. Robots and drones accept task assignment, hold, resume, return-to-charge and decision-level commands. Crew are read-only coordination markers.

Scene tabs move the camera across the same illustrative site. Pause and speed controls affect the simulation. Drop a selected link to demonstrate a stale last-known position, then reconnect to resume updates and send pending commands.

Commands progress through QUEUED, SENT, ACKNOWLEDGED and EXECUTING. An offline command has no effect until reconnection. One pending command per machine is supported; a later Hold cannot bypass it.

## Decision levels and limits

- Manual: selecting this level holds the machine until a command. A task assignment or Resume starts its scripted route. This is task-level control, not joystick control; routes loop rather than stopping at task completion.
- Supervised: follows its assigned route without selecting new tasks.
- Autonomous: cycles preset task labels on a timer. It is not an AI planner, and its own task changes do not change the route. Manager-issued assignments do change routes. A level-3 timer can later relabel a manager task, even while held.

The demo does not implement logins, operator roles, competing-manager arbitration, real robot control, real sensor input, collision avoidance, safety interlocks, emergency-stop behavior or cross-device communication. Hold all is an ordinary command, not an emergency stop. Offline machines keep their existing simulated behavior; the console freezes the last received state.

## Version

V10 adds adjustable physical site dimensions to the v9 design. The dark/orange/white workbench, detached glass-like fleet, task-button treatment and scene transitions are retained.

## 3D splat / intermittent mesh experiment

Branch: `feat/3d-splat-mesh`. Open `index.html` as before; the new panel is below
its original map. No dependencies, CDN, network calls or build step were added.

1. Watch the 3D robots follow the existing routes. Drag the 3D view to orbit,
   scroll to zoom, and select a machine in the original fleet list.
2. Use **Download sample**, then **Import .splat**, or import the included
   `data/exowatt-site.splat` (490 synthetic Gaussians, 15,680 bytes).
3. Increase band radius to 280 m for an immediate connected demonstration.
   Cut HQ uplink: machines keep moving, discovering and exchanging tiles while
   HQ's inventory stops growing. Restore it to drain buffered tiles from robots
   in HQ range. Lower radius to demonstrate isolated components and later encounters.
4. Enable **Selected unit's map only** to see the tiles that machine knows.
   The default view shows simulation ground truth, including disconnected units;
   the original console still shows last-known telemetry when its link is dropped.

### Representation and protocol

The importer supports the common 32-byte binary `.splat` layout: little-endian
float32 XYZ (12 bytes), positive float32 axis scales (12), uint8 RGBA (4), then
uint8 quaternion WXYZ (4), decoded as `(byte - 128) / 128` and normalized.
It rejects empty, incomplete, non-finite, non-positive-scale, zero-quaternion and
oversized input. Maximum: 20,000 splats / 640 KB. PLY and compressed splat formats
are not supported. A failed import retains the previous scene. Coordinates must
already be in the site's shared local metre frame (X east, Y north, Z up).
The renderer projects quaternion-rotated Gaussian covariance onto an orbitable
orthographic Canvas 2D view, sorts by depth, and alpha-blends soft ellipses. This
is a small CPU visualization, not a photorealistic GPU 3DGS renderer.

Splats are partitioned into immutable 80 m XY tiles. Every four simulated seconds,
a robot observes tiles with centroids within 95 m. Initial inventories include at
most one nearby tile. Robots retain all observed/received tiles for this session.
Each second, overlapping bands exchange at most one missing tile per direction,
using inventories from the start of the round to enforce relay delay. Duplicate
tiles are suppressed by tile ID. HQ receives at most one missing tile per in-range
robot per second while uplink is enabled. Byte totals count 32-byte Gaussian payloads
per successful delivery, including relay copies; they exclude protocol overhead.

The rings are a deliberately idealized connectivity model: peer links exist at
separation ≤ twice the selected radius; HQ's range is one radius. These are
illustrative bands, not calibrated antenna coverage. Map transfers and acknowledgments
are simulated inventory updates; there is no actual radio, socket transport, packet
loss, authentication, SLAM alignment, map revision conflict resolution, obstacle
attenuation, disk persistence or restart recovery. Existing mission/autonomy behavior
is unchanged. Importing a map resets inventories; resizing the original site moves
robots but does not rescale imported metric geometry.

### Research basis

The supplied reading notes motivate geometry sharing, intermittent encounters and
store-carry-forward reporting, particularly **ACHORD: Communication-Aware Multi-Robot
Coordination With Intermittent Connectivity** (2022),
https://ai.jpl.nasa.gov/public/documents/papers/saboia-et-al-rss2022.pdf.
The notes also cite **What is the best 3D scene representation for robotics?**,
**GSRF**, **RadCloudSplat**, and **PropEM-L**. These are design inspirations supplied
by the team, not independently reproduced or validated results. RF Gaussian models
predict/synthesize radio fields; they do not themselves provide a map-transfer
protocol. This demo implements neither their RF models nor their reported accuracy.
A next implementation could replace the range predicate with measured link quality,
and put versioned tile manifests, chunk checksums and resumable acknowledgments over
a real local transport.

### Validation

Run `node --test tests/splat.test.cjs` (Node 18+). Tests exercise hop latency,
duplicate suppression, range boundaries, offline retention, HQ recovery, and binary
validation. Browser smoke checks use the installed Playwright and Chromium against
a local HTTP server; no server is required for normal saved-file use.
