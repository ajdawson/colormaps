import os
import re

def _find_palette_files():
    palette_files = []
    for root, dirs, files in os.walk('.'):
        palette_files.extend([os.path.join(root, filename) \
                              for filename in files \
                              if os.path.splitext(filename)[1] == '.txt'])
    return palette_files


palette_files = _find_palette_files()
for palette_file in palette_files:

    with open(palette_file, 'r') as f:
        lines = f.readlines()

    # Move the old file, so as not to destroy it.
    moved_palette_file = palette_file + '.moved'
    os.rename(palette_file, moved_palette_file)

    # open the file to write:
    with open(palette_file, 'w') as f:
        for line in lines:
            if re.match('^\s*#.*:\s+.*$', line):
                nline = line.replace('#', '', 1).split(':')
                head = nline[0].strip().lower()
                body = nline[1].strip()
                if head == 'name':
                    line = line.replace(body, 'brewer_{!s}'.format(body))
                    line = line + '# description:  ColorBrewer {!s}\n'.format(body)
            f.write(line)
            
