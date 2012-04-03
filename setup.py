from setuptools import setup
import os.path

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as README:
    DESCRIPTION = README.read()

setup(
    name='recurly',
    version='2.1.1',
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
    install_requires=['iso8601'],
    tests_require=['mock',
                   'unittest2'],
    test_suite='unittest2.collector',
    zip_safe=True,
)
