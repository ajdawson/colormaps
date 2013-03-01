Colormap Gallery
================

Built-in colormaps
------------------

.. plot::

   from colormaps import get_colormap_base_names, show_colormap


   bases = filter(lambda n: not(n.startswith('ncl_') or n.startswith('brewer_')),
                  get_colormap_base_names())
   for base in bases:
       show_colormap(base)


ColorBrewer colormaps
---------------------

Maps downloaded from http://www.personal.psu.edu/cab38/ColorBrewer/ColorBrewer_RGB.html. These colors are licensed under an Apache-style license (http://www.personal.psu.edu/cab38/ColorBrewer/ColorBrewer_updates.html).

.. plot::

   from colormaps import get_colormap_base_names, show_colormap


   bases = filter(lambda n: n.startswith('brewer_'),
                  get_colormap_base_names())
   for base in bases:
       show_colormap(base)


NCL colormaps
-------------

Colormaps from the NCAR Command Language version 6.1.0 (http://dx.doi.org/10.5065/D6WD3XH5)

.. plot::

   from colormaps import get_colormap_base_names, show_colormap


   bases = filter(lambda n: n.startswith('ncl_'),
                  get_colormap_base_names())
   for base in bases:
       show_colormap(base)
