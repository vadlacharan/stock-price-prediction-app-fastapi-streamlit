import os
import subprocess
import sys


def install_requirements(venv_path):
    """Install dependencies from requirements.txt without updating the file."""
    print("Installing requirements...")

    # Activate the virtual environment
    activate_path = os.path.join(venv_path, "Scripts", "activate") if os.name == "nt" else os.path.join(venv_path, "bin", "activate")
    
    # Install dependencies from requirements.txt
    commands = [
        f"source {activate_path} && pip install -r requirements.txt"
        if os.name != "nt"
        else f"call {activate_path} && pip install -r requirements.txt "
    ]

    for command in commands:
        subprocess.run(command, shell=True, check=True)
    print("Requirements installed.")


def run_app(command, app_name):
    """Run an app (backend or frontend)."""
    print(f"Starting {app_name}...")
    process = subprocess.Popen(command, shell=True)
    return process


if __name__ == "__main__":
    # Define paths
    venv_path = "backend/venv"  # Shared virtual environment path

    try:
        # Step 1: Install dependencies from requirements.txt
        install_requirements(venv_path)

        # Step 2: Run both apps
        backend_process = run_app(f"source backend/venv/bin/activate && cd backend && uvicorn main:app --reload", "FastAPI Backend") \
            if os.name != "nt" else run_app(f"call backend\\venv\\Scripts\\activate && cd backend && fastapi dev main.py", "FastAPI Backend")

        frontend_process = run_app(f"source backend/venv/bin/activate && cd frontend && streamlit run app.py", "Streamlit Frontend") \
            if os.name != "nt" else run_app(f"call backend\\venv\\Scripts\\activate && cd frontend && streamlit run main.py", "Streamlit Frontend")

        print("Both Backend and Frontend are running!")

        # Step 3: Wait for processes to complete
        backend_process.wait()
        frontend_process.wait()

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\nShutting down both apps...")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)
