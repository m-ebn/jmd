from setuptools import setup

setup(
    name='jmd',
    version='0.0',
    description='A useful module',
    author='Michael Ebnicher',
    author_email='foomail@foo.com',
    packages=['jmd'],  # same as name
    # external packages as dependencies
    install_requires=['python-frontmatter', 'os', 're', 'argparse', 'numpy'],
)
