from setuptools import setup
import os.path
import re

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as README:
    DESCRIPTION = README.read()

VERSION_RE = re.compile("^__version__ = '(.+)'$",
                        flags=re.MULTILINE)
with open(os.path.join(os.path.dirname(__file__),
                       'recurly', '__init__.py')) as PACKAGE:
    VERSION = VERSION_RE.search(PACKAGE.read()).group(1)

more_install_requires = list()
try:
    import ssl
except ImportError:
    more_install_requires.append('ssl')

setup(
    name='recurly',
    version=VERSION,
    description="The official Recurly API client",
    long_description=DESCRIPTION,
    author='Recurly',
    author_email='support@recurly.com',
    url='https://github.com/recurly/recurly-client-python',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=['recurly'],
    install_requires=['iso8601', 'backports.ssl_match_hostname', 'six>=1.4.0', 'defusedxml'] + more_install_requires,
    tests_require=['mock',
                   'six',
                   'unittest2',
                   'defusedxml'],
    test_suite='unittest2.collector',
    zip_safe=True,
)
