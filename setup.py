from setuptools import find_packages
from setuptools import setup


version = "2.0.0"

setup(
    name="plone.stringinterp",
    version=version,
    description="Adaptable string interpolation",
    long_description=(open("README.rst").read() + "\n" + open("CHANGES.rst").read()),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="Plone Zope Interpolation",
    author="Plone Foundation",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://github.com/plone/plone.stringinterp",
    license="GPL version 2",
    packages=find_packages(),
    namespace_packages=["plone"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "plone.base",
        "plone.memoize",
        "zope.i18n",
    ],
    extras_require={
        "test": [
            "plone.app.contenttypes",
            "plone.app.testing",
            "plone.testing",
        ],
    },
    entry_points="""
        [z3c.autoinclude.plugin]
        target = plone
    """,
)
