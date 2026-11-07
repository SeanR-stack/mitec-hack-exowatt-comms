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
