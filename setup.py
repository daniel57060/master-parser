from setuptools import setup, find_packages

setup(
    name="c_inspectors",
    version="0.1",
    packages=find_packages(exclude=["tests"]),
    install_requires=["tree-sitter"],
    entry_points={
        'console_scripts': [
            'c_inspectors = c_inspectors.cli:main',
        ],
    },
)
