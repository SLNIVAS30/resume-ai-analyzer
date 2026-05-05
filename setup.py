from setuptools import setup, find_packages

setup(
    name="resume-ai-analyzer",
    version="1.0.0",
    description="Professional Resume Analysis and Career Guidance Tool",
    long_description=open("README.md").read() if open("README.md") else "",
    long_description_content_type="text/markdown",
    author="Resume AI Team",
    author_email="",
    url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit==1.28.1",
        "pandas==2.1.3",
        "plotly==5.17.0",
        "nltk==3.8.1",
        "pdfminer3==1.0.3",
        "pyresparser==1.0.6",
        "streamlit-tags==1.0.5",
        "Pillow==10.0.1",
        "geocoder==1.38.1",
        "geopy==2.4.1",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "resume-ai=App_fixed:run",
        ],
    },
)
