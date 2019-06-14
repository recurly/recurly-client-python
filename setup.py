import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recurly",
    version="3.0b2",
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
