# Test report: multi-engine Chess Teacher

## Scope and limitation

This is source-level and simulated-dependency validation, **not a real-engine
end-to-end certification**. The development environment could read upstream source
pages but could not download the Stockfish, chess.js, ONNX Runtime or model files
for execution. No live GitHub Pages deployment was made. The supplied source ZIP
therefore contains no engine binaries and no substitute chess rules library.

The 33 Chromium checks executed the application's interface and coordination code
with a test-only rules fixture, simulated Stockfish UCI messages, synthetic ONNX
logits and a storage substitute. Real Blob workers were exercised, but the runtime
imports/fetches were replaced in the in-memory test copy. Normal network navigation
was restricted in this environment; these checks do not demonstrate that the real
WASM files, model or site-relative URLs load successfully on a deployed site.
Neither fixtures nor instrumented HTML are included in the deliverable.

## Results

- Application JavaScript: `node --check` passed.
- Python downloader: compilation and `--help` passed.
- 33 Chromium interface / coordination checks passed.
- 12 Maia position-encoding and move-orientation unit checks passed.
- 10 offline downloader structural/hash validation checks passed.
- Offline `--check --only full` correctly reported absent files and returned exit
  status 1, without creating or downloading model files.

The 33 browser checks cover the standard board, saved model/rating/history, the
correct full-engine path, mid-turn switching, cancellation after New/Undo/Flip,
Maia's deterministic and sampled choices, separation of Maia likelihoods from
Stockfish hints, both-colour behaviour, hidden-hint handling, v1 save migration,
missing-model errors without silent fallback, and retries retaining the game.
Layout checks covered 1920x1080, 1366x768, 390x844 and 844x390 viewports. No
unexpected page JavaScript errors occurred in that suite. The bottom-colour test
checks seat assignment; this is not a replacement for a full legal-move audit.

The 12 encoding checks cover 768 float32 entries, the starting 32 pieces, all 12
piece channels, rank orientation, Black's colour swap, representative moved pieces,
en-passant target handling, castling/promotion UCI reflection, reflection symmetry
and rejection of malformed FEN input. They do not test the quality of Maia's real
predictions.

The 10 installer checks accept the expected WASM header/digest, ES-module marker
and ONNX Runtime version, and reject an incorrect digest, HTML, a Git LFS pointer,
invalid WASM header, too-small ONNX file, wrong runtime version and wrong move
mapping. These are synthetic local files, not successful upstream downloads.

`preview.png` is a UI preview using simulated scores, not an engine benchmark or
evidence of a completed real Stockfish search.

## Required real-dependency smoke test

After running the installer on your own machine, use the existing local server
and application address. Check the following before publishing widely:

1. `install-models.py --check` passes for all installed assets.
2. Stockfish Lite starts, gives four legal hints and replies in Play computer.
3. Switching to Full keeps the game and produces a new Full analysis/reply.
4. Switching to Maia during a pending reply prevents the old engine from moving.
5. Maia loads its model, displays legal-move likelihoods and replies; test with
   Allow Blunder on and off. The off setting means most likely human move.
6. Flip the board and test Maia as White, then try castling and a promotion position
   reached through legal play. Ensure Undo and reload preserve the game.
7. Check browser Network/Console for real runtime errors, wrong MIME types or 404s.
8. Repeat using the actual GitHub Pages project URL and a mobile browser if those
   will be supported. First-load time and memory use depend on the device.

Strength labels are not FIDE-calibrated. No actual-engine performance, rating,
move-quality or mobile-memory benchmark is claimed.
