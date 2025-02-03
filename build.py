import subprocess
import platform
import shutil
import typer
from pathlib import Path
from dotenv import dotenv_values

# Load environment variables
config = dotenv_values("project.env")

# Constants from .env file
SESSION_CWD = Path(__file__).parent
ENTRY_SCRIPT = config.get("ENTRY_SCRIPT", "example/cli.py")
OUTPUT_NAME = config.get("OUTPUT_NAME", "example_output")
DIST_DIR = SESSION_CWD / config.get("DIST_DIR", "dist")

VENV_DIR = SESSION_CWD / ".venv"  # Using `.venv` for consistency
PYTHON_EXECUTABLE = (
    VENV_DIR / "Scripts" / "python"
    if platform.system() == "Windows"
    else VENV_DIR / "bin" / "python"
)

app = typer.Typer()

def clean():
    """Remove previous build artifacts."""
    build_dir = SESSION_CWD / "build"
    spec_file = SESSION_CWD / f"{OUTPUT_NAME}.spec"

    for path in [build_dir, DIST_DIR, spec_file]:
        if path.exists():
            shutil.rmtree(path) if path.is_dir() else path.unlink()
    print("✔ Cleaned previous build artifacts.")

def setup_venv():
    """Ensure a virtual environment exists and install dependencies (for local builds)."""
    if not VENV_DIR.exists():
        print("Creating virtual environment...")
        subprocess.run(["python", "-m", "venv", str(VENV_DIR)], check=True)

    print("Installing dependencies...")
    subprocess.run(
        [str(PYTHON_EXECUTABLE), "-m", "pip", "install", "-r", "requirements.txt"],
        check=True,
    )

@app.command()
def build(
    clean_before: bool = typer.Option(
        False, "--clean", help="Clean build artifacts before building"
    ),
    ci: bool = typer.Option(
        False, "--ci", help="Run in CI mode (skip virtual environment setup)"
    ),
):
    """Build the project into a standalone executable."""

    if clean_before:
        clean()

    if not ci:
        setup_venv()

    # Determine which Python executable to use
    python_exec = "python" if ci else str(PYTHON_EXECUTABLE)

    print(f"🚀 Building {OUTPUT_NAME} for {platform.system()}...")
    cmd = [
        python_exec,
        "-m",
        "PyInstaller",
        "--onefile",
        "--name",
        OUTPUT_NAME,
        ENTRY_SCRIPT,  # FIXED: Correctly referencing the entry script
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✔ Build completed. Executable is in the '{DIST_DIR}' folder.")
    except subprocess.CalledProcessError as e:
        print("❌ Error: Build process failed.")
        raise e

if __name__ == "__main__":
    app()
