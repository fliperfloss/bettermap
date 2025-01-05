from setuptools import setup, find_packages

setup(
    name='BetterMap',  # Your project name
    version='0.1',
    description='A simple Nmap scanner with multiple options.',
    author='biskit',  # Replace with your name
    author_email='your.email@example.com',  # Replace with your email
    packages=find_packages(),  # Automatically finds your project packages
    install_requires=[
        'colorama',  # Add other dependencies here if needed
    ],
    entry_points={
        'console_scripts': [
            'bettermap = bettermap.main:main',  # Replace 'bettermap.main:main' with the entry point to your main function
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the minimum Python version required
)
