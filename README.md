# DrumCloud JS

DrumCloud JS is a granular sample instrument for REAPER.

This repository is a ReaPack repository. Installing the package installs the
JSFX instrument, its CC0 factory samples, and a 46-preset factory bank.

## Install with ReaPack

1. Open **Extensions → ReaPack → Import repositories** in REAPER.
2. Paste this URL:

   `https://raw.githubusercontent.com/Chmod666music/DrumCloud-ReaPack/main/index.xml`

3. Synchronize packages.
4. Find and install **DrumCloud JS**.
5. Add `JS: DrumCloud JS` to a track and send it MIDI.

### Install the factory presets

1. Open **Actions → Show action list** after installing DrumCloud JS.
2. Search for **Install DrumCloud Factory Presets** and run the action once.
3. Close and reopen DrumCloud JS to refresh its preset list.

If a DrumCloud preset bank already exists, the installer creates a timestamped
backup before installing the factory bank.

ReaPack installs the instrument in `Effects/DrumCloud` and the samples in
`Data/DrumCloud` inside the REAPER resource directory.

## Features

- Granular sample playback with MIDI pitch
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
- Factory samples: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)
