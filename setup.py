from setuptools import setup

setup(
    name='pystructural',
    version='0.1',
    packages=['pystructural', 'pystructural.core', 'pystructural.elements', 'pystructural.geometry',
              'pystructural.core_systems'],
    url='https://github.com/RikHendriks/pystructural',
    license='GNU General Public License v3.0',
    author='Rik Hendriks',
    author_email='rikhendriks@rocketmail.com',
    description='A structural finite element method implementation'
)