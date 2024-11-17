from setuptools import setup, find_packages


setup(
    name="nex",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        'grpcio-tools',
    ],
    author="Retendo Contributors",
    description="NEX Library of NEX Server for Wii U & 3DS.", 
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)