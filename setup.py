import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dispair",  # Replace with your own username
    version="0.0.1",
    author="GDWR",
    author_email="gregory.dwr@gmail.com",
    description="Webhook handler for Discord Interactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GDWR/Dispair",
    project_urls={
        "Bug Tracker": "https://github.com/GDWR/dispair/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
