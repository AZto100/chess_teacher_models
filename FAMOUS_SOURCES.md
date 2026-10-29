# Famous Games — sources and validation

100 distinct source games, reused across six categories: 600 puzzles. The 1800–2026 selection window currently contains games dated 1834–2026. These are curated anthology games, selected famous-player brilliancies, and named 2026 highlights; they are not an arbitrary event dump. Not every game has a universally recognised nickname.

Selections come from Chess Classics; the Immortal Games anthology; Richard Réti’s Masters of the Chessboard; Bobby Fischer’s My 60 Memorable Games; Mikhail Tal’s The Life and Games; Great Masters; and source-selected modern brilliancies. Exact source membership and links appear in famous-games.csv. No book/article commentary is reproduced.

Important: many famous games ended in resignation. Their played moves are preserved in famous-source-games.pgn. Stockfish continuations after the recorded end are stored separately in famous-game-manifest.json; they are hypothetical training moves, not historical game moves. A puzzle whose starting board is beyond the recorded end is visibly marked “Training continuation”. tournamentLine contains only recorded moves from the puzzle position and is empty for a wholly derived starting position. After the recorded line ends, or after the player deviates, Stockfish supplies the defence. exampleLine may include hypothetical moves and is used for validation, never as a required solution.

| Category | Puzzles | Engine mate bounds (moves: count) | Derived starting positions |
|---|---:|---|---:|
| 1 or fewer | 100 | 1: 100 | 88 |
| 2 or fewer | 100 | 1: 2, 2: 98 | 83 |
| 3 or fewer | 100 | 1: 2, 2: 8, 3: 90 | 80 |
| 4 or fewer | 100 | 1: 2, 2: 8, 3: 6, 4: 84 | 78 |
| 5 or fewer | 100 | 1: 2, 2: 8, 3: 4, 4: 17, 5: 69 | 78 |
| 6 or fewer | 100 | 1: 2, 2: 8, 3: 4, 4: 12, 5: 15, 6: 59 | 75 |

A category permits mate in X or fewer moves, as requested. Every source game appears once per category, with no duplicated game within a category. All example lines were legally replayed through checkmate. Non-trivial mate bounds were checked with Stockfish 16 at 200,000 and 1,000,000 nodes; shortest-mate claims are not exhaustive proofs. Browser defence continues to use your existing Stockfish 19 Lite files.

## Date distribution

- 1800–1849: 3 games.
- 1850–1899: 15 games.
- 1900–1949: 25 games.
- 1950–1979: 28 games.
- 1980–1999: 9 games.
- 2000–2026: 20 games.
