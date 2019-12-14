from setuptools import setup, find_packages

setup(
    name='py2latex',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    description='Convert pandas dataframes to LaTeX tables',
    long_description=open('README.md').read(),
    install_requires=['pandas'],
    url='https://github.com/KarlNaumann/Py2LaTeX',
    author='Karl Naumann',
)