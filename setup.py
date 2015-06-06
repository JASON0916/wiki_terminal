__author__ = 'cm'
from setuptools import setup, find_packages, Extension

setup(name='wiki_terminal',
      version='1.1.1',
      description="This script will enable you use wikipedia in terminal. This is inspired by longcw's youdao.",
      long_description="""
                        Install:
                        you can install it by python install setup.py
                        Help:
                        wiki -h(--help)for help
                        wiki -s(--summary) argto get summary about the arg
                        wiki -S(--search) argto search arg on wiki
                        wiki -r(--random) s(summary)to get a random tittle (you can get summary about it if you want.)
                        wiki -g(--geosearch) latitude longitude (radius) Do a wikipedia geo search for latitude and longitude using.
                        wiki -H(--history) show your search history and allow you to search again easily.
                        wiki -c clear your query history.
                        Version:
                        Version 1.0.0 basic function built\n
                        Version 1.0.1 the geosearch function is added\n
                        version 1.1.0 the keyword-highlight function is added\n
                        version 1.1.1 the search function bug fixed and history function added\n
                        """,
      keywords='python wikipedia terminal',
      author='cm',
      author_email='jason0916phoenix@gmail.com',
      url='https://github.com/JASON0916/wiki_terminal',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'termcolor', 'wikipedia',
          ],
      classifiers=[
          'Programming Language :: Python :: 2.7',
      ],
      entry_points={
          'console_scripts': [
              'wiki = wiki.main:main',
          ]
      },
)