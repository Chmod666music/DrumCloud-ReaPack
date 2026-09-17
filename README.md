# DrumCloud JS v0.27.1

DrumCloud JS is a granular sample instrument for REAPER.

v0.27.1 keeps the complete dark-and-gold ReaKit interface while preserving the
v0.26 audio engine, slider numbering, presets, saved states and automation.
The required ReaKit GUI controls are now bundled with DrumCloud, so there is no
separate ReaKit dependency to install. GRAIN, MOTION, PITCH, SPACE, DELAY and
SOURCE/OUTPUT panels plus REAPER Last Touched support are unchanged.
See [validation notes](VALIDATION.md) for test coverage and limitations.

This repository is a ReaPack repository. Installing the package installs the
JSFX instrument, its CC0 factory samples, and a 46-preset factory bank.

## Install with ReaPack

1. Open **Extensions → ReaPack → Import repositories** in REAPER.
2. Paste this URL:

   `https://raw.githubusercontent.com/Chmod666music/DrumCloud-ReaPack/main/index.xml`

3. Synchronize packages.
4. Find and install **DrumCloud JS**.
5. Add `JS: DrumCloud JS` to a track and send it MIDI.

Starting with v0.27.1, DrumCloud is self-contained: the two ReaKit libraries used
by its interface are installed inside the DrumCloud effect folder. You do not
need to add the ReaKit repository or install ReaKit separately. Existing ReaKit
installations can remain installed; DrumCloud simply uses its pinned local copy.

If you are updating from v0.27, synchronize packages and update DrumCloud JS.

### If the custom GUI is still missing

The native Sample selector without the dark-and-gold interface normally means
REAPER is still loading the older v0.27 package or the v0.27.1 support files did
not install completely.

1. In ReaPack, choose **Synchronize packages**.
2. Confirm that **DrumCloud JS 0.27.1** is installed, then reinstall it if needed.
3. Close and reopen the effect, or restart REAPER.

DrumCloud does not require a separate ReaKit installation. For comparison,
updates or direct ReaKit support, these are the official links:

