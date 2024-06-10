from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()
        requirements = [line for line in lines if line and not line.startswith("#")]
    return requirements


def get_readme_content():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="api-to-dataframe",
    version="v0.0.1",
    packages=find_packages(),
    author="Ivanildo Barauna de Souza Junior",
    author_email="ivanildo.jnr@outlook.com",
    description="A package to convert API responses to pandas",
    install_requires=parse_requirements("requirements.txt"),
    long_description=get_readme_content(),
    long_description_content_type="text/markdown",
    url="https://github.com/IvanidoBarauba/api-to-dataframe",
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)
