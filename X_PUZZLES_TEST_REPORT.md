# Compact mate-puzzle test report

## Delivered build

`x-player.html` is an additive compact player. The original `index.html` and `index-960.html` have not been changed. The only engine path is `engine/stockfish-19-lite-single.js`, with its matching WASM beside it. Those existing engine files are not included in this ZIP.

## Puzzle verification

27 positions: 5 each for mate in 1, 2, 3, 4 and 5, plus 2 for mate in 6.

All 27 positions are legal, non-terminal at the start, with the stated attacking colour on move. Their mate lengths were independently verified by exhaustive bounded AND/OR search over legal moves: a forced mate exists within N attacking moves, and none exists within N-1. This is a separate validation algorithm, NOT another engine used for play. An actual checkmating example was legally replayed for every shipped position. The player does not use the examples to grade a move or pick a defensive reply.

See `puzzles/verification-report.json` and `tools/verify-puzzles.cjs`. Mate-in-one puzzles are explicitly labelled as derived training continuations of the published source positions.

## Browser checks

179 Chromium interface assertions passed with the actual embedded chess rules and actual puzzle JSON content. This includes legal successful play through all 27 example lines, no intermediate feedback, incorrect-attempt reset, timer continuity, timer freeze on mate, Undo, cancellation of stale replies, page-cache return, in-page promotion, black-side orientation, six difficulty choices, and the fixed Lite engine URL.

Board sizing was checked at 245x245, 245x480, 320x568, 375x667, 480x480, 500x350, 1000x700 and 1920x1080. The board stayed square and within the viewport with no page scrolling. Desktop and narrow screenshots were reviewed.

## Static publishing checks

All 27 individual share pages contain Player Card metadata in the initial HTML, point to their own fixed puzzle IDs, and reference existing JPEG thumbnails rendered from the actual player UI. Six level JSON files have the expected counts. The metadata generator was run successfully. The optional reproducibility verifier was also run successfully on exported mate-in-one and mate-in-three records.

## Important limitations

- The environment blocks external engine downloads and browser navigation to the local test server. Browser tests therefore used simulated Stockfish UCI messages, simulated JSON fetches and a simulated page URL; they did NOT run the Stockfish WASM binary. No simulation or test hooks are present in the delivered player.
- Real Stockfish inference, actual GitHub Pages asset serving, mobile devices and X's live card/sandbox behaviour have NOT been tested here.
- Fixed engine time budgets are practical UI limits, not a guarantee of perfect defence on every possible off-solution line.
- Static Player Card metadata does not guarantee that X will display a playable card. Test an actual post after deployment. No files have been pushed or posted from this session.
- No X handle was supplied. The generated cards do not invent one; add your real attribution using the included generator before your live test.

## Assertion log

