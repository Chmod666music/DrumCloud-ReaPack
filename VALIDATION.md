# v0.26 validation and release notes

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

The JSFX version/changelog/provides metadata declares 0.26. After a release
commit reaches main, the GitHub workflow runs reapack-index --rebuild and publishes the index
with real committed source URLs, including the User Samples README. No
unpublished or invented commit URLs have been inserted into the index.
