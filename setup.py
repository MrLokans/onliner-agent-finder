import re
from setuptools import (
    setup,
    find_packages
)

version = ""

requirements = []
# I actually took it from requests library
with open('agent_spider/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

if not version:
    raise ValueError("No version specified.")

setup(
    name="onliner_spider_agent",
    version=version,
    url='https://github.com/MrLokans/onliner-agent-finder',
    download_url='https://github.com/MrLokans/onliner-agent-finder/tarball/{}'.format(version),
    author='MrLokans',
    author_email='mrlokans@gmail.com',
    license='MIT',
    packages=find_packages(exclude=["tests"]),
    entry_points={
        'console_scripts': [
            'onliner_agent_finder = agent_spider.run:main'
        ]
    },
    install_requires=requirements,
    classifiers=(
        'Intended Audience :: Developers, Data Scientists',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
    zip_safe=False
)
