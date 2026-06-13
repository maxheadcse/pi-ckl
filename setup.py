#!/usr/bin/env python3

"""
Setup script for Pi Coding Agent Configuration Tool
"""

import os
from setuptools import setup, find_packages

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read README
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pi-coding-agent-configurator',
    version='1.0.0',
    author='Pi Coding Agent Team',
    author_email='support@pi-coding-agent.com',
    description='A robust, menu-driven and CLI-capable configuration tool for the Pi Coding Agent',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/maxheadcse/pi-configurator',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pi-config = main:main',
            'pi-configurator = main:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Utilities',
    ],
    python_requires='>=3.8',
    keywords='pi coding agent configuration cli menu tool',
    project_urls={
        'Source': 'https://github.com/maxheadcse/pi-configurator',
        'Bug Tracker': 'https://github.com/maxheadcse/pi-configurator/issues',
        'Documentation': 'https://github.com/maxheadcse/pi-configurator/blob/master/README.md',
    },
)