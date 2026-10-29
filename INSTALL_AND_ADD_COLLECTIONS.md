# Install the Famous Games add-on

1. Replace your existing x-player.html with the separately supplied updated x-player.html.
2. Extract this ZIP into the same website folder. It adds puzzles/collections.json and puzzles/famous/mate-1.json through mate-6.json. It does not contain or overwrite your existing puzzles/mate-*.json files, x-puzzles.html, engine/ or x-posts/.
3. Open x-player.html. Choose Famous Games in the collection dropdown. Your old puzzles are under Tournament Games.

Direct link: x-player.html?c=famous&p=m3-01
Existing x-player.html?p=m3-01 links still open the original tournament collection. Copying the player URL after switching collections preserves both the collection and puzzle ID.

Famous Games contains 100 distinct source games per category. The same 100 source games are reused across all six categories. Many starts are clearly marked engine training continuations after resignation: see FAMOUS_SOURCES.md and the complete recorded PGNs. No hypothetical move is represented as a recorded game move.

# Add future collections

Make a new folder, for example puzzles/tata-2026/, containing mate-1.json through mate-6.json in the same puzzle-pack format. Packs need not all have 100 entries. Their level field and each puzzle's mate field must match the category. IDs are unique within a pack and follow m1-01 ... m6-100, including larger numbers. The same IDs can occur in different collections because collection IDs namespace links and the cache.

Add an entry to the collections array in puzzles/collections.json:

    {"id":"tata-2026","name":"Tata Steel 2026","basePath":"puzzles/tata-2026/"}

Use the same scheme for a player or year, e.g. id fischer or classics-1850s. Paths are relative to x-player.html. Folder names and IDs are examples only; the sample collections are not supplied. No HTML changes are required for another collection.

Each puzzle needs id, mate, fen and attacker (w or b). source.game and source.year supply the heading. Set tournamentLine to an array of recorded UCI moves beginning at the starting FEN; leave it empty if no recorded continuation exists. Set source.trainingContinuation to true for starting boards from a hypothetical continuation; the player labels these explicitly. exampleLine can retain a validated sample solution without constraining the user's moves.

The target is actual checkmate in the stated number of attacking moves or fewer. Alternative solutions are accepted. The opponent uses recorded defence while the complete move prefix matches, then Stockfish after deviation or when the historical score runs out. Undoing to the recorded prefix restores historical defence.

Keep the existing engine files. Use a web server, not file://. Static X/Twitter preview cards are not generated for these additional puzzles; use the direct player links.
