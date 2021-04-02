#!/usr/bin/env python

# ===============================================================
# IBM Confidential
#
# OCO Source Materials
#
# Copyright IBM Corp. 2019
#
# The source code for this program is not published or otherwise
# divested of its trade secrets, irrespective of what has been
# deposited with the U.S. Copyright Office.
# ===============================================================

from setuptools import setup, find_packages

desc = 'Chart Library module'

with open('requirements.txt') as fp:
    reqs = fp.read().splitlines()

setup(
    name='amhairc',
    version="0.1.2",
    description=('Chart Library module'),
    long_description=desc,
    url='https://github.ibm.com/fd4b-agrotech-incubator/analytics-base.git',
    author='FD4B NONP',
    author_email='fd4bnonp@us.ibm.com',
    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
    keywords='',
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    install_requires=reqs,
    package_data={},
    data_files=[]
)
