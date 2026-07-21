"""Shared matplotlib helpers for the report figures: CJK-font setup and the
brand palette, so figure scripts don't each re-copy the same bootstrap."""
from pathlib import Path

import matplotlib

# Brand palette shared across the report figures.
NAVY, BLUE, AMBER, RED, GREY = "#1a2b4a", "#2e5b9e", "#e08a1e", "#b3261e", "#8a8a8a"

_CJK_FONTS = ("/System/Library/Fonts/Hiragino Sans GB.ttc",
              "/System/Library/Fonts/STHeiti Medium.ttc")


def setup_cjk_font():
    """Register a CJK font and disable the Unicode-minus glyph (many CJK fonts
    lack it). Call once, after ``matplotlib.use('Agg')`` and before plotting.
    Safe to call repeatedly."""
    from matplotlib import font_manager as fm
    for p in _CJK_FONTS:
        if Path(p).exists():
            fm.fontManager.addfont(p)
            matplotlib.rcParams["font.family"] = fm.FontProperties(fname=p).get_name()
            break
    matplotlib.rcParams["axes.unicode_minus"] = False
