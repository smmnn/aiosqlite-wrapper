from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
desc = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="aiosqlite-wrapper",
    version="0.0.2",
    description="a simple async wrapper for aiosqlite.",
    long_description=desc,
    long_description_content_type="text/markdown",
    author="smmnn",
    url="https://github.com/smmnn/aiosqlite-wrapper",
    python_requires=">=3.6",
    install_requires=['aiosqlite'],
    packages=['aiosqlite_wrapper'],
)