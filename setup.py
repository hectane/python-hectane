from setuptools import setup, find_packages


setup(
    name='pycannon',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'six',
    ],
    author='Nathan Osman',
    author_email='nathan@quickmediasolutions.com',
    description="Python module for sending emails with go-cannon",
    license='MIT',
    url='https://github.com/nathan-osman/pycannon',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
