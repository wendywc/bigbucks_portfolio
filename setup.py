from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'bigbucks_port',
    version = '0.0.4',
    author = 'Wenjie Cui',
    description= "A package used for portfolio analysis in Fintech512",
    long_description=long_description,
    long_description_content_type="text/markdown"
)