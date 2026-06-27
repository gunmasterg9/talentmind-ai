"""
Local launcher script for TalentMind AI
Concurrently runs FastAPI backend and Next.js frontend for local testing
"""

import os
import sys
import subprocess
import time
import signal
import socket
import shutil

# Ensure Node.js and Python paths are in environment PATH
nodejs_path = r"C:\Program Files\nodejs"
if os.path.exists(nodejs_path) and nodejs_path not in os.environ.get("PATH", ""):
    os.environ["PATH"] = nodejs_path + os.path.pathsep + os.environ.get("PATH", "")

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def kill_port_owner(port):
    # Try to free ports if they are already occupied (common after crashes)
    if sys.platform.startswith('win'):
        try:
            output = subprocess.check_output(f'netstat -aon | findstr :{port}', shell=True).decode()
            for line in output.strip().split('\n'):
                parts = line.split()
                if len(parts) > 4:
                    pid = parts[-1]
                    if pid != '0':
                        print(f"Stopping existing process on port {port} (PID: {pid})...")
                        subprocess.run(f"taskkill /F /PID {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

def main():
    print("=" * 60)
    print("      TalentMind AI - Local Concurrency Launcher")
    print("=" * 60)
    
    # 1. Clean up ports 8000 and 3000
    kill_port_owner(8000)
    kill_port_owner(3000)

    # 2. Check and generate candidates data if needed
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    
    candidates_json = os.path.join(data_dir, "candidates.json")
    db_path = os.path.join(data_dir, "talentmind.db")
    if os.path.exists(candidates_json) and not os.path.exists(db_path):
        print("Found candidates.json dataset! Running batch importer...")
        subprocess.run([sys.executable, os.path.join(data_dir, "import_jsonl.py"), candidates_json], check=True)
        print("Candidates dataset import completed.")
    elif not os.path.exists(db_path):
        print("Initial database seed not found. Running seed script...")
        subprocess.run([sys.executable, os.path.join(data_dir, "seed.py")], check=True)
        print("Database seeding completed.")

    # 3. Start Backend FastAPI
    print("Starting FastAPI Backend (Port 8000)...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Wait for backend to be online (models take time to load on startup)
    retries = 60
    backend_ready = False
    while retries > 0:
        if is_port_open(8000):
            backend_ready = True
            break
        time.sleep(1)
        retries -= 1

    if not backend_ready:
        print("Error: Backend failed to start on port 8000.")
        backend_process.terminate()
        return

    print("FastAPI Backend is online.")

    # 4. Start Next.js Frontend
    print("Starting Next.js Frontend (Port 3000)...")
    
    # Find npm executable dynamically
    npm_cmd = "npm"
    possible_npms = [
        "npm",
        r"C:\Program Files\nodejs\npm.cmd",
        r"C:\Program Files (x86)\nodejs\npm.cmd",
        os.path.expanduser(r"~\AppData\Roaming\npm\npm.cmd")
    ]
    for n in possible_npms:
        if shutil.which(n) or os.path.exists(n):
            npm_cmd = f'"{n}"' if " " in n else n
            break

    # Check if node_modules exists
    if not os.path.exists(os.path.join(frontend_dir, "node_modules")):
        print("Frontend dependencies (node_modules) not found. Running npm install...")
        subprocess.run(f"{npm_cmd} install --legacy-peer-deps", shell=True, cwd=frontend_dir)

    frontend_process = subprocess.Popen(
        f"{npm_cmd} run dev",
        shell=True,
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Wait for frontend to be online
    retries = 60
    frontend_ready = False
    while retries > 0:
        if is_port_open(3000):
            frontend_ready = True
            break
        time.sleep(1)
        retries -= 1

    if not frontend_ready:
        print("Error: Frontend failed to start on port 3000.")
        backend_process.terminate()
        frontend_process.terminate()
        return

    print("\n" + "=" * 60)
    print(" [SUCCESS] Redrob AI Platform is running locally!")
    print("=" * 60)
    print("  * Web UI:            http://localhost:3000")
    print("  * Backend API Docs:  http://localhost:8000/docs")
    print("=" * 60)
    print("Press CTRL+C to terminate both processes.")
    print("=" * 60 + "\n")

    # Monitor output and wait for interrupt
    try:
        while True:
            # Check if either process terminated
            if backend_process.poll() is not None:
                print("Backend terminated unexpectedly.")
                break
            if frontend_process.poll() is not None:
                print("Frontend terminated unexpectedly.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
    finally:
        # Gracefully terminate both processes
        backend_process.terminate()
        frontend_process.terminate()
        
        # Give them a moment to terminate
        time.sleep(1)
        kill_port_owner(8000)
        kill_port_owner(3000)
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
