# Source and third-party notices

## Application

The new puzzle interface, styling, scripts and new source code in this package are offered under GPL-3.0-or-later, consistent with the embedded chess rules. The editable HTML and helper scripts are the source. Preserve applicable upstream copyright and licence notices. The complete GPL text and upstream notices are also embedded in the HTML inherited from your existing app.

## Embedded chess rules

The player reuses the chessops 0.15.0 source and Chess960 adapter already embedded in your `index-960.html`, without replacing it with a new chess engine. chessops is a legal-position/move library, not the computer opponent.

- chessops: copyright Niklas Fiekas; GPL-3.0-or-later.
- Source: https://github.com/niklasf/chessops/tree/v0.15.0
- Embedded @badrap/result dependency: MIT; notice retained in HTML.
- The adapter is reused from your existing file. All puzzle positions in this set are standard-chess positions. Its king-to-rook castling notation is matched by the UCI_Chess960 engine option.

## Stockfish 19 Lite

The only opponent engine is your existing single-threaded Stockfish.js 19 Lite pair. No compiled engine binaries are included in this update.

- Engine: GPLv3; retain the existing notices and exact corresponding-source access when distributing the JS/WASM files.
- Wrapper/source release: https://github.com/nmrugg/stockfish.js/tree/v19.0.1
- Published binaries: https://github.com/nmrugg/stockfish.js/releases/tag/v19.0.1
- Underlying engine: https://github.com/official-stockfish/Stockfish

Keep your repository's existing third-party licence/source materials. A free download price does not remove source/licence obligations.

## Position data

Source attribution is in `PUZZLE_SOURCES.md` and every puzzle JSON record. The original game positions were compiled by Bill Harvey at https://www.wtharvey.com/ . This subset reproduces factual board positions, game identifiers and coordinate moves, not the site's diagrams or explanatory prose. Mate-in-one records are explicitly identified as training continuations, rather than asserted historical game continuations.

## Piece artwork and thumbnails

Solid SVG pieces are reused from your existing chess teacher. The included JPEG card thumbnails are fresh renders of this puzzle interface, not scraped diagrams.
