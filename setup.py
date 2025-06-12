from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="InvoiceReimbursementSystem",
    version="0.0.1",
    author="Sahil Rahate",
    author_email="sahilrahate567@gmail.com",
    packages=find_packages(),
    install_requires=requirements
)