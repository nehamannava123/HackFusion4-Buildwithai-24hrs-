from setuptools import setup, find_packages

setup(
    name="codenav-ai",
    version="1.0.0",
    description="AI-powered codebase navigation assistant",
    author="CodeNav AI",
    packages=find_packages(),
    install_requires=['flask>=2.0.0'],
    entry_points={'console_scripts': ['codenav=codenav.cli:main']},
    python_requires='>=3.7',
)