- [ReaKit project and documentation](https://github.com/mequaz-sudo/ReaKit)
- [ReaKit ReaPack repository URL](https://raw.githubusercontent.com/mequaz-sudo/ReaKit/main/index.xml)

Installing the full ReaKit package is optional and should not be necessary for
DrumCloud v0.27.1. If the GUI is still missing after reinstalling DrumCloud,
please report the REAPER version, operating system and the exact error message
in the [DrumCloud issue tracker](https://github.com/Chmod666music/DrumCloud-ReaPack/issues).

### Install the factory presets

1. Open **Actions → Show action list** after installing DrumCloud JS.
2. Search for **Install DrumCloud Factory Presets** and run the action once.
3. Close and reopen DrumCloud JS to refresh its preset list.

If a DrumCloud preset bank already exists, the installer creates a timestamped
backup before installing the factory bank.

ReaPack installs the instrument under `Effects` (the path can include the
repository/category prefix, for example
`Effects/DrumCloud-ReaPack/Effects/DrumCloud`) and the samples in
`Data/DrumCloud` inside the REAPER resource directory.

## Features

- Granular sample playback with MIDI pitch
- Dark-and-gold scalable ReaKit interface with automation-safe controls
- Waveform display and click/drag positioning
- Grain size, density, position spread and stereo spread
- Animated grain markers
- Sample Start and Sample End range controls
- Forward, Backward, Ping Pong, Random Jump and Random Walk movement
- Per-grain pitch spread plus adjustable attack and release envelopes
- Stereo Room, Hall and Shimmer cloud reverb
- Filtered Stereo and Ping Pong delay
- Transparent output peak protection
- 46 factory presets made for v0.23

## Samples

All 130 factory samples were created by
[REVERBERA](https://freesound.org/people/REVERBERA/) and come from the
[Reverbera som pack on Freesound](https://freesound.org/people/REVERBERA/packs/45512/).
They are distributed under CC0 1.0. Detailed source and license information is
installed in `Data/DrumCloud/SAMPLE_CREDITS_AND_LICENSE.md`.

## Licenses

- DrumCloud JS source code: [MIT](LICENSE)
- Bundled ReaKit GUI libraries: MIT, Copyright (c) 2026 EON Studios; see `Effects/DrumCloud/ReaKit/LICENSE.txt` and the bundled third-party credits
- Factory samples: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)

ReaKit was created by EON Studios / mequaz-sudo. See the
[upstream project](https://github.com/mequaz-sudo/ReaKit) and its
[ReaPack repository](https://raw.githubusercontent.com/mequaz-sudo/ReaKit/main/index.xml).

## v0.26 tuning retained in v0.27.1

Sample Fine Tune is appended as slider 33: -100 to +100 cents, default 0.
Positive values raise pitch. Zero preserves v0.25 playback. All new grains,
including grains from already held voices, use the current Fine Tune; grains
already playing finish at their original rate to preserve boundary stability.
Root MIDI note retains its existing behavior. Existing sliders 1–32 and the
46-preset bank are unchanged.

Detect Root analyzes three regions of the loaded sample, using normalized
mean-subtracted autocorrelation with parabolic peak refinement. It reports
note name (C4 = MIDI 60), MIDI number, measured cents offset and confidence.
Confidence is a correlation score, not a calibrated probability. READY requires
all three regions, at least 72% correlation and agreement within 30 cents.
Noise, chords, short or changing-pitch material may be rejected or misidentified.
Analysis is synchronous and may briefly pause REAPER; run it while stopped.

The persistent result line above the waveform shows READY, APPLIED or a rejection
message even when the lower information panel is off-screen. Idle only means the
command has finished; it does not mean the result was discarded.

Detection alone changes no tuning. Use Apply Detected Tuning (slider 34):
**Apply Root Only** or **Apply Root + Tune**. Only READY/APPLIED results can be
applied; low-confidence results preserve both manual controls. Commands return
to Idle. Loading a different sample invalidates the result. A source detected
as F#3, -23 cents requires Root 54 and Fine Tune **+23** cents to correct it.
Both manual controls remain available afterward. Factory Auto Root remains
opt-in and does not set Fine Tune. Reset Fine Tune manually when changing samples
if the previous correction is no longer wanted.

Old presets and saved states gain default-zero Fine Tune when loaded fresh.
The factory bank is preserved byte for byte; please verify old preset switching
in REAPER, especially when switching from a newly tuned state to an older preset.

## User samples

`Data/DrumCloud/User Samples/` is reserved/documented in v0.26. Separate selectors,
Factory/User tabs and custom-folder browsing remain planned for a future release.
The original Sample slider and factory paths are unchanged. For current playback,
place a uniquely named WAV directly in `Data/DrumCloud`, reopen the effect and
select it. Keep originals in User Samples if useful. Do not assume the native
slider scans nested folders. See the bundled User Samples README.

## Local development installation

Keep this repository outside the REAPER resource `Effects` folder. Never copy
or clone the whole repo there: REAPER recursively discovers its JSFX and creates
a duplicate entry. Use Python 3.9+:

```sh
python3 tools/install_dev.py "/path/from/REAPER/Options/Show-REAPER-resource-path"
```

The installer reads ReaPack's registry and updates its existing instrument path.
Without a registered installation, it uses `Effects/DrumCloud`. It copies the
main JSFX plus its bundled `ReaKit` folder beside it, factory data to
`Data/DrumCloud`, and the preset action to `Scripts/DrumCloud`.
Existing files are backed up outside Effects; user audio and installed preset
banks are kept. A registered `Effects/DrumCloud-ReaPack` directory is legitimate
and is never archived. If that directory is unregistered and contains the
nested DrumCloud effect, inspect it and rerun with `--archive-duplicate` to move
it to `DrumCloud-dev-backups` outside Effects. Nothing is deleted.
For manual development installs, load the preset Lua script via Action List →
ReaScript: Load, then run it. ReaPack registers the action automatically.

ReaPack remains the normal distribution mechanism. The existing GitHub workflow
regenerates index.xml from committed JSFX metadata on main after each release.

JSFX file-slider and file-loading behavior follow the
[Cockos reference](https://www.reaper.fm/sdk/js/js.php) and
[file API](https://www.reaper.fm/sdk/js/file.php).
