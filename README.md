# Chess Teacher: Stockfish Lite, Full Stockfish and Maia-3

This update extends the existing auto-fit/autosave chess teacher. The application
code is still contained in `index.html`. No cloud engine, API key, Node.js, npm,
React, GPU or compilation step is needed for normal use. The external runtime,
model and rules assets are downloaded once by the included Python script.

**Package contents:** source HTML, downloader, Windows launcher, this README,
third-party notices, and a test report. **The ZIP does not contain the third-party
Stockfish/ONNX binaries or chess.js.** Do not replace working engine files with
empty folders or assume the small ZIP includes the models.

## Update your working folder

Back up your existing `index.html`. Copy this package's contents into the same
folder, replacing that HTML and keeping the existing `vendor` and `engine`
folders. Do not change the serving URL or browser profile if you want your saved
game to appear: browser storage is separate for different origins/site folders.
Existing version-1 game saves are supported; a missing saved engine choice means
Stockfish Lite. The new engine selection is saved alongside your game/settings.

Run the installer with an internet connection. On Windows, double-click
`Install-models-Windows.cmd`, or run:

```powershell
py -3 install-models.py
```

In WSL/Linux:

```bash
python3 install-models.py
```

The script uses only Python 3.9+ standard-library modules. It downloads the base
files if needed, the Full Stockfish pair, the Maia-3 model and mapping, the matching
ONNX Runtime Web files, and licence notices. It writes only into this folder.
Existing valid files are retained; a replacement is installed only after checks.
Stockfish release SHA-256 hashes are verified. Other assets are pinned to a source
commit and structurally checked; their hashes are recorded in `download-lock.json`
for later local verification, not claimed as independent publisher signatures.

Optional commands:

```text
py -3 install-models.py --only full
py -3 install-models.py --only maia
py -3 install-models.py --check
py -3 install-models.py --force
```

`--check` is offline. `--force` re-downloads; it does not remove a working file until
a replacement passes validation. Base files and notices are included in all modes.
A failed download is reported and the script exits with a non-zero status. Correct
the connection and rerun; already completed downloads are retained.

Use the same local server/address you used before, then Ctrl+F5. For a fresh setup:

```powershell
py -3 -m http.server 8765 --bind 127.0.0.1
```

Or `python3 -m http.server 8765 --bind 127.0.0.1` in WSL/Linux. Visit
`http://127.0.0.1:8765`. Do not double-click `index.html` to use a `file://` URL.
The server does not run chess analysis; the visitor's browser runs the engines.

## Files after installation

```text
index.html
install-models.py
Install-models-Windows.cmd
README.md
THIRD_PARTY_NOTICES.md
TEST_REPORT.md
.nojekyll
vendor/
  chess.js
  ort/
    ort.wasm.min.js
    ort-wasm-simd-threaded.mjs
    ort-wasm-simd-threaded.wasm
engine/
  stockfish-19-lite-single.js
  stockfish-19-lite-single.wasm
  stockfish-19-single.js
  stockfish-19-single.wasm
models/
  maia3/
    maia3_simplified.onnx
    all_moves.json
licenses/
  ... downloaded copyright/licence notices ...
download-lock.json
```

All these runtime URLs are local/relative to the app folder. There are no external
inference or CDN calls during play. A local installation works without internet
after installation. GitHub Pages still needs internet to load the site/files;
this update does not add a service worker or promise offline Pages caching.

## Engine dropdown and mid-game switching

| Selection | Opponent in Play computer | Teacher / best-move hints / bar |
|---|---|---|
| Stockfish Lite | Existing lite single-threaded Stockfish 19 | Same engine |
| Stockfish Full | Full-network single-threaded Stockfish 19 | Same engine |
| Maia-3 (human-like) | Official CSSLab Maia-3 browser ONNX export | Stockfish Lite |

Switch at any point. The position, turn, history and Undo are preserved. A pending
reply and old evaluation are invalidated, the old engine resources are released,
and fresh analysis starts. The computer replies only if it is still the top
colour's turn. No engine is silently substituted when files are missing.

Full Stockfish is a **larger network/build, not an unlimited-search mode**. Your
rating preset, node/depth ceiling and thinking cap still apply. Both Stockfish
builds intentionally use a single thread for ordinary static hosting.

In Practice, you move both sides. Selecting Full changes the analysis engine;
selecting Maia keeps Stockfish Lite analysis. Maia's own network is loaded lazily
when a computer turn actually needs a prediction. The selected engine can be
changed even if a large model is still loading.

## Allow Blunder

**Stockfish, either build:** checked keeps the existing weighted top-four draw,
rank bonuses, weighting options and mate safeguards. Unchecked follows the final
Stockfish best move for the current search budget, without intentional randomness.

