# setup.py

# from setuptools import setup, find_packages

# setup(
#     name="rag_sdk",
#     version="0.1.0",
#     packages=find_packages(),
#     install_requires=[
#         "requests",
#     ],
#     author="Akshay Kumar Pasupunooti",
#     author_email="pasupunootiakshay1@gmail.com",
#     description="Python SDK for interacting with RAG backend",
#     url="https://github.com/yourusername/rag_sdk",
#     classifiers=[
#         "Programming Language :: Python :: 3",
#     ],
# )
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rag_sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.7",
    author="Akshay Kumar Pasupunooti",
    author_email="pasupunootiakshay1@gmail.com",
    description="Python SDK for interacting with RAG backend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rag_sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
