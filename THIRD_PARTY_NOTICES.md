# Third-party notices and source access

This is an integration of existing open-source engines, not a new chess engine or
a claim of ownership over their code/models. The application source is the readable
`index.html`, including its embedded Maia worker. The downloader is also readable
source. Keep this file, applicable notices, licences and source access when sharing
the application, even if there is no charge. The upstream projects' licences
govern their respective components; this list is not a waiver of their terms.

## Stockfish / Stockfish.js 19.0.1

Author credits belong to the Stockfish contributors, Nathan Rugg, Chess.com and
other contributors identified in the upstream AUTHORS and source files.

- Licence: GPL version 3, copied by the installer to `licenses/Stockfish-GPL-3.0.txt`.
- Exact published engine release: https://github.com/nmrugg/stockfish.js/releases/tag/v19.0.1
- Corresponding source tree: https://github.com/nmrugg/stockfish.js/tree/v19.0.1
- Source archive: https://github.com/nmrugg/stockfish.js/archive/refs/tags/v19.0.1.zip
- Build script: https://github.com/nmrugg/stockfish.js/blob/v19.0.1/build.js
- Source/build support directory: https://github.com/nmrugg/stockfish.js/tree/v19.0.1/src
- Primary upstream: https://github.com/official-stockfish/Stockfish

The installer obtains the **unmodified** lite-single and full-single release pairs
and checks the SHA-256 values published on that release. No Stockfish C++/NNUE
modifications are part of this update. Source access must cover the exact binaries
you actually distribute, including required build scripts and neural-network
material, not just an unrelated current Stockfish checkout. If you rebuild or
modify them, retain and publish that matching source/build material too. Keep
upstream source access available to recipients or host a corresponding copy.

## Maia browser export, move mapping and reference interface

The official CSSLab frontend provides the targeted model, move-index data and
browser interface, pinned to commit:

`a6e52f5c811ee18863cb2f0e81f2433a5b9905de`

- Exact source: https://github.com/CSSLab/maia-platform-frontend/tree/a6e52f5c811ee18863cb2f0e81f2433a5b9905de
- Frontend licence: GPL version 3; copied to `licenses/Maia-frontend-GPL-3.0.txt`.
- Browser model: `public/maia3/maia3_simplified.onnx`
- Move-index mapping: `src/lib/engine/data/all_moves_maia3.json`
- Interface reference: `public/maia-worker.js`
- Position encoding reference: `src/lib/engine/tensor.ts`

The new worker/adapter in `index.html` targets those tensor and policy interfaces;
it is not the Maia website's full frontend and does not require React/Next.js.
The source and runtime URLs are local and have been adapted for a standalone page.
No model training, weight modification or claimed strength calibration was done.

## Maia-3 core model project

Credit: CSSLab, University of Toronto, and the Maia/Chessformer authors and
contributors credited in the official repositories and model cards.

- Project/source: https://github.com/CSSLab/maia3
- Licence notice: https://github.com/CSSLab/maia3/blob/main/LICENSE
- Model family: https://huggingface.co/collections/MaiaChess/maia3
- Model card, with code/weights licence direction: https://huggingface.co/UofTCSSLab/Maia3-5M

The installer retains the core project's AGPLv3 notice as
`licenses/Maia3-AGPL-3.0.txt`, alongside the frontend's GPL notice. Preserve both
upstream notices and review the terms for the exact model you redistribute. The
paper's CC BY 4.0 notice is **not** a replacement code/weights licence. The browser
ONNX export is identified by its own pinned frontend path above; this app does not
claim it is interchangeable with every native Maia-3 checkpoint.

## ONNX Runtime Web 1.23.0

Copyright Microsoft Corporation and contributors. MIT licence, with third-party
notices retained by the installer. The three runtime files are copied from the
same pinned CSSLab public/ort folder so their versions and generated interfaces
match, not mixed between releases.

- Source: https://github.com/microsoft/onnxruntime/tree/v1.23.0
- Licence: https://github.com/microsoft/onnxruntime/blob/v1.23.0/LICENSE
- Third-party notices: https://github.com/microsoft/onnxruntime/blob/v1.23.0/ThirdPartyNotices.txt
- Local copies: `licenses/ONNX-Runtime-MIT.txt`, `licenses/ONNX-Runtime-ThirdPartyNotices.txt`

## chess.js 1.4.0

Copyright Jeff Hlywa and other contributors as stated in the upstream notice.
BSD-2-Clause licence; retain the complete notice in source and redistributions.

- Source: https://github.com/jhlywa/chess.js/tree/v1.4.0
- Licence: https://github.com/jhlywa/chess.js/blob/v1.4.0/LICENSE
- Local copy: `licenses/chess.js-LICENSE.txt`

## Application-specific assets

The supplied `index.html` retains the previous board's embedded vector piece
artwork and UI, with the engine-switch/Maia adapter added as editable source. It
does not add downloaded piece images or proprietary fonts. There are no credentials,
tracking services or API keys in this update. Runtime model files are separate
from the source ZIP and must be installed before selecting the new opponents.
