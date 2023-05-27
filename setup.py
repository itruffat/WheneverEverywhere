from setuptools import setup

with open("version.info") as info_file:
    version = info_file.read()



setup(
    name='WheneverEverywhere',
    version=version,
    author='itruffat',
    description='A python-interpreter and compiler for the Whenever language.',
    long_description='A python-interpreter and compiler for the Whenever language, allowing the user to run it' +
                     'on python or transpile it into C code for latter merging',
    long_description_content_type='text/markdown',
    url='https://github.com/itruffat/WheneverEverywhere',
    packages=['WheneverEverywhere', 'WheneverEverywhere.whenever_parser', 'WheneverEverywhere.whenever_interpreter',
                'WheneverEverywhere.whenever_c_transpiler', 'WheneverEverywhere.whenever_interpreter'],
    package_dir={'': 'src'},
    package_data={
        'WheneverEverywhere.whenever_c_transpiler': ['template.c']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
