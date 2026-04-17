import os
import sys

SEPARATOR = "\n\n---- ends here ----\n\n"
OUTPUT_FILE = "all_models.py"

def find_models_files(root="."):
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        # skip virtualenvs, hidden dirs, node_modules
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith(".")
            and d not in ("venv", "env", ".venv", "node_modules", "__pycache__")
        ]
        for f in filenames:
            if f == "models.py":
                found.append(os.path.join(dirpath, f))
    return sorted(found)

def collect(root="."):
    files = find_models_files(root)
    if not files:
        print("No models.py files found.")
        sys.exit(1)

    parts = []
    for path in files:
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read().strip()
        parts.append(f"# {path}\n\n{content}")
        print(f"  + {path}")

    output = SEPARATOR.join(parts)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(output)

    print(f"\nDone. {len(files)} file(s) → {OUTPUT_FILE}")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    collect(root)
