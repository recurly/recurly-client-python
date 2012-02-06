from distutils.core import setup

setup(
    name='recurly',
    version='2.0.4',
    description="Interact with Recurly's REST API for subscription management from your Python website",
    author='Recurly',
    author_email='support@recurly.com',
    url='http://docs.recurly.com/client-libraries/python',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],

    packages=['recurly'],
    requires=['iso8601'],
)
