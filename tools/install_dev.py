#!/usr/bin/env python3
"""Install from a checkout outside Effects. Requires an explicit REAPER resource path."""
import argparse
from pathlib import Path
import shutil
import sqlite3
from datetime import datetime


def install(repo, resource, archive_duplicate=False):
    repo, resource = repo.resolve(), resource.expanduser().resolve()
    effects = resource / "Effects"
    if repo.is_relative_to(effects.resolve()):
        raise ValueError("Move the development checkout outside REAPER Effects first.")
    source = repo / "Effects" / "DrumCloud"
    if not (source / "DrumCloud_JS.jsfx").is_file():
        raise ValueError("DrumCloud source missing")
    if not resource.is_dir():
        raise ValueError("Choose the existing REAPER resource folder shown in REAPER Options.")
    # ReaPack may legitimately use the repository/category prefix. Preserve
    # its registered effect identity so projects and preset banks still match.
    registry = resource / "ReaPack" / "registry.db"
    registered = []
    registered_paths = []
    if registry.is_file():
        with sqlite3.connect(registry.as_uri() + "?mode=ro", uri=True) as db:
            registered_paths = [resource / row[0] for row in db.execute("SELECT path FROM files")]
        registered = [p for p in registered_paths if p.name == "DrumCloud_JS.jsfx" and p.is_relative_to(effects)]
    if len(registered) > 1:
        raise ValueError("Multiple registered DrumCloud effects; inspect ReaPack before installing.")
    target = registered[0] if registered else effects / "DrumCloud" / "DrumCloud_JS.jsfx"
    if not target.resolve().is_relative_to(effects.resolve()):
        raise ValueError("Registered effect path escapes Effects; inspect it manually.")
    duplicate = effects / "DrumCloud-ReaPack"
    managed_directory = any(p.is_relative_to(duplicate) for p in registered_paths)
    archive_needed = (duplicate.exists() or duplicate.is_symlink()) and not managed_directory
    if archive_needed:
        if not archive_duplicate:
            raise ValueError("Duplicate checkout found. Review it, then use --archive-duplicate.")
        expected = duplicate / "Effects" / "DrumCloud" / "DrumCloud_JS.jsfx"
        if not expected.is_file():
            raise ValueError("Unexpected duplicate layout; inspect it manually.")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = resource / "DrumCloud-dev-backups" / stamp
    pairs = [(source / "DrumCloud_JS.jsfx", target)]
    pairs += [(p, resource / "Data" / "DrumCloud" / p.name) for p in (source / "Samples").iterdir() if p.is_file()]
    pairs += [(source / "User Samples" / "README.md", resource / "Data" / "DrumCloud" / "User Samples" / "README.md")]
    pairs += [(source / "Presets" / "DrumCloud_v0.23_46_Factory_Presets.ini", resource / "Data" / "DrumCloud" / "DrumCloud_v0.23_46_Factory_Presets.ini"),
              (source / "Presets" / "Install_DrumCloud_Factory_Presets.lua", resource / "Scripts" / "DrumCloud" / "Install_DrumCloud_Factory_Presets.lua")]
    for src, dst in pairs:
        if dst.exists():
            old = backup / dst.relative_to(resource)
            old.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, old)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    if archive_needed:
        backup.mkdir(parents=True, exist_ok=True)
        shutil.move(str(duplicate), str(backup / "DrumCloud-ReaPack"))
    print("Installed", target.relative_to(resource), "Backups:", backup)
    print("Load Scripts/DrumCloud/Install_DrumCloud_Factory_Presets.lua in the Action List if needed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("resource", type=Path)
    parser.add_argument("--archive-duplicate", action="store_true")
    args = parser.parse_args()
    install(Path(__file__).resolve().parents[1], args.resource, args.archive_duplicate)
