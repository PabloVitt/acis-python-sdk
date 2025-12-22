"""
ACIS Trading Python SDK

Install with: pip install acis-trading
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="acis-trading",
    version="1.0.0",
    author="ACIS Trading",
    author_email="support@acis-trading.com",
    description="Python SDK for ACIS Trading API - AI-powered stock portfolio generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acis-trading/acis-python-sdk",
    project_urls={
        "Documentation": "https://acis-trading.com/api-docs",
        "Homepage": "https://acis-trading.com",
        "Bug Tracker": "https://github.com/acis-trading/acis-python-sdk/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "responses>=0.23.0",
        ],
    },
    keywords=[
        "acis",
        "trading",
        "stock",
        "portfolio",
        "ai",
        "machine-learning",
        "investment",
        "fintech",
        "api",
        "quantitative",
    ],
)
