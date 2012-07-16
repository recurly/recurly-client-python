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
    description="Interact with Recurly's REST API for subscription management from your Python website",
    long_description=DESCRIPTION,
    author='Recurly',
    author_email='support@recurly.com',
    url='http://docs.recurly.com/client-libraries/python',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=['recurly'],
    install_requires=['iso8601', 'backports.ssl_match_hostname'] + more_install_requires,
    tests_require=['mock',
                   'unittest2'],
    test_suite='unittest2.collector',
    zip_safe=True,
)
