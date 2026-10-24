# Compact mate puzzles for a website or experimental X Player Card

## Add to your existing repository

Copy the CONTENTS of this folder into the root of your existing `chess_teacher_models` repository. Do not replace `index.html` or `index-960.html`.

The new entry point is `x-player.html`. Its application logic, solid SVG pieces and chess rules are all embedded in the HTML. The ONLY opponent/analysis engine is Stockfish 19 Lite, single-threaded. There is no engine selector, Maia, full Stockfish, voice runtime, rating selector or evaluation bar in this edition.

Retain these existing files, with these exact names:

```
engine/stockfish-19-lite-single.js
engine/stockfish-19-lite-single.wasm
```

The matching engine JS and WASM files are NOT bundled in this update. No new engine download is required when they are already present in your repository. The original project's version was Stockfish.js 19.0.1; do not mix the loader and WASM from different releases. Runtime files are published by the engine project at:
https://github.com/nmrugg/stockfish.js/releases/tag/v19.0.1

All application asset URLs are relative, so ordinary GitHub Pages repository subpaths work. Open via HTTPS or a local HTTP server, not `file://`.

## Files to add

```
x-player.html                 Clean player; all application JS/CSS/rules included
x-share.html                  Default fixed-puzzle share page (m1-01)
x-puzzles.html                Catalogue of the individual share links
x-posts/m1-01.html ...         One static share page for each of the 27 puzzles
puzzles/mate-1.json ... -6.json
puzzles/verification-report.json
images/m1-01.jpg ...          Matching card thumbnails of the actual board
PUZZLE_SOURCES.md
X_PUZZLES_NOTICES.md
X_PUZZLES_TEST_REPORT.md
tools/build-x-cards.py        Optional metadata regeneration
tools/verify-puzzles.cjs     Optional offline puzzle verifier (Node.js)
```

Keep your original third-party source and licence material when publishing.

## Playing

The instruction states the attacking colour and the requested mate: for example, **White to move. Mate in 3!** The attacking colour is always at the bottom. Select a piece, then a destination; mouse, touch and keyboard buttons work. There are no legal-destination highlights, best-move colours, arrows, evaluations, move lists or tactical comments. A selection outline only identifies the piece you clicked.

Stockfish 19 Lite plays the defending side, with skill reduction and random/blunder selection disabled. It searches one best line, up to depth 28 and a fixed time budget of 0.9-2.4 seconds for levels requiring a reply. On a slow device this is a bounded engine search, not a promise of mathematically perfect defence on every off-solution branch. Stockfish must actually return a legal move; errors never silently substitute a random move or another engine.

The sole dropdown chooses **Mate in 1-6**. **Next** cycles through that level, returning to its first puzzle after the last one. Selecting another level or pressing Next resets the timer for the new puzzle.

### Attempt rules

- No correct/wrong judgement is displayed after intermediate moves. Any legal attacking move is allowed; the engine responds normally.
- Actual checkmate by the attacking colour within the allowed number of attacking moves shows **Correct!** and stops the timer. A faster mate is also accepted; a weaker defence may allow it.
- Making the Nth attacking move without mate, being checkmated, or reaching a drawn/terminal position shows **Try again**. After a short visible interval the initial position returns. The elapsed time continues throughout.
- **Undo** removes the player's latest move plus the defensive reply, or cancels a pending reply. This returns control to the player, not the defender. Undo does not erase elapsed time. Undo after success resumes the clock from the stopped value.
- Promotions use in-page Queen/Rook/Bishop/Knight buttons, not `prompt()` or `alert()`.

The timer starts when the puzzle and engine are ready. It includes thinking, computer replies, retry intervals, and time while the tab is hidden. The application does not save puzzle attempts to the full app's localStorage: each new post/load starts its own preset puzzle and timer. All timing and puzzle data are client-side; this is a practice tool, not tamper-proof contest scoring.

## Puzzles and verification

27 positions: five each for levels 1, 2, 3, 4 and 5; two for level 6.

Levels 2-6 are published positions from games of Anderssen, Morphy, Lasker, Capablanca, Tarjan, Riazantsev and Vladimirov, as compiled by Bill Harvey. Level 1 uses verified continuations from the level-2 positions; those continuation moves are not claimed to be moves played in the original games. The Immortal Game and Evergreen Game positions are included. Full provenance is in `PUZZLE_SOURCES.md` and each JSON record.

Each shipped mate length was independently checked by an exhaustive bounded legal-move AND/OR search: at least one attacking strategy forces mate within N moves against every legal defence, and no strategy forces mate within N-1. This verification used the embedded rules, not Stockfish inference. The optional `exampleLine` in JSON is a legal example, NOT the only accepted solution and not necessarily the defender's longest-resisting variation. No example lines are read by the live opponent or outcome checker.

To reproduce a proof with Node.js, for example:

```
node tools/verify-puzzles.cjs m3-01
node tools/verify-puzzles.cjs m6-01 180000
```

The optional second argument is the time limit in milliseconds. With no arguments the verifier checks all 27 positions. Longer mate proofs can take significant CPU time. A budget expiration is reported as incomplete, never as a successful proof.

## Fixed puzzle for each X post

Post the **individual share-page URL**, not a query string on `x-share.html`:

```
https://azto100.github.io/chess_teacher_models/x-posts/m3-01.html
```

Its initial HTML contains a Player Card pointing to:

```
https://azto100.github.io/chess_teacher_models/x-player.html?p=m3-01
```

Every share page has its own initial puzzle and actual starting-position image. IDs are m1-01 through m5-05 and m6-01 through m6-02. See `x-puzzles.html` for the list. These are future deployment addresses until you copy and push the files.

Card URLs are preconfigured for the public site address you supplied. No X handle was provided, so no identity has been invented. To include your real X account attribution, regenerate the metadata from the repository folder:

```
py -3 tools\build-x-cards.py --handle @YourActualHandle
```

For a different site URL:

```
py -3 tools\build-x-cards.py --site https://YOUR-USER.github.io/YOUR-REPO/ --handle @YourActualHandle
```

Both commands use Python's standard library only. They do not change the puzzles, player logic or existing chess teacher. Commit the regenerated pages after running them.

The generated player dimensions are 480 x 480. The board itself fits both available width and height and is tested as narrow as 245 pixels. Static metadata and an iframe-ready page do NOT guarantee that X will display an interactive card. Test one real post after deployment. If X shows an ordinary link/card instead, opening the share page still gives the puzzle in the browser. This package has not been published to or tested inside a live X post.

There is no microphone access, SharedArrayBuffer requirement, cross-origin-isolation helper, login or modal browser dialog. The single-threaded Stockfish build is deliberately used. Do not apply an X-Frame-Options or CSP frame-ancestors policy that prevents X from framing the player.

## Windows local test and push

From your repository root:

```
py -3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/x-player.html?p=m3-01`, or open `x-puzzles.html` on the same server. Your existing engine files must be present.

After checking the board locally, use your usual Git workflow. Review all staged changes before pushing. Example for an existing `main` branch:

```
git add x-player.html x-share.html x-puzzles.html x-posts puzzles images tools/build-x-cards.py tools/verify-puzzles.cjs PUZZLE_SOURCES.md X_PUZZLES_README.md X_PUZZLES_NOTICES.md X_PUZZLES_TEST_REPORT.md
git diff --cached --stat
git commit -m "Add compact Stockfish Lite mate puzzles and X share pages"
git pull --rebase origin main && git push origin main
```

Do not upload just the ZIP or just the player HTML. The JSON files, share pages and thumbnails must also be published.
