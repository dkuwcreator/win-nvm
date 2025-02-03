from setuptools import setup, find_packages
from pathlib import Path
from dotenv import dotenv_values
import os

# Load environment variables from .env file
from dotenv import dotenv_values

config = dotenv_values("project.env")

# Read project metadata from .env (fallback values included)
PROJECT_NAME = config.get("PROJECT_NAME", "example_project")
ENTRY_SCRIPT = config.get("ENTRY_SCRIPT", "example_project")
OUTPUT_NAME = config.get("OUTPUT_NAME", "example_project")
AUTHOR = config.get("AUTHOR", "John Doe")
AUTHOR_EMAIL = config.get("AUTHOR_EMAIL", "john.doe@example.com")
DESCRIPTION = config.get("DESCRIPTION", "An example project description.")
URL = config.get("URL", "https://example.com")

# Read version from wnvm/.version file
version_file_path = Path(".version")
if version_file_path.is_file():
    VERSION = version_file_path.read_text().strip()
else:
    VERSION = "dev"  # Fallback version

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read dependencies from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as req_file:
    install_requires = [line.strip() for line in req_file if line.strip() and not line.startswith("#")]

setup(
    name=PROJECT_NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=install_requires,  # Use requirements.txt dependencies
    entry_points={
        "console_scripts": [
            f"{OUTPUT_NAME}={OUTPUT_NAME}.cli:app",
        ],
    },
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.7",
    license_files=("LICENSE",),
    keywords=["azure", "CLI", "Azure portal", "Azure subscriptions"],
)
