import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="advanced_number_game", # Add these
    version="1.0.0",
    description="A number game offering a more advanced experience than other number game packages",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mrf-dot/number_game/",
    author="Mitch Feigenbaum",
    author_email="mfeigenbaum23@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["number_game"],
    include_package_data=True,
    install_requires=["secrets"],
        entry_points={
        "console_scripts": [
            "number_game=number_game.__main__:main",
        ]
    },
)
