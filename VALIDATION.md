# DrumCloud validation and release notes

## v0.27.1 self-contained GUI hotfix — 2026-09-17

v0.27.1 vendors the two exact ReaKit 1.3.0 libraries used by DrumCloud. They
provide the Serum and Encoder knobs plus the pill and segmented buttons used by
the interface and are pinned at upstream commit
`04996cc3f86a2b7098e50fc7cfdf0ae561e69ee4`. Both local includes are standalone,
so the dependency closure contains no further runtime imports.

Automated validation resolves every `ReaKit/` import beneath the installed
DrumCloud effect directory, rejects transitive imports in the vendored files,
and checks that the v0.27.1 entry in `index.xml` installs both includes, the MIT
license and third-party credits. The existing v0.26 comparison still verifies
that all 34 sliders and the complete `@sample` audio section are unchanged.
The 46 factory presets remain byte-identical to their baseline.

## v0.27 GUI release validation — 2026-09-15

v0.27 promotes the completed GUI from `gui/v0.27-dev` while retaining v0.26 as
the frozen compatibility baseline. Automated comparison against source commit
`15b93760f8c86b03ae290d10abf34e4afb14a072` verifies that all 34 slider numbers,
variables, defaults, ranges, steps and label text are preserved. A leading `-`
only hides the 33 parameters with custom equivalents. The native Sample file
slider remains visible because JSFX does not expose its scanned list to a
custom dropdown.

The complete `@sample` section is byte-identical to v0.26. Presets, factory
samples and installer isolation checks pass. Actual EEL detector tests continue
to pass at 44.1, 48 and 96 kHz, including rejection cases and correction sign.

Confirmed manually in REAPER by the user:

- All GRAIN, MOTION, PITCH, SPACE, DELAY and SOURCE/OUTPUT controls respond.
- Start/End knobs and waveform boundaries remain synchronized.
- Native Sample selection loads samples correctly.
- Window resizing and uniform GUI scaling work.
- REAPER Last Touched and automation work after explicit slider bitmasks and
  touch-session completion were applied to all custom controls.
- Preset changes populate the custom controls and waveform correctly during
  the GUI development sessions.

The frozen diagnostic v0.26 `@gfx` copy was removed after checkpoint `61ef213`.
The original implementation remains in Git history. This cleanup did not touch
the engine. The resulting v0.27 source was promoted only after the listed host
checks passed.

Baseline: GitHub main ccbdc0a (index update); JSFX source commit
8f5b60b943bfbbe38b4bc7f7b1c05e10f1fd201f, version 0.25.

## Passed

- Compiled the complete EEL source with Cockos WDL's portable EEL engine.
  REAPER-only file/MIDI/slider/graphics functions were replaced by no-op stubs
  for this syntax check; this is not a full REAPER host test.
- Ran the actual source detector and apply code in EEL on five synthesized
  tones (including a harmonic-rich signal) at 44.1, 48 and 96 kHz.
  Expected cents: -23, +31, -42, +47, -49. Largest error: 0.008 cent.
- Verified analysis alone preserves manual root/fine tune, and explicit combined
  application sets the correct MIDI root and opposite-sign pitch correction.
- Silence, random noise and three regions with different pitches were rejected;
  low-confidence application left manual controls unchanged.
- Sliders 1–32 match v0.25 exactly. The complete @sample section matches v0.25
  apart from adding Fine Tune to the per-grain detune exponent. At zero, that
  exponent is unchanged. MIDI handling, shared-pool boundary checks, grain
  retirement, reverb/shimmer/delay and output protection were not rewritten.
- All 46 presets and the factory preset installer are byte-identical to baseline.
  All 130 factory WAV files remain present and unchanged.
- Temporary-resource installation test verified duplicate refusal, explicit
  archival outside Effects, exactly one discoverable JSFX, and user-file survival.
- Full-source compilation and whitespace checks passed after final changes.

## Local REAPER verification

On 2026-09-04 the user confirmed detection/application works after moving the
result line above the waveform. The supplied screenshot shows B2 / MIDI 47,
measured +1.7 cents, Fine Tune -1.664849 cents and APPLIED status. The local
ReaPack-registered JSFX was updated in place with a backup.

## Remaining host coverage

Further checks: listening/null comparison at zero Fine Tune,
old projects, switching old/new presets, automation, polyphony, extreme ranges,
all four grain directions, sample-rate changes and factory preset action.
Automated source checks do not replace these host checks. Fine Tune affects newly
spawned grains; currently sounding grains retain their rate until completion.
The synchronous detector can briefly pause processing; analyze while stopped.
Pitch detection can misidentify octave/harmonic content and is not intended to
extract a root from arbitrary chords, drums or changing-pitch material.

User Samples is folder/readout groundwork, not an implemented nested browser.
The development installer preserves the ReaPack-registered instrument location.

## Reproduce

Use a Git checkout containing the baseline history. Build Cockos WDL eel2's
loose_eel, then run:

```
python3 tests/test_release.py /path/to/loose_eel
python3 tests/compile_full.py /path/to/loose_eel
```

## Publish

The JSFX version/changelog/provides metadata declares 0.27.1. After the release
commit reaches main, the GitHub workflow runs reapack-index --rebuild and publishes the index
with real committed source URLs, including the local ReaKit dependency closure,
license, credits and User Samples README. No
unpublished or invented commit URLs have been inserted into the index.
