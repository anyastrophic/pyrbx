import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup_info = {
    "name": "pyrbx",
    "version": "2.0.1",
    "author": "anyastrophic",
    "author_email": "logixism@pm.me",
    "description": "pyrbx is a modern object-oriented asynchronous Python wrapper for the Roblox web API.",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/anyastrophic/pyrbx",
    "packages": setuptools.find_packages(),
    "classifiers": [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        "Topic :: Software Development :: Libraries"
    ],
    "project_urls": {
        "Issue Tracker": "https://github.com/anyastrophic/pyrbx/issues",
        "GitHub": "https://github.com/anyastrophic/pyrbx/",
        "Examples": "https://github.com/anyastrophic/pyrbx/tree/main/examples",
    },
    "python_requires": '>=3.7',
    "install_requires": [
        "httpx>=0.21.0",
        "python-dateutil>=2.8.0"
    ]
}


setuptools.setup(**setup_info)
