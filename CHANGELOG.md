# Changelog

## 0.27.1
- Bundle the ReaKit GUI controls used by DrumCloud inside the package.
- Remove the separate ReaKit-install requirement and the missing-GUI failure mode.
- Include the ReaKit MIT license and attribution with the installed effect.
- Keep imports, GUI layout, all 34 sliders, presets, automation and the v0.26 audio engine unchanged.
- Improve installation/documentation links for ReaPack users.

## 0.27
- Add a scalable dark charcoal/navy interface with a unified gold accent.
- Add ReaKit Serum-style primary knobs and Encoder-style helper controls.
- Add complete GRAIN, MOTION, PITCH, SPACE, DELAY and SOURCE/OUTPUT panels.
- Preserve the custom waveform and grain visualization with direct positioning.
- Keep every existing slider number, range, default and order compatible.
- Add REAPER Last Touched and automation-safe gestures to all custom controls.
- Keep the native Sample selector as the reliable source-loading control.
- Initially imported ReaKit 1.3.0 as a separate dependency; v0.27.1 vendors the required controls locally.
- Preserve the v0.26 audio engine and factory preset bank unchanged.

## 0.26
- Show persistent detection feedback above the waveform so it is visible on short screens.
- Append default-zero Sample Fine Tune (slider 33), without reordering parameters.
- Refine multi-region normalized-autocorrelation peaks to fractional lags.
- Report note name, MIDI root, measured cents and correlation confidence.
- Separate detection from explicit root-only/root-plus-correction apply (slider 34).
- Reject inconsistent regions for automatic application; preserve manual overrides.
- Reserve/document User Samples folder without changing existing sample paths.
- Add portable, selective development installer with backup/duplicate archival.
- Preserve factory samples, 46-preset bank, grain boundary handling and effects.

## 0.25 baseline
Per-grain direction, Density Spread, user-triggered root detection, 8 voices,
32 shared grains and the v0.24.2 grain-boundary stability fixes.
