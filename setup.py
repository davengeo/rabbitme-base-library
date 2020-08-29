from setuptools import setup, find_namespace_packages

setup(
    author="David Navarro",
    author_email="me@davengeo.com",
    description="rabbitmq-multipoint-provisioning dist",
    name="rabbitmq-multipoint-provisioning",
    data_files=[('ini', ['app.ini']), ('make', ['Makefile']), ('templates', [
        'app/resources/environments.json',
        'app/resources/templates/exchanges/fanout.json',
        'app/resources/templates/exchanges/topic.json',
        'app/resources/templates/permissions/conventional.json',
        'app/resources/templates/policies/dead-letter-policy.json',
        'app/resources/templates/queues/sample-queue.json'
    ])],
    packages=find_namespace_packages(where="lib"),
    packages_dir={"": "lib"},
    install_requires=['requests', 'argparse', 'pyramda', 'rabbitpy'],
)
