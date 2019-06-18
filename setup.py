import setuptools
import re
import os.path

# get version from top level __init__ file
VERSION_RE = re.compile('^__version__ = "(.+)"$', flags=re.MULTILINE)
with open(os.path.join(os.path.dirname(__file__), "recurly", "__init__.py")) as PACKAGE:
    VERSION = VERSION_RE.search(PACKAGE.read()).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recurly",
    # version managed in recurly/__init__.py
    version=VERSION,
    author="Benjamin Eckel",
    author_email="ben@recurly.com",
    description="Recurly v3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/recurly/recurly-client-python",
    packages=setuptools.find_packages(),
    classifiers=[],
    tests_require=["coverage"],
)
