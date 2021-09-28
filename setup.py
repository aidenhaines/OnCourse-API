from setuptools import setup
with open("README.md","r",encoding="utf-8") as f:
    long_description=f.read()

setup(
    name="oncourse_api",
    version="1.0.0",
    description="A python api wrapper for OnCourse Connect",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wolfhound905/OnCourse-API",
    author="Wolfhound905",
    author_email="aiden8green@gmail.com",
    license="MIT",
    packages=["oncourse_api"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "beautifulsoup4"],
)