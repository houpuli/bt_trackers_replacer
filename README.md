# qBittorrent Tracker Replacement Script

**Original Description**
Torrent tracker replacer for qBittorrent (and possibly other BT clients)
 
Replaces old/outdated trackers in .fastresume files. Requires Python 3.6 or higher.
Place it alongside a `BT_backup` folder next to this script
 

Usage: python tracker\_replace.py \[old\_tracker] \[new\_tracker] \[--backup-dir DIR] (--dry-run | --apply)
 

# qBittorrent Tracker Replacement Script

A simple Python 3 script to replace tracker URLs in qBittorrent `.fastresume` files. It defaults to looking in a `BT_backup` folder located alongside the script, and supports both interactive prompts and non‑interactive modes (`--dry-run` or `--apply`).

---

## Requirements

* Python 3.6 or higher
* No external dependencies (uses only standard library)

---

## Installation

1. Clone or download this repository.
2. Place `tracker_replace.py` in your desired folder.
3. Ensure a `BT_backup` subfolder (containing your `.fastresume` files) sits next to `tracker_replace.py`. Alternatively, you can point to any other folder with `--backup-dir`.

---

## Usage

```bash
python tracker_replace.py [old_tracker] [new_tracker] [--backup-dir DIR] (--dry-run | --apply)
```

* **old\_tracker**: (optional positional) the URL or text to be replaced. If omitted, you will be prompted.
* **new\_tracker**: (optional positional) the replacement URL/text. If omitted, you will be prompted.
* **--backup-dir**: (optional) path to your `BT_backup` folder. Defaults to `./BT_backup` next to the script.
* **--dry-run**: show which files would be modified (counts and up to five samples) without writing changes.
* **--apply**: write changes to the `.fastresume` files.

You must specify exactly one of `--dry-run` or `--apply`. If neither flag is given, the script will prompt you to choose (default is dry‑run).

---

## Examples

### Linux / macOS (bash)

```bash
cd /path/to/script_folder
python3 tracker_replace.py \
  "https://old.example.com/announce" \
  "https://new.example.com/announce" \
  --dry-run
```

To apply the changes:

```bash
python3 tracker_replace.py \
  "https://old.example.com/announce" \
  "https://new.example.com/announce" \
  --apply
```

### Windows (Command Prompt)

```bat
C:\> cd C:\path\to\script_folder
C:\path\to\script_folder> python tracker_replace.py "https://old.example.com/announce" "https://new.example.com/announce" --dry-run
```

To apply:

```bat
C:\path\to\script_folder> python tracker_replace.py "https://old.example.com/announce" "https://new.example.com/announce" --apply
```

### Windows (PowerShell)

```powershell
PS C:\> Set-Location 'C:\path\to\script_folder'
PS C:\path\to\script_folder> python .\tracker_replace.py \
  "https://old.example.com/announce" \
  "https://new.example.com/announce" \
  --dry-run
```

To apply:

```powershell
PS C:\path\to\script_folder> python .\tracker_replace.py `
  "https://old.example.com/announce" `
  "https://new.example.com/announce" `
  --apply
```

---

## Interactive Mode

If you omit either `old_tracker`, `new_tracker`, or both, the script will prompt you to enter them:

```bash
$ python tracker_replace.py --dry-run
Enter old tracker URL/text: https://old.example.com/announce
Enter new tracker URL/text: https://new.example.com/announce
Dry-run: 3 file(s) would be modified.
Sample changes:
  In file1.fastresume:
    https://old.example.com/announce -> https://new.example.com/announce
  ...
```

If you omit both `--dry-run` and `--apply`, you will be asked:

```bash
Apply changes? [y/N]: y
```

(Default is `N` which results in a dry‑run.)

---

## Troubleshooting

* **Error: backup directory not found**
  Ensure `BT_backup` exists next to the script, or specify `--backup-dir` correctly.

* **No .fastresume files found**
  Verify your `.fastresume` files are in the specified backup directory.

* **Unicode or encoding errors**
  The script assumes ASCII‑compatible tracker URLs. Non‑ASCII data in the tracker section may be skipped.

---

Feel free to open an issue or submit a pull request for enhancements!

## Acknowledgements

This project is a fork of [Stat1cV01D/bt\_trackers\_replacer](https://github.com/Stat1cV01D/bt_trackers_replacer). Many thanks to the original author, Stat1cV01D, for the initial implementation!
