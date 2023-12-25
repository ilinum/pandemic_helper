from setuptools import setup

setup(
    name='pandemic_helper',
    version='0.1.0',
    py_modules=['helper_cli'],
    install_requires=[
        'Click',
        'Termcolor'
    ],
    entry_points={
        'console_scripts': [
            'pandemic_helper = helper_cli:cli',
        ],
    },
)