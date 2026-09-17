#!/usr/bin/env python3
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
main = repo / "Effects/DrumCloud/DrumCloud_JS.jsfx"
readme = repo / "README.md"
changelog = repo / "CHANGELOG.md"
gui = repo / "GUI_DEVELOPMENT.md"
installer = repo / "tools/install_dev.py"
tests = repo / "tests/test_release.py"


def one(text, old, new, label):
    if text.count(old) != 1:
        raise RuntimeError(f"{label}: expected exactly one match, got {text.count(old)}")
    return text.replace(old, new, 1)

# Main JSFX: packaging-only patch. Imports stay unchanged so REAPER resolves the
# bundled ReaKit/Library directory beside DrumCloud_JS.jsfx.
s = main.read_text()
s = one(s, "version: 0.27\n", "version: 0.27.1\n", "metadata version")
s = one(s, "changelog:\n", "changelog:\n  Bundle the required ReaKit GUI controls so DrumCloud opens with its full interface without a separate ReaKit install.\n  Add bundled ReaKit MIT license and attribution files.\n", "changelog header")
s = one(s, "  REVERBERA sound pack https://freesound.org/people/REVERBERA/packs/45512/\nprovides:\n",
        "  REVERBERA sound pack https://freesound.org/people/REVERBERA/packs/45512/\n  Documentation https://github.com/Chmod666music/DrumCloud-ReaPack/blob/main/README.md\n  ReaKit upstream https://github.com/mequaz-sudo/ReaKit\nprovides:\n  ReaKit/Library/*\n  ReaKit/LICENSE.txt\n  ReaKit/THIRD_PARTY_CREDITS.md\n",
        "links/provides")
s = one(s,
        "// ReaKit is a separate ReaPack dependency. Its public knob dispatcher provides\n// the Serum and Encoder styles used by the v0.27 interface.\n",
        "// ReaKit GUI controls are bundled locally under DrumCloud/ReaKit/Library.\n// The import paths stay unchanged; no separate ReaKit installation is required.\n",
        "ReaKit comment")
s = one(s, "version = 0.27;", "version = 0.271;", "runtime version")
s = one(s, 'gfx_drawstr("v0.27  /  REAKIT GUI");', 'gfx_drawstr("v0.27.1  /  REAKIT GUI");', "GUI version")
main.write_text(s)

# README: self-contained installation, credit, and update path.
r = readme.read_text()
r = one(r, "# DrumCloud JS v0.27\n", "# DrumCloud JS v0.27.1\n", "README title")
r = one(r,
        "v0.27 adds a complete dark-and-gold ReaKit interface while preserving the\nv0.26 audio engine, slider numbering, presets, saved states and automation.\nIt includes custom GRAIN, MOTION, PITCH, SPACE, DELAY and SOURCE/OUTPUT panels,\nplus REAPER Last Touched support for all custom controls.\n",
        "v0.27.1 keeps the complete dark-and-gold ReaKit interface while preserving the\nv0.26 audio engine, slider numbering, presets, saved states and automation.\nThe required ReaKit GUI controls are now bundled with DrumCloud, so there is no\nseparate ReaKit dependency to install. GRAIN, MOTION, PITCH, SPACE, DELAY and\nSOURCE/OUTPUT panels plus REAPER Last Touched support are unchanged.\n",
        "README intro")
r = one(r,
        "3. Synchronize packages.\n4. Find and install **ReaKit** (tested with version 1.3.0).\n5. Find and install **DrumCloud JS**.\n6. Add `JS: DrumCloud JS` to a track and send it MIDI.\n\nReaKit is required by the v0.27 interface and is imported from its normal\nReaPack installation. DrumCloud does not bundle or duplicate the library. If\nREAPER reports a missing `ReaKit/Library` import, install or update ReaKit and\nthen reopen or rescan DrumCloud JS.\n",
        "3. Synchronize packages.\n4. Find and install **DrumCloud JS**.\n5. Add `JS: DrumCloud JS` to a track and send it MIDI.\n\nStarting with v0.27.1, DrumCloud is self-contained: the small ReaKit subset used\nby its interface is installed inside the DrumCloud effect folder. You do not\nneed to add the ReaKit repository or install ReaKit separately. Existing ReaKit\ninstallations can remain installed; DrumCloud simply uses its pinned local copy.\n\nIf you are updating from v0.27, synchronize packages and update DrumCloud JS.\n",
        "README install")
r = one(r,
        "- DrumCloud JS source code: [MIT](LICENSE)\n- Factory samples: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)\n",
        "- DrumCloud JS source code: [MIT](LICENSE)\n- Bundled ReaKit GUI subset: MIT, Copyright (c) 2026 EON Studios; see `Effects/DrumCloud/ReaKit/LICENSE.txt` and the bundled third-party credits\n- Factory samples: [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)\n",
        "README licenses")
r = one(r, "## v0.26 tuning retained in v0.27\n", "## v0.26 tuning retained in v0.27.1\n", "README tuning header")
r = one(r,
        "The installer reads ReaPack's registry and updates its existing instrument path.\nWithout a registered installation, it uses `Effects/DrumCloud`. It copies only\nfactory data to `Data/DrumCloud` and the preset action to `Scripts/DrumCloud`.\n",
        "The installer reads ReaPack's registry and updates its existing instrument path.\nWithout a registered installation, it uses `Effects/DrumCloud`. It copies the\nmain JSFX plus its bundled `ReaKit` folder beside it, factory data to\n`Data/DrumCloud`, and the preset action to `Scripts/DrumCloud`.\n",
        "README dev installer")
