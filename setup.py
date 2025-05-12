from setuptools import setup, find_packages

setup(
    name="pdfsuite",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  # Add any dependencies here
    description="Common library for 'pdfsuite' plugins running under both Thunar and Nautilus",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Shining",
    author_email="shining@linuxcondom.net",
    url="https://github.com/shining-fnml/pdfsuite-plugin",
    license="GPL-3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Framework :: GTK",
        "Framework :: PyGObject",
        "Environment :: Plugins",
        "Topic :: Utilities",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Office/Business",
    ],
)
