from setuptools import setup

setup(
    name='load_balancer',
    version='1',
    packages=['load_balancer'],
    url='https://github.com/Craxti/load_balancer',
    license='MIT License',
    author='Craxti',
    author_email='fetis.dev@gmail.com',
    description='Load Balancer Python package',
    classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
    install_requires=[
        'requests',
        'aiohttp',
        'aiosignal',
        'async-timeout',
        'attrs',
        'certifi',
        'charset-normalizer',
        'colorama',
        'frozenlist',
        'idna',
        'iniconfig',
        'multidict',
        'notifications',
        'packaging',
        'pluggy',
        'prometheus-client',
        'pytest',
        'pytest-mock',
        'python-dotenv',
        'PyYAML',
        'requests',
        'urllib3',
        'yarl',

    ],
)
