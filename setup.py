# setup.py
from setuptools import setup, find_packages

setup(
    name="django-offload-with-logs",  # The name of your package on PyPI
    version="0.1.2",
    packages=find_packages(),  # This will find django_offload_with_logs
    include_package_data=True,  # So that static files, migrations, etc. are included
    install_requires=[
        "Django>=2.2",  # or whichever version you want to support
    ],
    description="Django task offloading with status tracking and user notifications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AyubKa4a/django-offload-with-logs",  # GitHub link
    author="Ayub Kara",
    author_email="a.kara@dojoon.ly",
    license="MIT",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
    ],
)
