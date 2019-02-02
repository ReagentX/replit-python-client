from setuptools import setup, find_packages

setup(
    name='replit-api',
    version='1.0',
    description='A Python 3 API for Repl.it',
    author='Christopher Sardegna',
    author_email='github@reagentx.net',
    install_requires=['requests', 'requests-cache'],
    packages=find_packages(),
    scripts=[]
)