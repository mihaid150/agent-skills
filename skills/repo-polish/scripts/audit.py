"""Mechanical scan for repo-polish. Read-only; prints a Markdown report.

Signals, not verdicts: every hit must be confirmed by reading the code.
Python files get AST checks; other text files get generic checks.

Usage: python audit.py <repo-root> [--max-file-lines 500] [--max-func-lines 60]
"""
import argparse
import ast
import hashlib
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

TEXT_EXT = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cs", ".go", ".rs", ".sh",
            ".ps1", ".yml", ".yaml", ".toml", ".cfg", ".ini", ".json", ".md", ".c", ".cpp", ".h"}
JUNK = re.compile(r"(^|/)(__pycache__/|\.ipynb_checkpoints/|\.DS_Store$|Thumbs\.db$|\.idea/|\.vscode/|"
                  r"venv/|\.venv/|env/|node_modules/|.*\.pyc$|.*\.log$|.*\.env$|\.env$)")
STRAY = re.compile(r"(_old|_new|_backup|_bak|_copy|_tmp|_temp|_final|_v\d+|\d+)\.[a-z]+$|"
                   r"(^|/)(old|backup|tmp|temp|copy)[_\-.]|\(\d\)\.|\.bak$|\.orig$", re.I)
NARRATION = re.compile(r"#\s*(step\s*\d+\s*[:.)-]|now\s+(we|let'?s|i)\b|let'?s\b|here\s+we\b|"
                       r"this\s+(function|method|class|code|block|script)\s|we\s+(need|will|now)\b|"
                       r"first,|next,|finally,)", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿✅❌✨]")
BANNER = re.compile(r"^\s*#\s*[=\-*#]{8,}")
ABS_PATH = re.compile(r"""["'](?:[A-Za-z]:\\\\?|[A-Za-z]:/|/home/|/Users/|/mnt/[a-z]/)[^"']*["']""")
TODO = re.compile(r"#\s*(TODO|FIXME|HACK|XXX)\b")


def tracked_files(root):
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, check=True)
        return [p for p in out.stdout.decode("utf-8", "replace").split("\0") if p]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [str(p.relative_to(root)).replace("\\", "/") for p in root.rglob("*")
                if p.is_file() and ".git" not in p.parts]


def looks_like_code(comment):
    body = comment.lstrip("#").strip()
    if len(body) < 4 or body.endswith(":") and " " not in body.rstrip(":"):
        return False
    if not re.search(r"[=()\[\].]|^(import|from|return|if|for|def|class|print)\b", body):
        return False
    try:
        ast.parse(body)
        return True
    except SyntaxError:
        return False


