from setuptools import setup, find_packages


setup(
    name='pycannon',
    version='0.1.0',
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
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ],
)
