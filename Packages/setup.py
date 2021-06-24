from setuptools import setup,find_packages

setup(
        name = 'Ptolemy',
        version = '0.1',
        packages = find_packages(),
        author = 'shihua',
        description = 'Ptolemy Module',
         install_requires = ['influxdb']
)