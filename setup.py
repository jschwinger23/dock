from setuptools import setup
from setuptools import find_packages

REQUIREMENTS = [
    'click',
]

setup(
    name='dock',
    version='0.1.0',
    description='Docker by Python',
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    entry_points={'console_scripts': ['dock=dock.cli:main']},
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=False)
