from setuptools import setup


with open('achievements.py') as f:
    info = {}
    for line in f.readlines():
        if line.startswith('__version__'):
            exec(line, info)
            break

README = open('README.md').read()

setup(name='achievements',
      version=info['__version__'],
      author='Benjamin Moran',
      author_email='benmoran@protonmail.com',
      description="A lightweight achievements framework.",
      long_description=README,
      license='MIT',
      keywords='gamedev,game',
      url='https://github.com/benmoran56/achievements',
      download_url='https://github.com/benmoran56/achievements/releases',
      platforms='POSIX, Windows, MacOS X',
      py_modules=["achievements"],
      classifiers=["Development Status :: 3 - Alpha",
                   # "Development Status :: 4 - Beta",
                   # "Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3 :: Only",
                   "Topic :: Games/Entertainment",
                   "Topic :: Software Development :: Libraries"])
