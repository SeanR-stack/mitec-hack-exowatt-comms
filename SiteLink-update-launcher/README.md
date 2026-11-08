# Run in VS Code

Requires Python 3.9 or newer. The launcher uses only the Python standard library: no pip install, no npm install, no build step and no VS Code extension is needed.

1. Clone or download this repository, then in VS Code choose **File > Open Folder** and open the `SiteLink-update-launcher` folder.
2. Choose **Terminal > New Terminal** and make sure the terminal is in that folder.
3. Run `python3 launcher.py` on macOS/Linux, or `py -3 launcher.py` on Windows. If `python` is Python 3 on your machine, `python launcher.py` works too.
4. The launcher prints a local `http://127.0.0.1:<port>` address and opens it in your browser. Keep the terminal open while using the launcher; press **Ctrl+C** to stop it.

Do not open `launcher.html` with Live Server or as a plain file: the version library needs the Python server's local routes. See `README.txt` for how to import future builds, plus backup and offline notes. The bundled v8, v9 and v10 builds are simulated previews; nothing in this folder controls real hardware.