def python_checks(path, text, args, hits, func_hashes):
    try:
        tree = ast.parse(text)
    except SyntaxError as e:
        hits["Python files that do not parse"].append(f"{path}:{e.lineno}")
        return
    imported, used = {}, set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.ImportFrom) and node.module == "__future__":
                continue
            for a in node.names:
                name = (a.asname or a.name).split(".")[0]
                if name != "*":
                    imported.setdefault(name, node.lineno)
        elif isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute):
            base = node
            while isinstance(base, ast.Attribute):
                base = base.value
            if isinstance(base, ast.Name):
                used.add(base.id)
        elif isinstance(node, ast.ExceptHandler):
            silent = all(isinstance(s, (ast.Pass, ast.Continue)) or
                         (isinstance(s, ast.Expr) and isinstance(getattr(s, "value", None), ast.Constant))
                         for s in node.body)
            broad = node.type is None or (isinstance(node.type, ast.Name) and node.type.id in ("Exception", "BaseException"))
            if node.type is None:
                hits["Bare `except:`"].append(f"{path}:{node.lineno}")
            elif broad and silent:
                hits["Silent broad except (`except Exception: pass`)"].append(f"{path}:{node.lineno}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            length = (node.end_lineno or node.lineno) - node.lineno + 1
            if length > args.max_func_lines:
                hits[f"Functions over {args.max_func_lines} lines"].append(f"{path}:{node.lineno} {node.name} ({length} lines)")
            if length >= 6:
                body = ast.dump(ast.Module(body=node.body, type_ignores=[]), annotate_fields=False)
                func_hashes[hashlib.sha1(body.encode()).hexdigest()].append(f"{path}:{node.lineno} {node.name}")
    exported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            exported = {getattr(e, "value", None) for e in getattr(node.value, "elts", [])}
    if not path.endswith("__init__.py"):
        for name, line in imported.items():
            if name not in used and name not in exported and not re.search(rf"\b{re.escape(name)}\b", text.split("\n", line)[-1]):
                hits["Possibly unused imports"].append(f"{path}:{line} {name}")
    if "__main__" not in text and re.search(r"^\s*print\(", text, re.M) and "/scripts/" not in f"/{path}":
        n = len(re.findall(r"^\s*print\(", text, re.M))
        hits["`print` calls in non-entry-point modules"].append(f"{path} ({n})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--max-file-lines", type=int, default=500)
    ap.add_argument("--max-func-lines", type=int, default=60)
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to a legacy code page
    root = Path(args.root).resolve()
    files = tracked_files(root)
    hits = defaultdict(list)
    func_hashes = defaultdict(list)

    for rel in files:
        p = root / rel
        if JUNK.search(rel):
            hits["Tracked junk (should be .gitignored)"].append(rel)
            continue
        if STRAY.search(rel.rsplit("/", 1)[-1]) or STRAY.search(rel):
            hits["Stray / versioned / backup-looking file names"].append(rel)
        try:
            size = p.stat().st_size
        except OSError:
            continue
        if size > 5 * 1024 * 1024:
            hits["Tracked files over 5 MB"].append(f"{rel} ({size // (1024 * 1024)} MB)")
        if p.suffix.lower() not in TEXT_EXT:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        if len(lines) > args.max_file_lines and p.suffix != ".md" and p.suffix != ".json":
            hits[f"Files over {args.max_file_lines} lines"].append(f"{rel} ({len(lines)} lines)")
        if p.suffix in (".md", ".json"):
            continue
        run = 0
        for i, line in enumerate(lines, 1):
            s = line.strip()
            if p.suffix == ".py" and s.startswith("#"):
                if NARRATION.search(s):
                    hits["Narration-style comments"].append(f"{rel}:{i} {s[:70]}")
                if BANNER.match(s):
                    hits["Banner separator comments"].append(f"{rel}:{i}")
                if looks_like_code(s):
                    run += 1
                    if run == 2:
                        hits["Commented-out code"].append(f"{rel}:{i - 1}")
                else:
                    run = 0
            else:
                run = 0
            if EMOJI.search(line):
                hits["Emoji in code/config"].append(f"{rel}:{i} {s[:60]}")
            if ABS_PATH.search(line):
                hits["Hardcoded absolute paths"].append(f"{rel}:{i} {s[:80]}")
            if TODO.search(line):
                hits["TODO/FIXME/HACK"].append(f"{rel}:{i} {s[:70]}")
        if p.suffix == ".py":
            python_checks(rel, text, args, hits, func_hashes)

    for locs in func_hashes.values():
        if len(locs) > 1:
            hits["Identical function bodies (duplication)"].append(" == ".join(locs))

    names = {f.lower() for f in files}
    tops = {f.split("/")[0].lower() for f in files}
    missing = [n for n, ok in [
        ("README.md", any(n.startswith("readme") for n in names if "/" not in n)),
        ("LICENSE", any(n.startswith(("license", "licence", "copying")) for n in names if "/" not in n)),
        (".gitignore", ".gitignore" in names),
        ("dependency file (requirements.txt / pyproject.toml / package.json / environment.yml)",
         any(n.endswith(("requirements.txt", "pyproject.toml", "package.json", "environment.yml", "setup.py")) for n in names)),
        ("tests (tests/ or test_*.py)", "tests" in tops or "test" in tops or any(re.search(r"(^|/)test_[^/]*\.py$|_test\.py$", n) for n in names)),
    ] if not ok]
    if missing:
        hits["Missing repo basics"] = missing

    head = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    print(f"# repo-polish mechanical scan\n\nRoot: `{root.name}` at `{head or 'no git'}`, {len(files)} tracked files.\n"
          "Signals only: confirm each by reading the code.\n")
    for title, items in sorted(hits.items(), key=lambda kv: -len(kv[1])):
        print(f"## {title} ({len(items)})")
        for it in items[:40]:
            print(f"- {it}")
        if len(items) > 40:
            print(f"- ... {len(items) - 40} more")
        print()
    if not hits:
        print("No mechanical signals found.")


if __name__ == "__main__":
    main()
