__author__ = 'cm'
from setuptools import setup, find_packages, Extension

setup(name='wiki_terminal',
      version='1.2.0',
      description="This script will enable you use wikipedia in terminal.",
      long_description="""
                        Install:
                        you can install it by python install setup.py
                        Help:
                        use help for help
                        summary arg to get summary about the arg
                        search arg to search arg on wiki
                        random s(summary)to get a random tittle (you can get summary about it if you want.)
                        geosearch latitude longitude (radius) Do a wikipedia geo search for latitude and longitude using.
                        Version:
                        Version 1.0.0 basic function built\n
                        Version 1.0.1 the geosearch function is added\n
                        version 1.1.0 the keyword-highlight function is added\n
                        version 1.1.1 the search function bug fixed and history function added\n
                        version 1.2.0 rewrite wiki_terminal using prompt-toolkit\n
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
              'wikipedia = wiki.client:main',
          ]
      },
)
