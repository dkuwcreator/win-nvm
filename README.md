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

- Python 3.8 or later
- Windows 10 or later
- `pip` package manager

### **Installation from Source**

Currently, `win-nvm` is not available on PyPI. You can install it manually from the repository:

```sh
git clone https://github.com/dkuwcreator/windows-nvm.git
cd windows-nvm
pip install .
```

Alternatively, you can clone the repository and install locally:

```sh
git clone https://github.com/dkuwcreator/windows-nvm.git
cd windows-nvm
pip install .
```

### **Installing via PowerShell Script**

For an easier setup, use the provided PowerShell install script:

```powershell
.\install.ps1
```

This script will set up `win-nvm` without requiring additional manual steps.

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
