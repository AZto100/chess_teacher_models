# Chess Teacher - optional hands-free voice update

## Updating a working installation

Replace only `index.html` in your existing chess app folder/repository. Keep all
existing chess, Stockfish, Maia and speech runtime/model files, and keep
`voice-coi-serviceworker.js` beside the HTML. Refresh the page with Ctrl+F5 after
publishing. This update does not require different speech binaries or a new model.

This package also contains the same optional speech installer and isolation helper
as the previous voice release. Those helpers are unchanged. The large speech,
chess and engine binaries are NOT included in this ZIP.

## Click-to-move is still the default

On every page load the microphone is off and the voice panel is closed. Click a
piece and then its destination exactly as before; mouse moves do not require a
voice confirmation. The game, strength and other existing saved settings retain
their original storage key. No microphone session, preview or transcript is saved.

## Hands-free play

Open **Voice (optional)** and click **Start hands-free**. The selected local speech
method is prepared when necessary. The first Whisper setup may require one reload
for cross-origin isolation; then open the panel and start again. Accept the browser's
microphone permission prompt. The **Voice settings, typed correction & setup**
section contains the speech-method choice and a separate **Prepare voice** button.

Speak one short command at a time:

| Spoken command | Result |
| --- | --- |
| `C two to C four` | Preview C2:C4. Only C4 is highlighted green, with a dotted centre-to-centre line from C2. No piece moves. |
| `D two to D four` | Replace the previous preview. Only D4 is highlighted green. |
| `move` | Play the currently previewed legal move. Say it separately, after the preview is displayed and Listening is shown. |
| `cancel` | Clear the preview without turning off hands-free. Normal hints return. |
| `stop listening` | Turn off hands-free and release microphone resources. |

Phonetic coordinates such as `Charlie two to Charlie four` also work. Coordinates
and `move` in one utterance do not bypass confirmation. A repeated `move` without
a pending preview does nothing. Illegal or unclear replacement commands clear the
old preview rather than leaving a potentially unwanted move ready to execute.

The green preview is YOUR command, not an engine recommendation. It temporarily
replaces all engine-coloured squares and engine dotted lines, without changing
your saved white/black hint switches. It is still visible when those hints are off.
The destination stays green even when it was part of the latest grey-highlighted move.

In Practice, speak moves for either colour. In Play computer, speak only for your
bottom-side colour. Hands-free waits during the computer turn and becomes ready
again automatically after the computer replies. The mouse remains available
while hands-free is running. Clicking the board clears the preview and invalidates
any unfinished voice command so that your mouse selection takes priority.

### Promotions and castling

Say `castle kingside` or `castle queenside` when legal, then `move`. The preview
shows the king's destination; confirming plays the complete castling move.

Say `E seven to E eight promote to queen`, then `move`. When a promotion piece was
not specified, the app previews the destination and asks for `queen`, `rook`,
`bishop` or `knight`. Say the piece, review the updated preview, then say `move`.
It does not silently choose a queen.

### Timing and optional manual controls

Whisper detects a pause automatically, then transcribes that phrase locally. There
is no Stop-and-transcribe click between commands. The existing stream.wasm model
interface accepts short phrases: keep coordinates to about four seconds. The
Whisper pause setting is available inside the settings section.

While the indicator says **Processing - wait**, wait for **Listening** before
speaking the next command. Audio during processing or the computer's turn is
ignored, not queued. No promise of instant transcription is made; speed depends on
your machine and local speech model. Browser recognition processes final results
only and is re-armed after a normal recognition-session end.

The visible **Play [move]** button and the editable transcript under settings are
optional alternatives. The main board does not need them for ordinary mouse play.

New game, Undo, engine/seat/play-setting changes, Escape, closing the voice panel,
hiding the tab or a speech failure stop the session and clear its preview. Ordinary
mouse, voice and computer moves keep an explicitly started hands-free session
enabled. After a reload or returning from a hidden tab, explicitly start hands-free
again. **Stop listening** always stops; it does not transcribe or play a last command.

## Reusing the existing local speech assets

Whisper uses these existing files:

```
index.html
voice-coi-serviceworker.js
wasm/
    stream.js
    ... matching WASM/worker companions
models/
    ggml-base.en-q5_1.bin
```

The existing engine, `vendor/`, Maia and other model files remain where they were.

To copy speech assets from your oral-exam folder (Python 3.9+):

```bat
py -3 install-voice.py --from-exam "C:\path\to\oral-exam"
```

To use the unchanged download installer instead:

```bat
py -3 install-voice.py
```

Or double-click `Install-voice-Windows.cmd`. Upload the actual downloaded files,
not a ZIP, when publishing a new setup. For an already working voice installation,
none of these installation steps need to be repeated for the hands-free update.

The alternative browser on-device method requires real `processLocally` support
and an installed language pack. It never silently falls back to cloud recognition.
Whisper uses the existing isolation helper and local model. Both methods need
HTTPS/localhost and microphone permission. Hosting, browser permissions and actual
speech recognition should be checked on your target device.

## Privacy and validation

No recording or transcript is stored in the app's saved game or uploaded by this
application. The active microphone is indicated on screen. Capture buffers are
bounded and discarded after processing/cancellation. A spoken confirmation is
accepted only for the same current position and preview, after that preview has
been rendered. Background or outdated recognition results cannot commit a move.

Speech recognition can still mishear a legal coordinate or a confirmation. Review
the single green destination before saying `move`. There is deliberately no
immediate-play-on-coordinates option, including for users who enabled that option
in the previous release.

Primary implementation references:
- https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition/continuous
- https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition/end_event
- https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition/processLocally

See `VOICE_TEST_REPORT.md` for the checks performed and their limitations.
