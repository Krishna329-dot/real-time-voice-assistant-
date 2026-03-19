import subprocess
import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_ui():
    return subprocess.Popen(
        [sys.executable, "ui_server.py"],
        cwd=BASE_DIR
    )

def run_agent():
    return subprocess.Popen(
        [sys.executable, "agent.py", "console"],
        cwd=BASE_DIR
    )

if __name__ == "__main__":
    print("🚀 Starting JARVIS System...")
    print("🖥️  Launching Avatar UI...")
    ui_process = run_ui()

    time.sleep(2)  # UI ko thoda time do start hone ka

    print("🎤 Launching JARVIS Agent...")
    agent_process = run_agent()

    try:
        ui_process.wait()
        agent_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down JARVIS...")
        ui_process.terminate()
        agent_process.terminate()
