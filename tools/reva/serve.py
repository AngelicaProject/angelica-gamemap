"""Serve ReVa, the MCP server of Ghidra, on an analyzed Ghidra project,
without Ghidra's window: http://127.0.0.1:8080/mcp/message.

Run it with the Python environment that has Ghidra's PyGhidra
(`.ai/adding-entries.md`, "Ghidra and ReVa"), and keep it running while you
work; Ctrl+C stops it:

    python tools/reva/serve.py --ghidra <Ghidra folder> --projects <folder> --project ffxiv
"""
import argparse
import os
import sys
import time


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ghidra", required=True, help="the Ghidra folder, with ghidraRun.bat")
    parser.add_argument("--projects", required=True, help="the folder that holds the project")
    parser.add_argument("--project", default="ffxiv", help="the project's name")
    args = parser.parse_args()

    os.environ["GHIDRA_INSTALL_DIR"] = args.ghidra
    import pyghidra

    pyghidra.start(install_dir=args.ghidra)
    from java.io import File
    from reva.headless import RevaHeadlessLauncher

    # No configuration file: ReVa's defaults, 127.0.0.1 and port 8080.
    launcher = RevaHeadlessLauncher(None, True, False, File(args.projects), args.project)
    launcher.start()
    if not launcher.waitForServer(60000):
        print("ReVa did not start in 60 seconds", file=sys.stderr)
        return 1
    print(f"ReVa serves {args.project} on http://127.0.0.1:{launcher.getPort()}/mcp/message", flush=True)
    try:
        while launcher.isRunning():
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        # Ctrl+C may have stopped the JVM first, and the server with it.
        try:
            launcher.stop()
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
