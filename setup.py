from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    lic = f.read()

setup(
    name='pystructural',
    version='0.1',
    description='A structural finite element method implementation.',
    long_description=readme,
    author='Rik Hendriks',
    author_email='rikhendriks@rocketmail.com',
    url='https://github.com/RikHendriks/pystructural',
    license=lic,
    packages=find_packages(),
    install_requires=[
            'numpy',
            'catecs',
            'matplotlib',
            'bokeh',
            'svgpathtools',
        ]
)
