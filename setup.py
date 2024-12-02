from setuptools import setup, find_packages

setup(
    name="sample_messaging_sdk",
    version="0.1.0",
    description="SDK for the assessment sample messaging API",
    author="Talal AWija",
    author_email="talal.awija@gmail.com",
    url="",
    packages=find_packages(),
    install_requires=[
        "requests>=2.26.0",
        "pydantic>=1.8"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT LIcense",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"

)