__author__ = 'cm'
from setuptools import setup, find_packages, Extension

setup(name='wiki_terminal',
      version='1.0.0',
      description="This script will enable you wiki in terminal. This is inspired by longcw's youdao.",
      long_description="This script will enable you wiki in shell. This is inspired by longcw's youdao."
                       "Please visit my github page for more information.",
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