**Maia:** checked samples Maia's probability distribution over **all legal moves**.
Unchecked takes its highest-probability human move deterministically. This means
"most likely human move", not "objectively strongest move". It may still blunder.
The app does not add Stockfish rank bonuses, filter mates, or replace Maia's policy
with the Stockfish top four; doing so would change what Maia is modelling.

Maia likelihoods are shown in a separate panel. The board's green/yellow squares,
dotted lines, objective best-move list and evaluation bar are always Stockfish
analysis. Disabling the computer colour's hints also hides its Maia probabilities.
The top four Maia probabilities can total less than 100%, because other legal moves
have probability too. They are not winning chances.

## Strength and think limit

For Stockfish, the number retains the existing uncalibrated training-budget
meaning. For Maia, it is passed as both `elo_self` and `elo_oppo` to the model's
continuous float inputs. Maia is trained to predict human play; neither this input
nor the budget label guarantees an actual FIDE rating, particularly at low/extreme
values. There is no local FIDE calibration study for this app.

In Maia mode, the think-limit label becomes **Teacher think limit**. It caps the
Stockfish teacher, not Maia's single neural-network inference. The reply waits for
both a current teacher result and Maia's current legal-move distribution. There is
a startup timeout and a separate inference watchdog; these are reliability limits,
not playing-strength controls.

## Maia version / compatibility

The installer pins the official frontend to:

`a6e52f5c811ee18863cb2f0e81f2433a5b9905de`

It fetches `public/maia3/maia3_simplified.onnx`, the matching 4,352-move mapping,
and the three matching `public/ort/` runtime files (ONNX Runtime Web 1.23.0).
The worker uses `tokens: float32 [1,64,12]`, `elo_self: float32 [1]`,
`elo_oppo: float32 [1]`, and reads `logits_move`. Black positions are reflected
rank-wise with colours swapped; legal moves are mapped back, including promotions.
A stable softmax is applied only to legal moves. A missing mapping, bad score,
unexpected model interface, or invalid move causes an error rather than a guessed
replacement move. The chosen move is checked against the current rules-library
legal moves immediately before being played.

Do not substitute a native Maia `.pt` file, Maia-2 ONNX model, or arbitrary newer
Maia-3 export: interfaces and move mappings can differ. This integration targets
the exact official browser export listed above, not every member of the Maia family.

## GitHub Pages

Upload the resulting runtime folders and readable application source, not just
the ZIP or the HTML. Keep `.nojekyll`, the downloaded notices and source links.
Full Stockfish's WASM is about **94.6 MiB** and this Maia export is about **43.6 MiB**.
The runtime has its own download too. The large files are above GitHub's 25 MiB
browser-upload limit; use Git/GitHub Desktop for the repository, or a Pages build
that downloads the pinned files before deployment. The two model files are below
the normal 100 MiB Git file limit. Do not upload Git LFS pointer text in place of
the actual runtime files.

Both engines run with one WASM thread, without requiring COOP/COEP headers or a GPU.
Maia runs in a Blob worker whose application code is embedded in `index.html`.
A custom Content Security Policy would need to allow that worker and WASM execution.
Ordinary browser memory limits still apply, especially on phones.

## Troubleshooting / real-engine check

First choose Stockfish Lite and make a move; then Full; then Maia in Play computer.
Use Ctrl+F5 after replacing files. Maia should load on a computer turn, show its
own loading status and then play. Full's first download can be noticeably larger.
If a model fails, the game is not reset: use Retry engine or choose a different
engine. The browser developer console / Network panel identifies 404s.

Run `install-models.py --check` to detect missing/changed assets. A successfully
served 404 fallback page is not a model; the worker/installer reject HTML responses.
An incomplete or Git LFS pointer file also fails validation. No automatic remote
API or different engine is used as a hidden fallback.

Read `TEST_REPORT.md` before treating this as production-tested. The real Stockfish
WASM and ONNX files could not be downloaded in the development environment, so
actual inference, real chess.js compatibility and a live Pages deployment still
need the local smoke check described above.

## Sources

- Stockfish.js release and matching hashes: https://github.com/nmrugg/stockfish.js/releases/tag/v19.0.1
- Engine build variants: https://github.com/nmrugg/stockfish.js/blob/v19.0.1/README.md
- Official Maia browser export, mapping and worker: https://github.com/CSSLab/maia-platform-frontend/tree/a6e52f5c811ee18863cb2f0e81f2433a5b9905de
- Official Maia-3 implementation: https://github.com/CSSLab/maia3
- ONNX Runtime configuration: https://onnxruntime.ai/docs/tutorials/web/env-flags-and-session-options.html
- GitHub large-file limits: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
