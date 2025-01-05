from setuptools import setup, find_packages
import os

# Check platform to conditionally add dependencies
if os.name == 'nt':  # For Windows
    extra_requirements = ['msvcrt']
else:  # For Linux/Unix
    extra_requirements = ['curses']

setup(
    name='bettermap',
    version='0.1',
    description='A better Nmap automation script',
    author='Your Name',
    author_email='your_email@example.com',
    packages=find_packages(),
    install_requires=[
        'colorama',  # Cross-platform color support
    ],
    extras_require={
        'platform-specific': extra_requirements,  # Platform-specific dependencies
    },
    entry_points={
        'console_scripts': [
            'bettermap=bettermap:main',  # Entry point to your script
        ],
    },
)
