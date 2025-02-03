# Parse command-line arguments
param (
    [string]$UserPath = "dist",
    [switch]$Uninstall
)

# Load environment variables from .env if available
$envFilePath = "project.env"
if (Test-Path $envFilePath) {
    Get-Content $envFilePath | ForEach-Object {
        $var = $_ -split '=', 2
        if ($var.Length -eq 2) {
            Set-Item -Path "Env:$($var[0].Trim())" -Value $var[1].Trim()
        }
    }
}

# Constants (Loaded from .env or default values)
$OUTPUT_NAME = $env:OUTPUT_NAME ?? "example"
$DIST_DIR = $env:DIST_DIR ?? "dist"

# Function to update PATH environment variable
function Update-Path {
    param (
        [string]$TargetPath,
        [switch]$Remove
    )
    
    $userPath = [System.Environment]::GetEnvironmentVariable("PATH", "User")
    if (-not $userPath) {
        Write-Host "User PATH environment variable not found. Using an empty PATH."
        $userPath = ""
    }

    if ($Remove) {
        if ($userPath -match [regex]::Escape($TargetPath)) {
            Write-Host "Removing $TargetPath from PATH..."
            $newPath = ($userPath -split ";" | Where-Object {$_ -ne $TargetPath}) -join ";"
            [System.Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
            Write-Host "Removed $TargetPath from PATH. Restart your terminal or system for changes to take effect."
        } else {
            Write-Host "$TargetPath not found in PATH. Skipping removal."
        }
    } else {
        if ($userPath -notmatch [regex]::Escape($TargetPath)) {
            Write-Host "Adding $TargetPath to PATH..."
            $newPath = if ($userPath) { "$userPath;$TargetPath" } else { $TargetPath }
            [System.Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
            Write-Host "Added $TargetPath to PATH. Restart your terminal or system for changes to take effect."
        } else {
            Write-Host "$TargetPath is already in PATH. Skipping addition."
        }
    }
}

# Function to install the executable
function Install-App {
    param (
        [string]$UserPath = $DIST_DIR
    )

    # Resolve absolute path
    $destPath = Resolve-Path -ErrorAction SilentlyContinue $UserPath
    if (-not $destPath) {
        New-Item -ItemType Directory -Path $UserPath -Force | Out-Null
        $destPath = Resolve-Path $UserPath
    }

    $executable = "$DIST_DIR\$OUTPUT_NAME.exe"
    if (-not (Test-Path $executable)) {
        Write-Host "Error: Executable not found in '$DIST_DIR'. Run the build step first."
        exit 1
    }

    # Check if the source and destination paths are the same
    if ($executable -ne "$destPath\$OUTPUT_NAME.exe") {
        # Copy the executable to the destination path
        Copy-Item -Path $executable -Destination $destPath -Force
        Write-Host "Installed $OUTPUT_NAME to $destPath."
    } else {
        Write-Host "$OUTPUT_NAME is already in the destination path. Skipping copy."
    }

    # Add directory to PATH
    Update-Path -TargetPath $destPath

    # Update current session's PATH
    $env:PATH = "$env:PATH;$destPath"
    Write-Host "Installation complete. You may need to restart your terminal for PATH changes to take effect."
}

# Function to uninstall the executable
function Uninstall-App {
    param (
        [string]$UserPath = $DIST_DIR
    )

    $destPath = Resolve-Path -ErrorAction SilentlyContinue $UserPath
    if (-not $destPath) {
        Write-Host "Error: Directory $UserPath does not exist. Skipping uninstallation."
        return
    }

    $executable = "$destPath\$OUTPUT_NAME.exe"
    if (Test-Path $executable) {
        Remove-Item -Path $executable -Force
        Write-Host "Removed $OUTPUT_NAME from $destPath."
    } else {
        Write-Host "Executable not found in $destPath. Skipping removal."
    }

    # Remove directory from PATH
    Update-Path -TargetPath $destPath -Remove
}

if ($Uninstall) {
    Uninstall-App -UserPath $UserPath
} else {
    Install-App -UserPath $UserPath
}

# Ensure PATH updates reflect immediately in the session
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
