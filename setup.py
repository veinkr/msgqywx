# coding:utf8
from os import path

from setuptools import setup

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="msgqywx",
    version="0.6.0",
    description="发送企业微信应用消息",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="demon finch",
    author_email="yhf2lj@outlook.com",
    license="MIT",
    url="https://github.com/veink-y/msgqywx",
    keywords="企业微信 消息",
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["msgqywx"],
)
