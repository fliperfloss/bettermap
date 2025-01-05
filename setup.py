from setuptools import setup, find_packages

setup(
    name="NmapScanner",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'colorama',  # Required for color printing
    ],
    entry_points={
        'console_scripts': [
            'nmap-scanner = your_script_name:main',  # Replace 'your_script_name' with the actual name of your Python script file without the .py extension
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A script for scanning IP addresses using Nmap",
    long_description=open('README.md').read(),  # Ensure you have a README.md for long description
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nmap-scanner",  # Update with your GitHub URL if applicable
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
