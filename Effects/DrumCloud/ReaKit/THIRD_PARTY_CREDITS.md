# Third-Party Credits

ReaKit stands on the shoulders of the REAPER JSFX community. The components
below derive from other authors' work and are included and redistributed here
**with their authors' permission**, alongside EON Studios' original code
(MIT — see LICENSE). Huge thanks to all of them.

Permission records are kept on file by EON Studios.

DrumCloud v0.27.1 vendors the two ReaKit libraries it imports, pinned exactly
to ReaKit 1.3.0 at upstream commit
`04996cc3f86a2b7098e50fc7cfdf0ae561e69ee4`. The files provide the Serum-style
and Encoder knobs plus pill and segmented selectors used by DrumCloud. Both
include files are standalone and have no transitive imports; together they are
the complete runtime dependency closure for DrumCloud's GUI.

---

## VU meters (`vu_kbsg.jsfx-inc`, parts of `meters_kbsg.jsfx-inc`)

- **ZenoMOD VU Meter v1.7.7** — by ZenoMOD (with credits to chris-s, aurelien,
  Lubomir I. Ivanov). Spring-mass needle physics and the themed vector faces.
- **Liteon VU Meter** — by Lubomir I. Ivanov (c) 2008-2009. RMS ballistics and
  the retro vector face.
- **Tukan Studios** — tk-vu_lib_d (demian d mod). Spring-mass physics and face
  drawing approach.

## Knob styles (`knobs_kbsg.jsfx-inc`)

- **BirdBird** — the VIC rainbow-arc knob (style 9).
- **Joanny / MacFizz** — the blue pot knob (style 6).
- **Spice Pro** — the blue arc-fill knob (style 10).
- **Witti Sound** — the clean arc + dot knob (style 4).

## Button styles (`buttons_kbsg.jsfx-inc`)

- **Joanny** — the green checkbox style.
- **Spice** — the segmented-bar selector style.

---

All remaining widgets — including the hardware-inspired knob styles (SSL, Neve,
API, Pultec, Vari-Mu, MPC, Ableton, Pro Tools, FabFilter, Serum, Roland,
encoders, jog wheels and both 2026 additions), the full slider/fader library,
the remaining buttons, and the meters DSP/drawing outside the VU — are original
EON Studios code, drawn from hardware reference photos, not from other plugins'
source.
