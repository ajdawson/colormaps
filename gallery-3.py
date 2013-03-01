from colormaps import get_colormap_base_names, show_colormap


bases = filter(lambda n: n.startswith('ncl_'),
               get_colormap_base_names())
for base in bases:
    show_colormap(base)