"""Build and install the colormaps package."""
# Copyright (c) 2012 Andrew Dawson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from distutils.core import setup


for line in open('lib/colormaps/__init__.py').readlines():
    if (line.startswith('__version__')):
        exec(line.strip())

package_data = {'colormaps': ['palette/*.txt', 'palette/ncl/*.txt',
                              'palette/brewer/diverging/*.txt',
                              'palette/brewer/qualitative/*.txt',
                              'palette/brewer/sequential/*.txt']}

if __name__ == '__main__':
    setup(
        name='colormaps',
        version=__version__,
        description='Easily generate colormaps for matplotlib',
        author='Andrew Dawson',
        author_email='dawson@atm.ox.ac.uk',
        url='http://github.com/ajdawson/colormaps',
        long_description="""
        colormaps can generate colormaps of varying lengths from sets of
        base colors. It is designed to allow total control of colormaps
        in matplotlib.
        """,
        packages=['colormaps'],
        package_dir={'': 'lib'},
        package_data=package_data,)
