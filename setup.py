from setuptools import setup

setup(
    name="fake-legal",
    version="1.0.0",
    description="Python SDK and CLI for the fake.legal Temporary Email API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="fake.legal",
    author_email="support@fake.legal",
    url="https://fake.legal",
    py_modules=["fake_legal"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "fake-legal=fake_legal:main",
        ],
    },
)
