import json
import shutil
import requests
import zipfile
import subprocess
import typer
import winreg
from pathlib import Path
from InquirerPy import prompt
from InquirerPy.base.control import Choice

app = typer.Typer()

__version__ = "dev"  # Placeholder, will be replaced by build.py

WNVM_DIR = Path.home() / "wnvm"
VERSIONS_DIR = WNVM_DIR / "versions"
CONFIG_FILE = WNVM_DIR / "config.json"
NODE_BASE_URL = "https://nodejs.org/dist"
WNVM__IDENTIFIER = "wnvm"

# Ensure required directories exist
WNVM_DIR.mkdir(exist_ok=True)
VERSIONS_DIR.mkdir(exist_ok=True)


def save_config(current_version: str):
    """Save the currently active Node.js version."""
    with open(CONFIG_FILE, "w") as f:
        json.dump({"current_version": current_version}, f)


def load_config():
    """Load the currently active Node.js version."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f).get("current_version")
    return None


def update_user_path(new_node_path: Path):
    """Persistently update the user PATH variable."""
    reg_key = r"Environment"

    # Read existing PATH
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_READ) as key:
        current_path, _ = winreg.QueryValueEx(key, "Path")

    # Remove old wnvm paths (if any)
    new_path_entries = [p for p in current_path.split(";") if WNVM__IDENTIFIER not in p]

    # Add new Node.js path at the beginning
    new_path_entries.insert(0, str(new_node_path))

    # Update PATH in the registry
    new_path = ";".join(new_path_entries)
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key, 0, winreg.KEY_WRITE) as key:
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)

    # Apply changes immediately (no reboot required)
    subprocess.run(["setx", "Path", new_path], shell=True)


def get_available_versions():
    """Get all available Node.js versions from the official website."""
    response = requests.get(f"{NODE_BASE_URL}/index.json")
    if response.status_code != 200:
        typer.echo("❌ Error: Could not retrieve available versions.")
        return []

    versions = response.json()
    return [version["version"].lstrip("v") for version in versions]


@app.command()
def available():
    """List all available Node.js versions."""
    typer.echo("Fetching available Node.js versions...")
    versions = get_available_versions()
    if not versions:
        typer.echo("❌ No versions available.")
    else:
        typer.echo("Available Node.js versions:")
        for version in versions:
            typer.echo(f"  {version}")


@app.command()
def install(version: str = typer.Argument(None)):
    """Download and install a specific Node.js version."""
    versions = get_available_versions()
    if not versions:
        typer.echo("❌ No versions available to install.")
        return

    if version is None:
        question = {
            "type": "fuzzy",
            "name": "version",
            "message": "Select a Node.js version to install:",
            "choices": [Choice(v) for v in versions],
        }
        answers = prompt(question)
        version = answers["version"]
    else:
        # Find the closest match for the specified version
        matching_versions = [v for v in versions if v.startswith(version)]
        if not matching_versions:
            typer.echo(f"❌ No available versions match '{version}'.")
            return
        version = matching_versions[0]

    version_dir = VERSIONS_DIR / version

    if version_dir.exists():
        typer.echo(f"✔ Node.js v{version} is already installed.")
        return

    zip_url = f"{NODE_BASE_URL}/v{version}/node-v{version}-win-x64.zip"
    zip_path = WNVM_DIR / f"node-v{version}.zip"

    typer.echo(f"⬇ Downloading Node.js v{version}...")
    response = requests.get(zip_url, stream=True)

    if response.status_code != 200:
        typer.echo(f"❌ Error: Could not find Node.js v{version}.")
        return

    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    typer.echo(f"📦 Extracting Node.js v{version}...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(version_dir)

    zip_path.unlink()  # Remove zip file after extraction
    typer.echo(f"✔ Installed Node.js v{version} successfully!")


@app.command()
def list():
    """List installed Node.js versions."""
    installed_versions = [p.name for p in VERSIONS_DIR.iterdir() if p.is_dir()][::-1]
    if not installed_versions:
        typer.echo("No Node.js versions installed.")
    else:
        typer.echo("Installed Node.js versions:")
        for v in installed_versions:
            prefix = "👉" if v == load_config() else "  "
            typer.echo(f"{prefix} {v}")


@app.command()
def use(version: str = typer.Argument(None)):
    """Persistently switch to a specific Node.js version."""
    installed_versions = [p.name for p in VERSIONS_DIR.iterdir() if p.is_dir()][::-1]

    if not installed_versions:
        typer.echo("❌ No Node.js versions installed.")
        return

    if version is None:
        questions = [
            {
                "type": "list",
                "name": "version",
                "message": "Select a Node.js version to use:",
                "choices": installed_versions,
            }
        ]
        answers = prompt(questions)
        version = answers["version"]

    version_dir = VERSIONS_DIR / version
    node_path = version_dir / f"node-v{version}-win-x64" / "node.exe"

    if not node_path.exists():
        typer.echo(
            f"❌ Node.js v{version} is not installed. Run `wnvm install {version}` first."
        )
        return

    typer.echo(f"✔ Persistently switching to Node.js v{version}...")

    update_user_path(node_path.parent)
    save_config(version)
    typer.echo(f"✔ Now using Node.js v{version} (persistent)")


@app.command()
def current():
    """Show the currently active Node.js version."""
    version = load_config()
    if version:
        typer.echo(f"✔ Current Node.js version: {version}")
    else:
        typer.echo("❌ No Node.js version is currently active.")


@app.command()
def remove(version: str):
    """Uninstall a specific Node.js version."""
    version_dir = VERSIONS_DIR / version
    if not version_dir.exists():
        typer.echo(f"❌ Node.js v{version} is not installed.")
        return

    typer.echo(f"🗑 Removing Node.js v{version}...")
    shutil.rmtree(version_dir)

    # Reset PATH if the removed version was active
    if load_config() == version:
        save_config("")  # Clear current version
        update_user_path("")  # Reset PATH
        typer.echo("✔ PATH reset.")

    typer.echo(f"✔ Node.js v{version} removed.")


GITHUB_REPO = "dkuwcreator/win-nvm"

def fetch_latest_version():
    """Retrieve the latest version from GitHub releases."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()["tag_name"].lstrip("v")
    except requests.RequestException:
        return None  # Fail gracefully if the request fails

@app.command()
def version():
    """Show the wnvm CLI version and check for updates."""
    typer.echo(f"wnvm version {__version__ or 'dev'}")

    # Fetch the latest release from GitHub
    latest_version = fetch_latest_version()

    if latest_version and latest_version != __version__:
        typer.echo(f"⚠ A new version ({latest_version}) is available!")
        typer.echo("Update by running:")
        typer.echo("  iwr -useb https://raw.githubusercontent.com/dkuwcreator/win-nvm/main/install.ps1 | iex")
        
if __name__ == "__main__":
    app()
