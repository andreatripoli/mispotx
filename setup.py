import setuptools


setuptools.setup(
    name="mispotx",                     # This is the name of the package
    version="1.0.0",                        # The initial release version
    author="Andrea Tripoli",                     # Full name of the author
    description="A tool to push OTXs to MISP",
    long_description="A tool to extract pulses from AlienVault and push them into your MISP instance",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Topic :: Utilities",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["src"],             # Name of the python package
    package_dir={'': 'src'},     # Directory of the source code of the package
    install_requires=[
        'pymisp>=2.4.183',
        'OTXv2>=1.5.12',
        'python-dateutil'
    ],                    # Install other dependencies if any
    license='MIT',                          # License
    url='https://github.com/andreatripoli/mispotx',
    keywords=[
        'MISP', 'OTX', 'AlienVault'
    ],
)
