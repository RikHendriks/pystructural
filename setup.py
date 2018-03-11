from setuptools import setup

setup(
    name='pystructural',
    version='0.1',
    packages=['pystructural', 'pystructural.elements', 'pystructural.geometries', 'pystructural.materials',
              'pystructural.core_systems', 'pystructural.core_components', 'pystructural.element_geometries',
              'pystructural.additional_components'],
    url='https://github.com/RikHendriks/pystructural',
    license='GNU General Public License v3.0',
    author='Rik Hendriks',
    author_email='rikhendriks@rocketmail.com',
    description='A structural finite element method implementation'
)