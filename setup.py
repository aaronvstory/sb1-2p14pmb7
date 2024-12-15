"""Setup configuration for the package."""
from setuptools import setup, find_packages

setup(
    name="doordash-automation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "undetected-chromedriver",
        "selenium",
        "rich",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "doordash-automation=src.main:main",
        ],
    },
    python_requires=">=3.8",
)