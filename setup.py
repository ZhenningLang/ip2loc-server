# -*- coding: utf-8 -*-

import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    install_requires = [req for req in f.read().split('\n') if req]


setuptools.setup(
    name="ip2loc_server",
    version="1.0.0dev1",
    author="ZhenningLang",
    author_email="zhenninglang@163.com",
    description="A tiny web server for ipv4 to geo location conversion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZhenningLang/ip2loc_server",
    packages=setuptools.find_packages('./src'),
    python_requires='>=3.5',
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        '': ['*.ZIP', 'data_version'],
    },
    entry_points={
        'console_scripts': [
            'ip2loc = ip2loc_server:entry',
        ]
    },
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
