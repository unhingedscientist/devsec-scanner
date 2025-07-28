from setuptools import setup, find_packages

setup(
    name='devsec-scanner',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'click',
        'boto3',
        'pymongo',
        'openai',
    ],
    entry_points={
        'console_scripts': [
            'devsec-scan=devsec_scanner.cli:main',
        ],
    },
    include_package_data=True,
    description='Developer-first security scanner for exploitable vulnerabilities',
    author='Your Name',
    url='https://github.com/yourusername/devsec-scanner',
)
