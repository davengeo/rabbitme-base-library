from setuptools import setup, find_namespace_packages

setup(
    author="David Navarro Alvarez",
    author_email="me@davengeo.com",
    description="rabbitmq-base-library dist",
    name="rabbitmq-base-library",
    data_files=[('ini', ['app.ini']), ('make', ['Makefile'])],
    packages=find_namespace_packages(include=["lib.*"]),
    install_requires=['requests', 'argparse', 'pyramda', 'rabbitpy'],
)
