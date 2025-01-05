from setuptools import setup, find_packages
import os

# Function to read version from a version file or static value
def read_version():
    version = "0.1"  # Change this when updating the version
    return version

# Read the long description from the README file
def read_long_description():
    with open("README.md", "r") as fh:
        return fh.read()

# Define the required dependencies
def read_requirements():
    requirements = []
    with open("requirements.txt", "r") as fh:
        requirements = [line.strip() for line in fh.readlines()]
    return requirements

# Setup function
setup(
    name="bettermap",  # Name of the package
    version=read_version(),  # Version of the package
    author="biskit",  # Replace with your name
    author_email="your.email@example.com",  # Replace with your email
    description="A Python-based Nmap scanner with customizable features.",
    long_description=read_long_description(),  # Pulls from the README.md
    long_description_content_type="text/markdown",  # Tells that it's markdown format
    url="https://github.com/fliperfloss/bettermap",  # Replace with your repo URL
    packages=find_packages(),  # Automatically find packages in the current directory
    classifiers=[  # Additional metadata
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Ensure compatibility with Python 3.6 and above
    install_requires=read_requirements(),  # Read dependencies from requirements.txt
    entry_points={  # Makes the script executable from the command line
        'console_scripts': [
            'bettermap = bettermap:main',  # Entry point to the main function
        ],
    },
    include_package_data=True,  # Ensures additional files (like README) are included
    zip_safe=False,  # Indicates that the package can be reliably used from a zip file
)
