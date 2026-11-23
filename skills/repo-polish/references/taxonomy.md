# What to look for

Each item: the smell, why it costs something, the usual fix. Fix only with evidence, and only if behavior is preserved.

## 1. AI residue (high-volume generated code)

| Smell | Cost | Fix |
|---|---|---|
| Narration comments: `# Step 1: load the data`, `# Now we iterate over...`, `# This function calculates...`, `# Let's ...` | Noise; repeats the code; reads as generated | Delete. Keep only comments that explain *why* |
| Emoji or marketing tone in code, logs or comments (`✅ Done!`, `🚀 Starting server`) | Unprofessional; breaks some terminals/log parsers | Plain text |
| Banner separators (`# ======== SECTION ========`) in short files | Visual noise | Delete, or split the file if sections are real modules |
| Docstrings that restate the signature (`"""Takes x and returns y."""`) | Noise; drifts out of sync | Delete, or replace with the non-obvious part (units, invariants, side effects) |
| Commented-out code blocks | Dead weight; nobody knows if it matters | Delete (git keeps history) |
| One-implementation abstractions: base classes/interfaces/factories with a single concrete user, "manager"/"handler"/"helper" wrappers that only forward | Indirection without benefit | Inline into the single user |
| Duplicated logic that drifted: same function copy-pasted in `edge/`, `fog/`, `cloud/` with small edits | Fixes land in one copy only | One canonical version in a shared module; callers import it. Check every copy's differences first: a difference may be a bug or deliberate |
| Defensive code for impossible cases: `if x is None` after a constructor that never returns None, `isinstance` checks on internal values | Hides real errors, adds branches | Remove when provably impossible |
| Obsolete flags, aliases, compatibility paths, `v2`/`new_`/`_old` twins | Two ways to do one thing | Keep the one in use; delete the other after grep proves no use |
| `print` debugging left in library code | Noisy output | Remove, or use `logging` where output is wanted |

## 2. Error handling

| Smell | Fix |
|---|---|
| `except:` / `except Exception: pass` / `except Exception as e: print(e)` and continue | Catch the specific exception; let unexpected ones raise; log with context where swallowing is intended (and say why in a comment) |
| Silent fallbacks (`return {}` / default value on any error) | Fail loudly, or make the fallback explicit and logged |
| Inconsistent error style across modules (exceptions here, return codes there) | Pick the project's dominant style |

## 3. Structure

- **God files / god functions**: modules over ~500 lines or functions over ~60 lines doing several phases. Split by phase into named helpers in the same module first; move to new modules only with a pin inventory.
- **Misplaced code**: shared utilities living inside one component; config parsing scattered in many files; protocol/message definitions duplicated per node type.
- **Flat dump**: dozens of scripts in the repo root. Group into a package (`src/<pkg>/` or `<pkg>/`), `scripts/`, `tests/`, `configs/`, `docs/` only when the project is big enough to need it.
- **Entry points**: one clear way to run each component (`python -m pkg.edge`, a `main()` guarded by `if __name__ == "__main__":`). Module-level side effects (training starts on import) are a defect.
- **Dependency direction**: shared code must not import from a specific component.

## 4. Naming and consistency

- One naming style per language (`snake_case` in Python, no `camelCase` drift).
- Names say what, not how (`aggregate_weights`, not `do_process2`).
- Numbered or versioned names (`model_final_v3.py`, `test2.py`, `utils_new.py`) → one real name.
- Magic numbers used in several places → named constants or config.

## 5. Configuration and secrets

- Hardcoded absolute paths (`C:\Users\...`, `/home/<user>/...`), IPs, ports scattered in code → config file or env vars, with defaults.
- Secrets, tokens, API keys, `.env` files in git → STOP and tell the user immediately (needs key rotation, not just deletion; history rewrite is the user's call).
- Duplicate config (same value in Python, YAML and Dockerfile) → one source of truth.

## 6. Repository hygiene

- Tracked junk: `__pycache__/`, `*.pyc`, `.ipynb_checkpoints/`, `.DS_Store`, `*.log`, `.idea/` (unless shared on purpose), virtualenvs, `node_modules/`, model checkpoints and datasets over a few MB → `git rm --cached` + `.gitignore`. Large files: mention Git LFS or external storage; history rewrite only on the user's request.
- Missing basics: `README.md`, `LICENSE`, `.gitignore`, dependency file (`requirements.txt` / `pyproject.toml` with pinned or bounded versions), a way to run tests.
- Unused dependencies in `requirements.txt` (grep for imports first; some are imported lazily or by name in config).
- Notebooks with huge outputs committed: clear outputs, or move exploration notebooks to `notebooks/`.

## 7. Comments that should stay or be added

Keep or add comments that a reader cannot get from the code:
- **Why** a non-obvious choice was made (algorithm, constant, workaround and its issue link).
- **Units and shapes** (`# seconds`, `# (batch, channels, H, W)`).
- **Invariants and side effects** of public functions (docstring).
- **References**: paper/equation numbers for research code (`# Eq. 7 in <paper>`).

Rule of thumb: if deleting the comment loses no information, delete it. If it explains something the code cannot, keep it and make it accurate.

## Not findings

- Style preferences the project already follows consistently.
- Code that is unusual but deliberate (document it as `Deliberate`).
- "Could be more abstract": generality nobody needs is not an improvement.
