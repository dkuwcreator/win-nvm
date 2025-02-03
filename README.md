# win-nvm

**Version:** 0.1.0  
**Author:** Derk Kappelle  
**Email:** [derk.kappelle@uw-api.com](mailto:derk.kappelle@uw-api.com)  
**Repository:** [GitHub - win-nvm](https://github.com/dkuwcreator/windows-nvm.git)

## Description

`win-nvm` is a **No-Admin Windows version** of the **Node Version Manager (nvm)** tool. It allows users to install, manage, and switch between different versions of Node.js without requiring administrative privileges.

## Features

- Install Node.js versions without admin rights.
- Persistently switch Node.js versions using Windows user-level environment variables.
- Automatic PATH updates for seamless integration.
- Uses `typer` for a modern CLI and `InquirerPy` for interactive selections.
- Supports interactive fuzzy search for selecting Node.js versions.
- Minimalistic and fast, with a simple YAML-based configuration option.
- Includes a `build.py` script for generating new builds.
- Provides a PowerShell install script for easier setup.
- Supports virtual environments for clean dependency management.

## Installation

### **Prerequisites**
- Windows 10 or later
- No admin rights required
- `Python 3.8+` (only needed for manual build)

### **Installing via PowerShell Script (Recommended)**
The easiest way to install `win-nvm` is using the provided PowerShell script:

```powershell
iwr -useb https://raw.githubusercontent.com/dkuwcreator/windows-nvm/main/install.ps1 | iex
```

This will:
- **Download and install `wnvm.exe`** in your user directory (`%LOCALAPPDATA%\wnvm`).
- **Automatically update the PATH** so `wnvm` can be used immediately.

To verify the installation:
```powershell
wnvm --version
```

### **Uninstalling**
If you want to remove `win-nvm`, run:
```powershell
install.ps1 -Uninstall
```

### **Manual Installation**
Alternatively, you can download the latest release manually:
1. **Download the latest release** from [GitHub Releases](https://github.com/dkuwcreator/windows-nvm/releases/latest).
2. **Extract the `wnvm.exe`** to a location of your choice (e.g., `C:\Users\YourName\wnvm`).
3. **Add the folder to your Windows PATH** manually.

### **Building from Source**
If you want to build `win-nvm` yourself:
```sh
git clone https://github.com/dkuwcreator/windows-nvm.git
cd windows-nvm
pip install -r requirements.txt
python build.py --clean
```
The executable will be available in the `dist/` folder.

## Usage

### **Listing Available Node.js Versions**
```sh
wnvm available
```

### **Installing a Node.js version**
```sh
wnvm install 18.16.0
```
Or interactively select a version:
```sh
wnvm install
```

### **Switching to a specific Node.js version**
```sh
wnvm use 18.16.0
```
Or interactively select a version:
```sh
wnvm use
```

### **Listing installed Node.js versions**
```sh
wnvm list
```

### **Checking the currently active version**
```sh
wnvm current
```

### **Removing a Node.js version**
```sh
wnvm remove 16.13.0
```

## How It Works

- `win-nvm` downloads and extracts Node.js versions into the user directory.
- Updates the **user-level** Windows PATH variable (no admin required).
- Uses `typer` for a clean CLI experience and `InquirerPy` for interactive selection.
- Implements interactive selection using `InquirerPy`.
- The selected Node.js version remains active across terminal sessions.

## Development

### **Setting Up a Development Environment**
```sh
git clone https://github.com/dkuwcreator/windows-nvm.git
cd windows-nvm
pip install -r requirements.txt
```

### **Running from Source**
```sh
python wnvm/cli.py --help
```

### **Building an Executable**
To create a standalone executable using `build.py`:
```sh
python build.py --clean
```
The built executable will be available in the `dist/` directory.

### **Build System Details**
The `build.py` script ensures:
- A clean build by removing previous artifacts.
- A virtual environment is created if not already present.
- Dependencies are installed automatically.
- The executable is built using `pyinstaller`.

If `pyinstaller` is not installed, install it using:
```sh
pip install pyinstaller
```

## Contributing

Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request.

## License

This project is licensed under the **MIT License**.

---
For more details, visit the [GitHub Repository](https://github.com/dkuwcreator/windows-nvm.git).

