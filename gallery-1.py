from colormaps import get_colormap_base_names, show_colormap


bases = filter(lambda n: not(n.startswith('ncl_') or n.startswith('brewer_')),
               get_colormap_base_names())
for base in bases:
    show_colormap(base)