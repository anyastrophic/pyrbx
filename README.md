<p align="center" width="100%">
    <img src="https://raw.githubusercontent.com/anyastrophic/pyrbx/main/resources/textlogo.svg" alt="pyrbx" height="128em" />
    <br />
</p>
<p align="center">
    <a href="https://github.com/anyastrophic/pyrbx">GitHub</a> |
    <a href="https://discord.gg/UKPaPu4teg">Discord</a> |
    <a href="https://pypi.org/project/roblox/">PyPI</a> |
    <a href="https://pyrbx.jmk.gg/">Documentation</a> |
    <a href="https://github.com/anyastrophic/pyrbx/tree/main/examples">Examples</a> |
    <a href="https://github.com/anyastrophic/pyrbx/blob/main/LICENSE">License</a>
</p>
<p align="center">
    <a href="https://discord.gg/UKPaPu4teg"><img src="https://img.shields.io/discord/761603917490159676?style=flat-square&logo=discord" alt="RoAPI Discord"/></a>
    <a href="https://pypi.org/project/anyastrophic/"><img src="https://img.shields.io/pypi/v/roblox?style=flat-square" alt="pyrbx PyPI"/></a>
    <a href="https://pypi.org/project/roblox/"><img src="https://img.shields.io/pypi/dm/roblox?style=flat-square" alt="pyrbx PyPI Downloads"/></a>
    <a href="https://pypi.org/project/roblox/"><img src="https://img.shields.io/pypi/dm/anyastrophic?style=flat-square" alt="pyrbx PyPI Downloads (Legacy)"/></a>
    <a href="https://pypi.org/project/anyastrophic/"><img src="https://img.shields.io/pypi/l/roblox?style=flat-square" alt="pyrbx PyPI License"/></a>
    <a href="https://github.com/anyastrophic/pyrbx"><img src="https://img.shields.io/github/commit-activity/w/rbx-libdev/pyrbx?style=flat-square" alt="pyrbx GitHub Commit Activity"/></a>
    <a href="https://github.com/anyastrophic/pyrbx"><img src="https://img.shields.io/github/last-commit/rbx-libdev/pyrbx?style=flat-square" alt="pyrbx GitHub Last Commit"/></a>
</p>

# Overview
Welcome to pyrbx a fork of pyrbx.
pyrbx is an asynchronous, object-oriented wrapper for the Roblox web API.

This fork main purpose is to implement support for Roblox Cloud APIs, however other features are also being added.

The table below represents full support of cloud services.

| Service          | Completed |
|------------------|---|
| Messaging        | ✅ |
| Data Stores      | ❌ |
| Place Publishing | ❌ |
| Assets           | ❌ |

# Features
The key features are:  

- **Asynchronous**: pyrbx works well with asynchronous frameworks like [FastAPI](https://fastapi.tiangolo.com/) and 
[discord.py](https://github.com/Rapptz/discord.py).  
- **Easy**: pyrbx's client-based model is intuitive and easy to learn for both the beginner and expert developer. It
  abstracts away API requests and leaves you with simple objects that represent data types on the Roblox platform.
- **Flexible**: pyrbx's builtin Requests object allows the user to do things that we haven't already implemented
ourselves without dealing with advanced Roblox-specific concepts.

# Installation
To install pyrbx from PyPI, you can install with pip:
```
pip install pyrbx
```

To install the latest unstable version of pyrbx, install [git-scm](https://git-scm.com/downloads) and run the following:
```
pip install git+https://github.com/anyastrophic/pyrbx.git
```

# Tutorial
Learn how to use pyrbx in our docs:
https://anyastrophic.github.io/pyrbx/dev/