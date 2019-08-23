from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["kubernetes==10.0.0", "pandas"]

setup(
    name="kubernetes-resource-monitor",
    version="1.0.5",
    license='MIT',
    author="Tan Zheng Wei",
    author_email="tanzhengwei143@gmail.com",
    description="Package contains a client that can be used to interface with KRM Api service.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/zhengwei143/kubernetes-resource-monitor",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
