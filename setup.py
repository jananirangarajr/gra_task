from os import path
from codecs import open as codopen
from setuptools import setup


current_path = path.abspath(path.dirname(__file__))


with codopen(path.join(current_path, 'requirements.txt'), encoding='utf-8') as f:
    requirement_list = f.read().split('\n')
install_requires = [x.strip() for x in requirement_list]

setup(
    name='GRA_task',
    version='1.0',
    author='Janani Rangaraj',
    description='Technical interview for GRA',
    url='https://github.com/',
    license='Apache 2.0',
    entry_points={
        'console_scripts': [
            'run-aws-local=gra_task.run_aws_local:main'
            ]
    },
    include_package_data=True,
    install_requires=install_requires,
)