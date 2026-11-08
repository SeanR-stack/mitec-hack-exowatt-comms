# Offline field workspace

Local, simulated robot/drone survey workspace with a saved-version library. The current bundled layout is v18: black/charcoal throughout, orange accents, left-side tabs, survey controls, Fleet, companion 3D view, comparison tools and Activity. Older v8, v9, v10 and v17 builds are retained. Future standalone HTML builds can be imported without replacing older versions.

This is a simulation, not a hardware connector. There are no live sensor readings or real equipment commands. Obstacle modeling is not implemented. The comparison uses illustrative assumptions, not measured HM-10 performance or verified price quotes.

## Run in VS Code

Requires **Python 3.9 or newer** and a modern browser. The launcher uses only Python's standard library. No pip install, npm install, build step or VS Code extension is required.

1. Clone or download this folder to a writable location.
2. In VS Code choose **File > Open Folder** and open the folder containing `launcher.py`, `launcher.html`, `versions.json` and `builds/`.
3. Choose **Terminal > New Terminal**. Make sure the terminal is in that same folder.
4. Run:

   macOS/Linux:
   ```sh
   python3 launcher.py
   ```

   Windows:
   ```powershell
   py -3 launcher.py
   ```

   If your Python 3 installation uses the `python` command instead, run `python launcher.py`.

5. The launcher opens your browser at a printed `http://127.0.0.1:<port>` address. If it does not open, copy the exact address from the terminal. The port is chosen automatically and can change on restart.
6. Choose **v18 - Robot names and link error** (or an older saved version), then **Launch selected version**. It fills the browser window. **Back to versions** closes that simulation and returns to the library. **Full screen** requests native browser fullscreen where supported; press Escape to leave native fullscreen.
7. Keep the terminal running while using the launcher. Press **Ctrl+C** to stop it.

Do not use VS Code Live Server or open `launcher.html` directly for the version library: it needs the Python launcher's local `/api/versions`, `/api/import` and `/build` routes. A standalone self-contained build under `builds/` can be opened directly for a quick simulation preview, but that bypasses the library.

On macOS, `Start-SiteLink.command` is an optional shortcut for running the same Python launcher; the terminal commands above are the cross-platform route. The shortcut's filename is legacy branding, not the current workspace name.

## Import future versions offline

1. Obtain a trusted **standalone HTML** build by download, USB or local transfer.
2. In the version library enter a version name, choose the HTML file and acknowledge that you trust its source.
3. Select **Save update offline**. The launcher copies the file into `builds/` and records it in `versions.json`.
4. Select the saved version and launch it. An identical file selects its existing entry instead of creating a duplicate.

Imports accept complete UTF-8 HTML up to 12 MB, not ZIP archives, Python applications or multi-file builds. Old builds are not replaced. Imported versions survive restarting the launcher. Switching versions starts a new simulation; unsaved simulation state/results do not transfer.

Back up the entire folder, including `builds/` and `versions.json`. Do not replace those two items with a fresh download if you want to keep local imports. Stop the launcher before manually updating its files. Do not edit the version index or delete build files while it is running.

## Local-only and offline limits

The server binds only to `127.0.0.1` on the current computer, not the network. Self-contained bundled builds can run offline. An imported build with external links or dependencies may still need internet. The browser frame limits some browser-specific APIs. Import only code you trust: the launcher is not a malware scanner or signature verifier.

The full-window behavior is already included in `launcher.html`; the older `README-full-window.txt` is retained as historical patch guidance and is not a separate installation step for this complete folder.
