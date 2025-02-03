import subprocess
import platform
import shutil
import typer
from pathlib import Path
from dotenv import dotenv_values
import os

# Load environment variables
config = dotenv_values("project.env")

# Constants from .env file
PROJECT_NAME = config.get("PROJECT_NAME", "example_project")
ENTRY_SCRIPT = config.get("ENTRY_SCRIPT", "example/cli.py")
OUTPUT_NAME = config.get("OUTPUT_NAME", "example_output")
DIST_DIR = config.get("DIST_DIR", "dist")

app = typer.Typer()

def is_package_installed(package_name: str) -> bool:
    """Check if a Python package is installed."""
    try:
        subprocess.run(
            [package_name, "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def clean():
    """Remove previous build artifacts and reinstall dependencies."""
    cwd = Path(__file__).parent
    build_dir = cwd / "build"
    dist_dir = cwd / DIST_DIR
    spec_file = cwd / f"{PROJECT_NAME}.spec"
    venv_dir = cwd / ".venv"
    python_executable = venv_dir / ("Scripts" if platform.system() == "Windows" else "bin") / "python"

    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    if spec_file.exists():
        spec_file.unlink()
    print("Cleaned previous build artifacts.")

    if venv_dir.exists():
        print("Reinstalling dependencies in virtual environment...")
        subprocess.run([python_executable, "-m", "pip", "install", "-r", cwd / "requirements.txt", "--no-cache-dir"], check=True)
        print("Reinstalled dependencies.")

@app.command()
def build(clean_before: bool = typer.Option(False, "--clean", help="Clean build artifacts before building")):
    """Build the project into a standalone executable."""
    cwd = Path(__file__).parent
    venv_dir = cwd / ".venv"
    python_executable = venv_dir / ("Scripts" if platform.system() == "Windows" else "bin") / "python"

    if clean_before:
        clean()

    if not venv_dir.exists():
        print("Virtual environment not found. Creating .venv...")
        subprocess.run(["python", "-m", "venv", venv_dir], check=True)
        print(".venv created successfully.")

    print("Installing dependencies inside the virtual environment...")
    subprocess.run([python_executable, "-m", "pip", "install", "-r", cwd / "requirements.txt"], check=True)

    print(f"Building {OUTPUT_NAME} for {platform.system()}...")
    cmd = [python_executable, "-m", "PyInstaller", "--onefile", "--name", OUTPUT_NAME, ENTRY_SCRIPT]

    try:
        subprocess.run(cmd, check=True)
        print(f"Build completed. Executable is in the '{DIST_DIR}' folder.")
    except subprocess.CalledProcessError as e:
        print("Error: The build process failed.")
        print("Check the output above for details and ensure your entry script is correct.")
        raise e

if __name__ == "__main__":
    app()
