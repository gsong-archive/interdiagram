# -*- coding: utf-8 -*-

# Colors
COLOR_SCHEME = 'X11'
COLOR1 = 'dodgerblue2'
COLOR2 = 'firebrick2'
COLOR3 = 'purple2'
GRAY = 'gray50'
DARK_GRAY = 'gray30'
NODE_HEADER_COLOR = 'azure'

# General options
FONT = 'helvetica'
FONT_BOLD = FONT + ' bold'
LAYOUT = 'dot'

# DOT graph options
GRAPH_OPTIONS = dict(
    directed=True,
    rankdir='LR',
    strict=False,
)

# DOT node options
NODE_OPTIONS = dict(fontname=FONT)
COMPONENT_OPTIONS = dict(
    color=COLOR2,
    colorscheme=COLOR_SCHEME,
    shape='box',
    style='dashed,rounded',
    **NODE_OPTIONS
)
SECTION_OPTIONS = dict(
    color=COLOR1,
    colorscheme=COLOR_SCHEME,
    shape='box',
    style='rounded',
    **NODE_OPTIONS
)
AD_HOC_NODE_OPTIONS = dict(
    color=COLOR3,
    colorscheme=COLOR_SCHEME,
    fontcolor=COLOR3,
    style='dashed',
    **NODE_OPTIONS
)

# DOT edge options
EDGE_OPTIONS = dict(
    arrowsize=.6,
    color=GRAY,
    colorscheme=COLOR_SCHEME,
)