- 64 squares
- Only dropdown is puzzle level
- No evaluation bar
- No hint graphics
- Six mate levels
- No feedback before attempt
- Only Stockfish 19 Lite requested
- m1-01 instruction
- m1-01 actual checkmate accepted
- m1-01 timer stops
- m1-02 instruction
- m1-02 actual checkmate accepted
- m1-02 timer stops
- m1-03 instruction
- m1-03 actual checkmate accepted
- m1-03 timer stops
- m1-04 instruction
- m1-04 actual checkmate accepted
- m1-04 timer stops
- m1-05 instruction
- m1-05 actual checkmate accepted
- m1-05 timer stops
- m2-01 instruction
- m2-01 no intermediate feedback 0
- m2-01 actual checkmate accepted
- m2-01 timer stops
- m2-02 instruction
- m2-02 no intermediate feedback 0
- m2-02 actual checkmate accepted
- m2-02 timer stops
- m2-03 instruction
- m2-03 no intermediate feedback 0
- m2-03 actual checkmate accepted
- m2-03 timer stops
- m2-04 instruction
- m2-04 no intermediate feedback 0
- m2-04 actual checkmate accepted
- m2-04 timer stops
- m2-05 instruction
- m2-05 no intermediate feedback 0
- m2-05 actual checkmate accepted
- m2-05 timer stops
- m3-01 instruction
- m3-01 no intermediate feedback 0
- m3-01 no intermediate feedback 2
- m3-01 actual checkmate accepted
- m3-01 timer stops
- m3-02 instruction
- m3-02 no intermediate feedback 0
- m3-02 no intermediate feedback 2
- m3-02 actual checkmate accepted
- m3-02 timer stops
- m3-03 instruction
- m3-03 no intermediate feedback 0
- m3-03 no intermediate feedback 2
- m3-03 actual checkmate accepted
- m3-03 timer stops
- m3-04 instruction
- m3-04 no intermediate feedback 0
- m3-04 actual checkmate accepted
- m3-04 timer stops
- m3-05 instruction
- m3-05 no intermediate feedback 0
- m3-05 actual checkmate accepted
- m3-05 timer stops
- m4-01 instruction
- m4-01 no intermediate feedback 0
- m4-01 no intermediate feedback 2
- m4-01 actual checkmate accepted
- m4-01 timer stops
- m4-02 instruction
- m4-02 no intermediate feedback 0
- m4-02 no intermediate feedback 2
- m4-02 no intermediate feedback 4
- m4-02 actual checkmate accepted
- m4-02 timer stops
- m4-03 instruction
- m4-03 no intermediate feedback 0
- m4-03 actual checkmate accepted
- m4-03 timer stops
- m4-04 instruction
- m4-04 no intermediate feedback 0
- m4-04 actual checkmate accepted
- m4-04 timer stops
- m4-05 instruction
- m4-05 no intermediate feedback 0
- m4-05 no intermediate feedback 2
- m4-05 no intermediate feedback 4
- m4-05 actual checkmate accepted
- m4-05 timer stops
- m5-01 instruction
- m5-01 no intermediate feedback 0
- m5-01 no intermediate feedback 2
- m5-01 no intermediate feedback 4
- m5-01 actual checkmate accepted
- m5-01 timer stops
- m5-02 instruction
- m5-02 no intermediate feedback 0
- m5-02 no intermediate feedback 2
- m5-02 no intermediate feedback 4
- m5-02 actual checkmate accepted
- m5-02 timer stops
- m5-03 instruction
- m5-03 no intermediate feedback 0
- m5-03 no intermediate feedback 2
- m5-03 no intermediate feedback 4
- m5-03 no intermediate feedback 6
- m5-03 actual checkmate accepted
- m5-03 timer stops
- m5-04 instruction
- m5-04 no intermediate feedback 0
- m5-04 no intermediate feedback 2
- m5-04 actual checkmate accepted
- m5-04 timer stops
- m5-05 instruction
- m5-05 no intermediate feedback 0
- m5-05 no intermediate feedback 2
- m5-05 no intermediate feedback 4
- m5-05 no intermediate feedback 6
- m5-05 actual checkmate accepted
- m5-05 timer stops
- m6-01 instruction
- m6-01 no intermediate feedback 0
- m6-01 no intermediate feedback 2
- m6-01 no intermediate feedback 4
- m6-01 no intermediate feedback 6
- m6-01 no intermediate feedback 8
- m6-01 actual checkmate accepted
- m6-01 timer stops
- m6-02 instruction
- m6-02 no intermediate feedback 0
- m6-02 no intermediate feedback 2
- m6-02 actual checkmate accepted
- m6-02 timer stops
- Wrong final move shows Try again
- Failed attempt resets automatically
- Failure does not reset timer
- All pieces restored on reset
- Undo reverses user move and defender reply
- Undo disabled at starting position
- Undo cancels pending defence without stale move
- Undo returns control to attacker
- Returning from page cache resumes the defending engine
- Undo remains correct after page-cache resume
- Level change cancels pending defence
- Level selection loads new puzzle
- Next loads a different same-level puzzle
- Non-solution first move is not graded early
- Promotion chooser opens inside the board
- No promotion feedback before choice
- Chosen promotion can finish checkmate
- Timer remains frozen beyond a full second after mate
- Undo after mate resumes elapsed clock
- Black puzzle flips board automatically
- 245x245 board stays square
- 245x245 board fits
- 245x245 no scrolling
- 245x480 board stays square
- 245x480 board fits
- 245x480 no scrolling
- 320x568 board stays square
- 320x568 board fits
- 320x568 no scrolling
- 375x667 board stays square
- 375x667 board fits
- 375x667 no scrolling
- 480x480 board stays square
- 480x480 board fits
- 480x480 no scrolling
- 500x350 board stays square
- 500x350 board fits
- 500x350 no scrolling
- 1000x700 board stays square
- 1000x700 board fits
- 1000x700 no scrolling
- 1920x1080 board stays square
- 1920x1080 board fits
- 1920x1080 no scrolling
- No browser JavaScript errors: []
