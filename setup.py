import os
from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(os.path.abspath("setup.py"))

setup(
    name='gemini-api-automation',
    extras_require=dict(tests=['pytest']),
    packages=find_packages(where=['src']),
    package_dir={"": "src"}
)
