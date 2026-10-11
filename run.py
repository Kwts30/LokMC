"""LokMC — Unified Single-Process Launcher (Crafty Controller Architecture).

Executes the unified LokMC daemon on http://localhost:8443.
Serves the web dashboard, REST API, WebSockets, and server orchestration
from a single unified service without requiring multiple terminals.
Works on PC (Windows/Linux/macOS) and Phone (Android Termux / Pydroid 3).
"""

import os
import sys
import socket
import argparse
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"
BUILD_DIR = FRONTEND_DIR / "build"


def get_local_ip():
    """Detect the local machine IP on Wi-Fi or LAN for mobile phone access."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


def main():
    parser = argparse.ArgumentParser(description="LokMC Unified Server Launcher")
    parser.add_argument("--host", default="0.0.0.0", help="Host interface to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8443, help="Port to listen on (default: 8443)")
    parser.add_argument("--reload", action="store_true", help="Enable uvicorn hot reloading for development")
    args = parser.parse_args()

    # 1. Build frontend if not already present
    if not (BUILD_DIR / "index.html").exists():
        print("[LokMC] Frontend build directory not detected. Attempting build...")
        try:
            subprocess.run(["npm", "run", "build"], cwd=str(FRONTEND_DIR), check=True, shell=(sys.platform == "win32"))
            print("[LokMC] Frontend built successfully.")
        except Exception as e:
            print(f"[LokMC Warning] Could not automatically build frontend via npm: {e}")
            print("[LokMC Warning] The API will still run. Run 'npm run build' inside frontend/ when Node is available.")

    # 2. Identify virtual environment python on PC if available
    is_win = sys.platform == "win32"
    if is_win:
        base_prefix = Path(sys.base_prefix)
        dll_dir = base_prefix / "DLLs"
        if dll_dir.exists():
            try:
                os.add_dll_directory(str(dll_dir))
            except (AttributeError, OSError):
                pass
            try:
                os.add_dll_directory(str(base_prefix))
            except (AttributeError, OSError):
                pass
            os.environ["PATH"] = f"{base_prefix};{dll_dir};{os.environ.get('PATH', '')}"

    venv_python = BACKEND_DIR / (".venv/Scripts/python.exe" if is_win else ".venv/bin/python")

    # If running with external python on PC, re-exec inside venv if venv exists
    if venv_python.exists() and sys.executable.lower() != str(venv_python).lower():
        if is_win:
            sys.exit(subprocess.call([str(venv_python), str(Path(__file__).resolve())] + sys.argv[1:]))
        else:
            os.execv(str(venv_python), [str(venv_python), str(Path(__file__).resolve())] + sys.argv[1:])

    # 3. Setup python path
    os.chdir(str(BACKEND_DIR))
    sys.path.insert(0, str(BACKEND_DIR))

    local_ip = get_local_ip()

    # Reconfigure stdout to utf-8 if supported
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("\n" + "=" * 64)
    print("  * LokMC - Minecraft Server Remote Management Daemon *")
    print(f"  PC Local Access:    http://localhost:{args.port}")
    print(f"  Phone / LAN Access: http://{local_ip}:{args.port}")
    print("  Architecture: Unified Async Daemon (Single Port & Process)")
    print("=" * 64 + "\n")

    import uvicorn
    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