# Add upstream credit near license section if it is not already there.
needle = "## v0.26 tuning retained in v0.27.1\n"
credit = "ReaKit was created by EON Studios / mequaz-sudo. Upstream project:\nhttps://github.com/mequaz-sudo/ReaKit\n\n"
r = r.replace(needle, credit + needle, 1)
readme.write_text(r)

# Changelog.
c = changelog.read_text()
entry = "# Changelog\n\n## 0.27.1\n- Bundle the ReaKit GUI controls used by DrumCloud inside the package.\n- Remove the separate ReaKit-install requirement and the missing-GUI failure mode.\n- Include the ReaKit MIT license and attribution with the installed effect.\n- Keep imports, GUI layout, all 34 sliders, presets, automation and the v0.26 audio engine unchanged.\n- Improve installation/documentation links for ReaPack users.\n\n"
c = one(c, "# Changelog\n\n", entry, "CHANGELOG header")
c = c.replace("- Import ReaKit 1.3.0 as a separate ReaPack-installed dependency.\n", "- Initially imported ReaKit 1.3.0 as a separate dependency; v0.27.1 vendors the required controls locally.\n", 1)
changelog.write_text(c)

# GUI development notes: describe pinned local dependency and update the manual check.
g = gui.read_text()
g = one(g, "# DrumCloud v0.27 ReaKit GUI\n", "# DrumCloud v0.27.1 ReaKit GUI\n", "GUI doc title")
old_dep = "## ReaKit dependency\n\nInstall **ReaKit** with ReaPack before loading DrumCloud v0.27. The\nJSFX imports the installed library directly:\n\n```eel\nimport ReaKit/Library/knobs_kbsg.jsfx-inc\n```\n\nThe interface was developed against ReaKit 1.3.0. In REAPER, use\n**Extensions → ReaPack → Browse packages**, find ReaKit, install it, then reopen\nor rescan the DrumCloud JSFX. Do not copy the library into this repository.\n"
new_dep = "## ReaKit dependency\n\nStarting with v0.27.1, DrumCloud vendors the small ReaKit subset it actually\nuses under `Effects/DrumCloud/ReaKit/Library/`. The existing imports remain:\n\n```eel\nimport ReaKit/Library/knobs_kbsg.jsfx-inc\nimport ReaKit/Library/buttons_kbsg.jsfx-inc\n```\n\nREAPER resolves those files beside the JSFX, so users no longer need a separate\nReaKit install. The copy is intentionally pinned: GUI behavior cannot change\nunder an existing DrumCloud release when upstream ReaKit updates. ReaKit is MIT\nlicensed by EON Studios; the license and attribution ship beside the subset.\n"
g = one(g, old_dep, new_dep, "GUI dependency section")
g = g.replace("1. Confirm the effect compiles with ReaKit installed and reports\n   `v0.27 / REAKIT GUI`.\n", "1. Confirm the effect compiles with no separate ReaKit installation and reports\n   `v0.27.1 / REAKIT GUI`.\n", 1)
g = g.replace("7. Temporarily remove/rename the ReaKit install and confirm the resulting import\n   error makes the missing dependency obvious; restore it before further tests.\n", "7. Temporarily remove/rename any separately installed ReaKit and confirm DrumCloud\n   still opens with the complete GUI from its bundled local copy.\n", 1)
gui.write_text(g)

# Development installer: copy the vendored ReaKit folder beside whichever JSFX
# path ReaPack has registered.
i = installer.read_text()
old = '    pairs = [(source / "DrumCloud_JS.jsfx", target)]\n'
new = ('    pairs = [(source / "DrumCloud_JS.jsfx", target)]\n'
       '    bundled_reakit = source / "ReaKit"\n'
       '    pairs += [(p, target.parent / "ReaKit" / p.relative_to(bundled_reakit))\n'
       '              for p in bundled_reakit.rglob("*") if p.is_file()]\n')
i = one(i, old, new, "installer pairs")
installer.write_text(i)

# Structural tests: assert self-contained GUI files exist and dev install copies them.
t = tests.read_text()
t = t.replace("# and audio engine byte-for-byte. ReaKit stays an imported dependency.\n", "# and audio engine byte-for-byte. ReaKit imports now resolve to bundled local files.\n", 1)
anchor = "assert 'import ReaKit/Library/buttons_kbsg.jsfx-inc' in s\n"
addition = (anchor +
            "assert (repo/'Effects/DrumCloud/ReaKit/Library/knobs_kbsg.jsfx-inc').is_file()\n"
            "assert (repo/'Effects/DrumCloud/ReaKit/Library/buttons_kbsg.jsfx-inc').is_file()\n"
            "assert (repo/'Effects/DrumCloud/ReaKit/LICENSE.txt').is_file()\n")
t = one(t, anchor, addition, "test import assertions")
anchor2 = "    assert len(list((r/'Effects').rglob('*.jsfx'))) == 1\n    assert len(list((r/'DrumCloud-dev-backups').rglob('DrumCloud_JS.jsfx'))) == 1\n"
addition2 = "    assert len(list((r/'Effects').rglob('*.jsfx'))) == 1\n    assert (r/'Effects/DrumCloud/ReaKit/Library/knobs_kbsg.jsfx-inc').is_file()\n    assert (r/'Effects/DrumCloud/ReaKit/Library/buttons_kbsg.jsfx-inc').is_file()\n    assert len(list((r/'DrumCloud-dev-backups').rglob('DrumCloud_JS.jsfx'))) == 1\n"
t = one(t, anchor2, addition2, "test dev install")
tests.write_text(t)

# One-shot script: remove itself so subsequent index rebuilds are clean.
Path(__file__).unlink()
print("Prepared DrumCloud JS v0.27.1 self-contained ReaKit hotfix")
