from setuptools import setup, find_packages

setup (
    name="clean_folder",
    version="1.0",
    author="Korets Roman",
    entry_points= {
        'console_script': ['clean=clean_folder.clean:main'],
    },
    packages=find_packages(),
    description="Clean folder script",
)


