from distutils.core import setup
from setuptools import find_packages

setup(
    name='module-symbols',
    version='1.0.0',
    description='Linux module licence compliance analyzer',
    author='Peter M. Petrakis',
    author_email='peter.petrakis@gmail.com',
    license='GPL',
    install_requires=[
        'PyYAML',
        'setuptools',
        ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'module-symbols = module_symbols.cli:main',
        ],
        },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP", # XXX change
        ],
    )
