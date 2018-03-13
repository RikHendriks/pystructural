from setuptools import setup

setup(
    name='pystructural',
    version='0.1',
    packages=['pystructural', 'pystructural.core', 'pystructural.core.elements', 'pystructural.core.materials',
              'pystructural.core.geometries', 'pystructural.core.core_systems', 'pystructural.core.core_components',
              'pystructural.core.element_geometries', 'pystructural.core.additional_components'],
    url='https://github.com/RikHendriks/pystructural',
    license='GNU General Public License v3.0',
    author='Rik Hendriks',
    author_email='rikhendriks@rocketmail.com',
    description='A structural finite element method implementation'
)