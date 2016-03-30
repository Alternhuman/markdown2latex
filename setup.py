from setuptools import setup

from mdx_latex import __version__, __doc__

setup(
    name = 'markdown2latex',
    version = __version__,
    py_modules=['mdx_latex'],
    entry_points='''
    [console_scripts]
    markdown2latex.py=mdx_latex:main
    ''',
    install_requires=[
        'Markdown>=2.6.6',
        ],

    # metadata for upload to PyPI
    author = 'Diego Martín',
    url = 'https://github.com/Alternhuman/markdown2latex.git',
    author_email = 'diegomartinpi [at] gmail [dot] com',
    description = __doc__.split()[0],
    long_description = __doc__,
    license = 'MIT',
    keywords = 'latex markdown python',
    download_url = 'https://github.com/Alternhuman/markdown2latex.git',
    zip_safe=False,
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
