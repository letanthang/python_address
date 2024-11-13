from setuptools import setup, find_packages

setup(
    name='python_address',
    version='0.1.2',
    description='A Python library for address parsing and validation.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Le Tan Thang',
    author_email='letanthang@gmail.com',
    url='https://github.com/letanthang/python_address',
    package_data={
        'python_address': ['assets/wards.csv'],  # Specifies the files to include
    },
    packages=find_packages(),
    install_requires=[],
)