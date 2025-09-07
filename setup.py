from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="Python.Trading.Indicators",
    version="0.1.0",
    author="venantvr",
    author_email="venantvr@gmail.com",
    description="A comprehensive Python library for technical analysis indicators used in algorithmic trading",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/venantvr/Python.Trading.Indicators",
    project_urls={
        "Bug Tracker": "https://github.com/venantvr/Python.Trading.Indicators/issues",
        "Repository": "https://github.com/venantvr/Python.Trading.Indicators.git",
        "Documentation": "https://Python.Trading.Indicators.readthedocs.io/",
    },
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-xdist>=3.0.0",
        ],
    },
    keywords=[
        "trading",
        "technical-analysis",
        "indicators", 
        "finance",
        "rsi",
        "candlestick",
        "volatility",
        "algorithmic-trading",
    ],
    include_package_data=True,
    zip_safe=False,
)
