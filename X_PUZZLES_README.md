# Mate in X update

Replace x-player.html and x-puzzles.html in your existing site and place all six JSON files in puzzles/. Keep your existing engine/stockfish-19-lite-single.js and its matching WASM files in engine/. The engine files were not attached and are not included in this update. Serve through your existing website or a local HTTP server; do not open the HTML with file://.

There are 100 distinct starting positions per category (600 entries). Positions may recur in different categories. The target is mate in X moves **or fewer**. Higher categories include shorter mates, as requested; see PUZZLE_SOURCES.md for the bounds. Counts do not imply that every category position has an exact shortest mate of X.

The heading now includes both players and the year. The defender follows the original tournament mainline while the complete played history matches it. Once you deviate, Stockfish 19 Lite supplies defensive moves. Undoing back to the recorded prefix restores the recorded defence. A legal checkmate within the move limit is accepted regardless of the line played. There is no early rejection for a different move. An unsuccessful attempt resets with the timer continuing, as before.

The six sets are rebuilt from recorded tournament games. Puzzle IDs are assigned to these new sets; old IDs can therefore now identify different positions. The index links directly to x-player.html?p=m6-100, for example. This update does not create new X/Twitter static Player Card pages; existing x-posts pages and their preview images are not refreshed by this ZIP.

Only puzzle ID support, heading metadata and defence selection changed in x-player.html. The index entries were refreshed. The board, controls, engine selection and outcome rules are unchanged.

Validation: every recorded move was replayed with python-chess and the player's embedded chessops rules, every recorded line ends in actual checkmate within the category move limit, and all 600 starts are playable. Stockfish 16 was used offline with a 1,000,000-node search per non-trivial position to find a mate bound at the initial position; these are bounded engine findings, not exhaustive proofs of shortest mate. Browser defence continues to use your existing Stockfish 19 Lite.
