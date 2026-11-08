SiteLink update library

Requires Python 3.9+ on this laptop. No third-party packages.
1. Extract the entire ZIP to a writable folder.
2. Open a terminal in that folder and run: python3 launcher.py
   Windows may use: py -3 launcher.py
3. The browser opens a 127.0.0.1 local address. Keep the terminal open while using it. Ctrl+C stops it.

ADD FUTURE UPDATES
Obtain a trusted standalone HTML build through download, USB or local transfer. In the library give it a name, choose the file, acknowledge that you trust its source, then Save update offline. This copies the complete file into builds/ and adds it to versions.json. Old builds are never replaced. An identical file selects the existing build. Import accepts UTF-8 complete HTML, maximum 12 MB, not ZIPs, Python apps or dependent multi-file builds.

Choose a saved build and Launch. Back to versions closes that simulation and returns to the library. Unsaved state/results are not transferred. Closing/restarting the launcher preserves imported files. Back up the entire folder. Do not edit versions.json or remove builds manually while running.

The local server binds only to 127.0.0.1 on a free port. It is not shared over the network. Imported builds run in an isolated browser frame; browser-specific APIs may be unavailable there. External links/dependencies can still require internet. Only self-contained builds can be expected to work offline. This is not a hardware connector, updater, digital-signature verifier or malware scanner. Import only code you trust.

Includes unchanged v8, v9 and v10 simulated previews. Nothing controls real hardware. The main UI-polish preview is separate.
