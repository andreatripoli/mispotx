from glob import glob

import setuptools
from setuptools import find_packages
from os.path import splitext, basename


setuptools.setup(
    name="mispotx",                     # This is the name of the package
    version="1.2.0",                        # The initial release version
    author="Andrea Tripoli",                     # Full name of the author
    description="A tool to push OTXs to MISP",
    long_description="A tool to extract pulses from AlienVault and push them into your MISP instance",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Topic :: Utilities",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.9',                # Minimum version requirement of the package
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/mispotx/util/*', recursive=True)],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pymisp>=2.4.183',
        'OTXv2>=1.5.12'
    ],          # Install other dependencies if any
    license='MIT',                          # License
    url='https://github.com/andreatripoli/mispotx',
    keywords=[
        'MISP', 'OTX', 'AlienVault'
    ],
    package_data={
        'mispotx': ['config.ini'],
    },
    entry_points={
        'console_scripts': ['mispotx=mispotx.cli:main'],
    }
)
