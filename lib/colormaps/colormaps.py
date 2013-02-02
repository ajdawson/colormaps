"""Colormap generation for matplotlib"""
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
import os
import re

import numpy as np
from matplotlib.colors import ListedColormap
from scipy.interpolate import interp1d


# Dictionary to store colormap bases.
_bases = {}


class ColormapBase(object):
    """A colormap base.

    A container for base colors and meta-data.

    """

    def __init__(self, name, colors, description=None, attributes=None):
        """Create a :py:class:`colormaps.ColormapBase` instance.

        **Arguments:**

        *name*
            Name for the colormap.

        *description*
            Description of the colormap.

        *colors*
            A :py:class:`numpy.ndarray` dimensions (N, 3) containing N
            RGB triples.

        """
        self.name = name
        self.description = description if description is not None else ''
        self.colors = self.__process_colors(colors)
        self.ncolors = len(colors)
        try:
            for key, value in attributes.items():
                setattr(self, key, value)
        except AttributeError:
            pass

    def __process_colors(self, colors):
        try:
            if colors.ndim !=2 or colors.shape[1] != 3:
                raise ValueError
        except (AttributeError, ValueError):
            raise ValueError('colors must be an Nx3 array: {!s}'.format(self.name))
        if (colors > 1.).any():
            colors /= 255.
        return colors


def register_colormap_base(base, overwrite=False):
    """Register a colormap base for use.

    **Argument:**

    *base*
        A :py:class:`colormaps.ColormapBase` instance to regoster.

    **Keyword argument:**

    *overwrite*
        If *False*, *base* will not overwrite a colormap base with the
        same name. If *True*, *base* will overwrite a colormap base with
        the same name if one exists.

    """
    global _bases
    if base.name in _bases.keys() and not overwrite:
        raise ValueError('colormap base already exists: '
                         '{!s}'.format(base.name))
    _bases[base.name] = base


def list_colormap_bases(name=None, full=False):
    """List the base colormaps.

    **Optional arguments:**

    *name*
        List only the colormap named *name*.

    *full*
        If *False* only the name and description of the colormap bases
        will be printed. If *True* the colors (RGB in the range 0 to 1)
        will also be printed. Defaults to *False*.

    """
    bases = _bases.keys() if name is None else [name]
    for basename in sorted(bases):
        try:
            base = _bases[basename]
            print '{base.name}: {base.description}'.format(base=base)
            if full:
                for color in base.colors:
                    print '  {c[0]:.2f} {c[1]:.2f} {c[2]:.2f}'.format(c=color)
        except KeyError:
            raise ValueError('colormap base does not exist: '
                             '{!s}'.format(name))

def get_colormap_base_names():
    """Return a list of the names of all colormap bases."""
    return sorted(_bases.keys())


def get_colormap_base(name):
    """
    Return a colormap base (a :py:class:`colormaps.ColormapBase`
    instance.

    **Argument:**

    *name*
        Name of the colormap base to return.

    """
    try:
        base = _bases[name]
    except KeyError:
        raise ValueError('colormap base does not exist: '
                         '{!s}'.format(name))
    return base


def create_colormap(ncolors,
                    base='rainbow',
                    name=None,
                    reverse=False,
                    white=False):
    """Create a colormap from a set of base colors.
    
    **Argument:**
    
    *ncolors*
        The number of colors required in the colormap.
    
    **Keyword arguments:**
    
    *base*
        Name of the colormap base to build the colormap from. Use
        :py:func:`colormaps.list_colormap_bases` to print the names
        of available colormap bases. Use
        :py:func:`colormaps.register_colormap_base` to add a new
        colormap base.
    
    *name*
        Name for the new colormap. If *name* is not given the default
        name 'create_colormap' is used.
    
    *reverse*
        If *False* the colors will be in the same order as specified by
        the colormap base. If *True* the colors will be in the reverse
        order.

    *white*
        The number of white cells to be inserted into the middle of the
        colormap. The number of white cells specified is included in the
        value of *ncolors*. Defaults to no white cells.
        
    """
    try:
        # Retrieve the colormap base.
        base = _bases[base]
    except KeyError:
        raise ValueError()
    rgb = base.colors
    # Determine how many colors are required after factoring in white cells.
    ncolors_interp = (ncolors - white) if white else ncolors
    # Get the required colors.
    base_length = rgb.shape[0]
    if base_length == ncolors_interp:
        # Don't need to interpolate if the number of colors required is the
        # same as the number of colors in the colormap base.
        rgb_interp = rgb.copy()
    else:
        # Interpolate the colormap base colors to get the required number.
        x0 = np.arange(0, base_length)
        x1 = np.linspace(0, base_length-1, ncolors_interp)
        red = np.interp(x1, x0, rgb[:, 0])
        green = np.interp(x1, x0, rgb[:, 1])
        blue = np.interp(x1, x0, rgb[:, 2])
        rgb_interp = np.array([red, green, blue]).transpose()
    if white:
        # Add white to the center of the colormap.
        rgb_white = np.ones([ncolors, 3])
        interp_middle = ncolors_interp / 2
        rgb_white[:interp_middle] = rgb_interp[:interp_middle]
        rgb_white[interp_middle+white] = rgb_interp[interp_middle:]
        rgb_interp = rgb_white
    if reverse:
        # Reverse the colors.
        rgb_interp = rgb_interp[::-1]
    return ListedColormap(rgb_interp, name=name)


def _find_palette_files():
    root_path = os.path.abspath(os.path.dirname(__file__))
    palette_paths = [os.path.join(root_path, 'palette')]
    palette_env = os.getenv('PYTHON_COLORMAPS')
    try:
        palette_paths.extend(palette_env.split(':'))
    except AttributeError:
        pass
    palette_files = []
    for palette_dir in palette_paths:
        for root, dirs, files in os.walk(palette_dir):
            palette_files.extend([os.path.join(root, filename) \
                                  for filename in files \
                                  if os.path.splitext(filename)[1] == '.txt'])
    return palette_files


def _colormap_file_parser(filename, prefix=None, suffix=None):
    with open(filename, 'r') as f:
        header = filter(lambda line: re.match('^\s*#.*:\s+.*$', line),
                        f.readlines())
    body_template = ''.join(filter(None, [prefix, '{!s}', suffix]))
    cmap_name = None
    cmap_description = None
    cmap_attributes = {}
    for line in header:
        line = line.replace('#', '', 1).split(':')
        head = line[0].strip().lower()
        body = line[1].strip()
        if head == 'name':
            cmap_name = body_template.format(body)
        elif head == 'description':
            cmap_description = body
        else:
            cmap_attributes[head] = body
    try:
        assert cmap_name is not None, \
                'missing name in file: {!s}'.format(filename)
    except AssertionError, e:
        raise ValueError(e)
    cmap_colors = np.loadtxt(filename)
    base = ColormapBase(cmap_name,
                        cmap_colors,
                        description=cmap_description,
                        attributes=cmap_attributes,)
    return base


def _load_colormap_bases():
    """Load colormap bases from file."""
    palette_files = _find_palette_files()
    for palette_file in palette_files:
        base = _colormap_file_parser(palette_file)
        register_colormap_base(base)


# Load colormap bases at import time.
_load_colormap_bases()


if __name__ == "__main__":
    pass

