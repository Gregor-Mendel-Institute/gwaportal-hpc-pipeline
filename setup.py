from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='gwaportal-hpc-pipeline',
    version='0.1.0',
    description='Analysis-pipeline for GMI GWA-Portal (HPC)',
    long_description=readme,
    author='Uemit Seren',
    author_email='uemit.seren@gmi.oeaw.ac.at',
    url='https://github.com/Gregor-Mendel-Institute/gwaportal-hpc-pipeline',
    license=license,
    keywords='GWAS',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        "celery >= 4.3.0",
	    "fabric >=2.5.0",
        "requests >=2.22.0",
        "h5py >= 2.10",
    ]
)
