Colormap Gallery
================

.. plot::

   import matplotlib.pyplot as plt
   from matplotlib.colorbar import ColorbarBase

   from colormaps import (create_colormap,
                          get_colormap_base,
                          get_colormap_base_names)


   def plot_base(base_name):
       base = get_colormap_base(base_name)
       cmap = create_colormap(base.ncolors, base=base_name)
       fig = plt.figure(figsize=(9, .7))
       ax = fig.add_axes([.01, .35, .98, .63])
       cb = ColorbarBase(ax, cmap=cmap, orientation='horizontal', ticks=[])
       cb.set_label('{:s}: {:d} colors'.format(base_name, base.ncolors))
       plt.show()


   base_names = get_colormap_base_names()
   ncl_bases = filter(lambda n: n.startswith('ncl_'), base_names)
   brewer_bases = filter(lambda n: n.startswith('brewer_'), base_names)
   builtin_bases = filter(lambda n: n not in ncl_bases + brewer_bases, base_names)
   for base in builtin_bases + brewer_bases + ncl_bases:
       plot_base(base)
