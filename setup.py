from setuptools import setup, find_packages

setup(
    name="ah_faceswap",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    install_requires=[
        "facefusionlib",
        "nanoid"
    ],
    include_package_data=True,
    python_requires=">=3.8"
)
