import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="VariantCallingGATK4-ekherman", # Replace with your own username
    version="1.0.0",
    author="Emily Herman",
    author_email="eherman@ualberta.ca",
    description="A Snakemake workflow for SNP and SV calling from raw Illumina data",
    url="https://github.com/stothard-group/variant-calling-gatk4",
    packages=setuptools.find_packages(),
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.21.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.11',
)
