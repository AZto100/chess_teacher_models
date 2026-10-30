# Exact mate-length correction

Replace x-player.html with the separately supplied updated player. Extract the puzzle ZIP into the website root, replacing both index pages and the supplied JSON files. Keep engine/ and its matching Stockfish 19 Lite JS/WASM files. The existing collection dropdown remains. JSON requests bypass the browser cache so old padded packs are not reused.

## Why the same Capablanca–Spielmann position appeared in several levels

The previous packs treated a category as “mate in X or fewer”. When a source game did not supply a longer mate, the pack builder reused its shorter position to fill the longer categories. Capablanca–Spielmann (1927) had the identical starting FEN in mate-in-3 through mate-in-6. That position is a forced mate in exactly 3, with no forced mate in 2. This was a categorisation/filling issue, not a promotion-count issue.

Now each starting position appears only in its exact shortest forced-mate category. Positions with a shorter forced mate, no proven mate within the category limit, or incomplete validation are not admitted. No category is padded with shorter mates.

## Corrected counts

| Collection | Mate 1 | Mate 2 | Mate 3 | Mate 4 | Mate 5 | Mate 6 |
|---|---:|---:|---:|---:|---:|---:|
| Famous Games | 100 | 100 | 100 | 100 | 100 | 100 |
| Tournament Games | 100 | 100 | 100 | 100 | 63 | 22 |

The Famous Games replacement pool supplies 100 distinct source games in every category. The same game may supply different starting positions at different levels, but the same starting board does not recur in different levels. The smaller original tournament pool does not supply 100 verified longer mates; those categories are deliberately shorter rather than incorrectly labelled.

## Defence and alternative solutions

Checking that one line ends in mate does not prove a forced mate. Each retained start has passed a full legal-move AND/OR search: the attacker has a strategy against every legal defensive reply within N moves, and no strategy can force mate within N−1. A node limit produces UNKNOWN, never a pass; such starts are omitted. Search ordering and transposition caching accelerate the complete bounded check, without engine evaluations or selective move pruning.

The stored defenceLine is independently constructed with a shortest winning attack and longest legal resistance. The player now follows this verified line while the user follows its prefix, and uses Stockfish after a deviation. Historical tournamentLine data remains available as provenance but no longer forces a known weak historical defence for verified packs. A faster checkmate after a defensive mistake, or a different legal mating line within the limit, still counts as correct.

Many Famous Games positions remain engine training continuations after historical resignation. These are visibly labelled; they are not presented as moves actually played. The recorded scores are in famous-source-games.pgn, and training continuations/source links are recorded separately. Verification changes category correctness, not the historical status of a derived board.

## Links and future collections

Existing valid IDs are kept where possible; incorrectly categorised slots are replaced. For the reduced tournament categories, retired IDs redirect through an aliases map to a verified position at that same level. Both index pages list only the verified positions. The catalogue still accepts future year, tournament or player collections. New packs should follow this exact-length policy and can include defenceLine; otherwise the player retains backwards-compatible tournamentLine behaviour.

## Reproduce the check

validation/exact-mate-certificates.csv lists every delivered starting FEN, exact mate length, proof node count and verified line. validation/previous-pack-audit.csv lists the result of checking each of the 1,200 previous pack entries. EXACT proves the old category, SHORTER proves it belongs below that category, and UNKNOWN means the check reached its node limit and the entry was not admitted on that result.

The independent validator source and its MIT-licensed chess rules header are supplied in validation/. Compile with:

    g++ -std=c++17 -O3 -DNDEBUG -o mate-proof validation/mate-proof.cpp

The program accepts one request per line: category, node budget, tab, then FEN. For example:

    3 100000000	7q/1R4pk/7p/3BQP2/2pP4/2P5/5PPP/6K1 w - - 1 36

It prints EXACT/SHORTER/NO_MATE/UNKNOWN, search nodes, and a best-resistance PV for exact positions. UNKNOWN is inconclusive and must not be classified as an exact mate.
