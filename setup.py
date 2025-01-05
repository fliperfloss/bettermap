import os
import sys
from setuptools import setup, find_packages
from subprocess import call

# Function to install required dependencies for Linux and Windows
def install_requirements():
    try:
        if sys.platform == "win32":
            print("Windows detected. Installing Windows-specific dependencies...")
            # On Windows, we'll install 'colorama' and 'msvcrt' (for compatibility with Windows)
            call([sys.executable, "-m", "pip", "install", "colorama"])

        elif sys.platform == "linux" or sys.platform == "linux2":
            print("Linux detected. Installing Linux-specific dependencies...")
            # On Linux, we install 'colorama' (msvcrt doesn't exist on Linux)
            call([sys.executable, "-m", "pip", "install", "colorama"])

        else:
            print(f"Unsupported OS: {sys.platform}. Please install dependencies manually.")
            return

    except Exception as e:
        print(f"Error during installation: {e}")
        sys.exit(1)

# Call the install_requirements function
install_requirements()

# Setup the package installation
setup(
    name="bettermap",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'colorama',  # Required package for cross-platform colored output
    ],
    entry_points={
        'console_scripts': [
            'bettermap = bettermap:main',  # This is the main function in your script
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

# Finish with a message
print("Installation complete. You can now use the 'bettermap' command in your terminal.")
