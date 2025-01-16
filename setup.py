import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='netsuitesdk',
    version='2.7.5',
    author='Simao Moreira',
    author_email='smoreira@broadvoice.com',
    description='Python SDK for accessing the NetSuite SOAP webservice',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['netsuite', 'api', 'python', 'sdk'],
    url='https://github.com/simapedro/bi-netsuite-sdk',
    packages=setuptools.find_packages(),
    install_requires=['zeep'],
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
