from setuptools import setup

setup(
    name='REC_Database_Cleaner',
    version='1.1.3',
    description='Takes the REC database survey from qualtrics and cleans/reorders the columns.',
    author='Chanteria Milner',
    packages=['app'],
    package_data={
        'app': ['templates/*.html'],
    },
    include_package_data=True,
    install_requires=[
        'Flask',
        'pandas',
        # Add any other dependencies your application requires
    ],
)






