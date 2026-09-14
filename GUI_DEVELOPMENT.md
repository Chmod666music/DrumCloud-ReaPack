# DrumCloud v0.27-dev GUI prototype

This branch keeps v0.26 frozen as the audio/preset compatibility baseline. The
prototype changes JSFX metadata and `@gfx` only, plus six persistent GUI-memory
blocks in unused addresses 512–607. It does not change `@block` or `@sample`.

## ReaKit dependency

Install **ReaKit** with ReaPack before loading this development version. The
JSFX imports the installed library directly:

```eel
import ReaKit/Library/knobs_kbsg.jsfx-inc
```

The prototype was developed against ReaKit 1.3.0. In REAPER, use
**Extensions → ReaPack → Browse packages**, find ReaKit, install it, then reopen
or rescan the DrumCloud JSFX. Do not copy the library into this repository.

ReaKit's supported `rk_knob_draw` API accepts accent RGB values (`cr`, `cg`,
`cb`). Serum style 17 applies them to its active arc and pointer. Encoder style
11 applies them to its LED field/ring; in ReaKit 1.3.0 its pointer is fixed
white inside the library. DrumCloud deliberately does not redraw that pointer
using a duplicate of ReaKit's internal geometry. If ReaKit exposes a pointer
color later, pass the same gold accent through that API.

## First functional section

The **GRAIN** panel binds existing parameters without renumbering them:

| Control | Existing slider | ReaKit style | Default |
|---|---:|---|---:|
| Grain Size | 3 | Serum (large) | 180 ms |
| Density | 5 | Serum (large) | 8 Hz |
| Position Spread | 6 | Encoder (small) | 10% |
| Stereo Spread | 9 | Encoder (small) | 50% |
| Attack | 15 | Encoder (small) | 10 ms |
| Release | 16 | Encoder (small) | 80 ms |

Writes use `slider_automate(sliderN)`. ReaKit supplies vertical drag, Ctrl fine
drag, Shift extra-fine drag, wheel adjustment and double-click/right-click
reset through its public dispatcher. The replaced native sliders use
JSFX's leading `-` label marker, so REAPER does not draw duplicate controls.
Their numbers, variables, defaults, ranges and steps remain unchanged for
presets, saved state and automation. Native sliders without a working custom
equivalent remain visible.

The second functional panel adds Position (slider 4), Scan Speed (7), Scan
toggle (8), the five Position Modes (11), Sample Start (12) and Sample End
(13). Position and Scan Speed use Serum controls, Start/End use compact Encoder
controls, and Scan/Position Mode use ReaKit's pill and segmented-button APIs.
Start and End may cross, matching the native sliders; the engine consistently
uses the lower value as range start and the higher value as range end. Their
larger hit radius and immediate GUI-side range normalization keep the knobs,
values and waveform boundary markers synchronized while dragging. PITCH, SPACE
and DELAY remain reserved and inert.

The fourth functional panel adds Reverb Mode (slider 17), Mix (18), Size (19),
Decay (20), Damping (21), and Shimmer Amount (22). Mode uses a four-way ReaKit
selector; Mix/Size use Serum controls and the helper parameters use Encoders.
The controls are always available while their audible effect continues to
follow the existing engine mode.

The fifth functional panel adds Delay Mode (slider 23), Time L/R (24–25),
Feedback (26), Mix (27), and Damping (28). Mode uses a three-way ReaKit
selector, Time L/R use Serum controls, and Feedback/Mix/Damping use Encoders.
This completes the planned GRAIN, MOTION, PITCH, SPACE, and DELAY skeleton.

The final Source/Output strip adds Output (slider 10), Grain Playback Direction
(30), Density Spread (31), and a readout of the Sample file slider (1). ReaKit
does not expose a file-dropdown widget, and JSFX does not expose enumeration of
a file slider's scanned list to `@gfx`. The native Sample selector therefore
remains visible and is the source of truth for loading, presets and saved state.
The other 33 native sliders are hidden only after receiving functional custom
equivalents; their declarations and compatibility surface remain intact.

The third functional panel adds Root Note (slider 2), Pitch Spread (14), Auto
Root (29), Detect Root (32), Fine Tune (33), and Apply Detected Tuning (34).
Root Note is stepped to integer MIDI notes; Fine Tune remains continuous at its
original 0.1-cent slider resolution. Detect and Apply retain the engine's
existing momentary command behavior and return to Idle after processing. SPACE
and DELAY remain reserved and inert.

The original custom waveform reads the same sample/grain state and retains
click/drag positioning through slider 4.

## Manual checks in REAPER

1. Confirm the effect compiles with ReaKit installed and reports
   `v0.27-dev / REAKIT GUI PROTOTYPE`.
2. Load an existing v0.26 preset and compare its sound and all 34 parameter
   values with v0.26.
3. Drag, Ctrl-drag, Shift-drag, wheel and double-click each GRAIN control while
   watching the corresponding parameter/automation lane.
4. Write and replay automation for sliders 3, 5, 6, 9, 15 and 16.
5. Drag inside the waveform and confirm Position (slider 4) still follows.
6. Resize and embed the FX window; confirm the 1180×980 design scales and the
   waveform/grain markers remain aligned.
7. Temporarily remove/rename the ReaKit install and confirm the resulting import
   error makes the missing dependency obvious; restore it before further tests.

Do not generate `index.xml`, tag, or publish this branch as stable.

## Beta cleanup checkpoint

After the functional and resize tests passed in REAPER, the disabled copy of
the v0.26 diagnostic `@gfx` code was removed from this development branch. Its
history remains recoverable from Git checkpoint `61ef213`; no audio, slider or
preset code was removed. Custom automation now uses explicit parameter bitmasks
and closes touch gestures on drag release, wheel changes and reset. The user
confirmed Last Touched behavior after this change.
