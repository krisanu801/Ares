import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Ares",  
    version="0.0.1",
    author="Krisanu801", 
    author_email="sarkarkrisanu03@gmail.com", 
    description="Autonomous Research & Experimentation System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krisanu801/Ares",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "google-generativeai",
        "arxiv",
        "pubmed_parser",
        "PyYAML",
        "requests",
        "pytest",
        "python-dotenv"
    ],
    entry_points={
        'console_scripts': [
            'ares=src.main:main', 
        ],
    },
    package_data={
        'configs': ['*.yaml'],
        'data': ['*.xml'], 
    },
    include_package_data=True, # Important to include non-python files
)
