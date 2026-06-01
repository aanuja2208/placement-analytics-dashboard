"""
Utility functions and constants for the Placement Analytics Dashboard.
Provides color palettes, formatters, trend helpers, and reusable UI components.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

# ---------------------------------------------------------------------------
# Color Palette
# ---------------------------------------------------------------------------

COLOR_PALETTE: dict[str, str] = {
    "primary": "#1B2A4A",        # dark navy
    "secondary": "#2E86AB",      # teal
    "accent": "#D97706",         # amber
    "success": "#16A34A",        # green
    "warning": "#EAB308",        # yellow
    "danger": "#DC2626",         # red
    "bg_card": "#FFFFFF",
    "bg_dark": "#F3F4F6",
    "text_primary": "#111827",
    "text_secondary": "#4B5563",
}

CHART_COLORS: List[str] = [
    "#2E86AB",
    "#A23B72",
    "#F18F01",
    "#22A06B",
    "#6554C0",
    "#00B8D9",
    "#FF8B6A",
    "#36B37E",
    "#FF5630",
    "#8993A4",
]

BRANCH_ORDER: List[str] = ["CSE", "IT", "ECE", "EE", "ME", "CE", "BT"]

# ---------------------------------------------------------------------------
# Number / Currency / Percentage Formatters
# ---------------------------------------------------------------------------


def format_number(n: float | int) -> str:
    """Format a number with comma separators.

    Examples
    --------
    >>> format_number(1234567)
    '1,234,567'
    >>> format_number(0)
    '0'
    """
    if n is None:
        return "N/A"
    return f"{int(n):,}" if float(n) == int(n) else f"{n:,.2f}"


def format_percentage(value: float | int, decimals: int = 1) -> str:
    """Return a value formatted as a percentage string.

    Examples
    --------
    >>> format_percentage(65.3)
    '65.3%'
    >>> format_percentage(100, decimals=0)
    '100%'
    """
    if value is None:
        return "N/A"
    return f"{value:.{decimals}f}%"


def format_currency(value: float | int) -> str:
    """Return a value (assumed to be in LPA) as a human-readable string.

    Examples
    --------
    >>> format_currency(8.5)
    '8.5 LPA'
    >>> format_currency(12.0)
    '12.0 LPA'
    """
    if value is None:
        return "N/A"
    return f"{value:.1f} LPA"


# ---------------------------------------------------------------------------
# Delta / Trend Helpers
# ---------------------------------------------------------------------------


def get_delta_indicator(
    current: float | int,
    previous: float | int,
) -> Tuple[str, str]:
    """Compute the percentage change and return a delta label with direction.

    Returns
    -------
    (label, color_hint)
        *label* is e.g. ``'^ +5.2%'`` or ``'v -3.1%'``.
        *color_hint* is ``'normal'`` when the change is positive (green in
        Streamlit metrics) or ``'inverse'`` when negative.
    """
    if previous is None or previous == 0:
        return ("--", "off")
    pct_change = ((current - previous) / abs(previous)) * 100
    if pct_change > 0:
        return (f"\u25B2 +{pct_change:.1f}%", "normal")
    if pct_change < 0:
        return (f"\u25BC {pct_change:.1f}%", "inverse")
    return ("-- 0.0%", "off")


def get_trend_label(values: List[float | int]) -> str:
    """Classify a list of sequential values as Improving, Declining, or Stable.

    Uses the last three data points (or fewer if not available) and a simple
    linear direction check.  A slope within +/-1 % of the mean is considered
    stable.
    """
    if values is None or len(values) < 2:
        return "Stable"

    recent = values[-3:] if len(values) >= 3 else values
    first, last = recent[0], recent[-1]
    mean_val = sum(recent) / len(recent) if recent else 1
    if mean_val == 0:
        mean_val = 1  # prevent division by zero
    pct_change = ((last - first) / abs(mean_val)) * 100

    if pct_change > 1:
        return "Improving"
    if pct_change < -1:
        return "Declining"
    return "Stable"


# ---------------------------------------------------------------------------
# Plotly Layout Helper
# ---------------------------------------------------------------------------


def get_plotly_layout(title: str = "", height: int = 400) -> dict:
    """Return a standard Plotly layout dict for a dark-themed dashboard.

    The layout uses transparent backgrounds, the Inter / Segoe UI font stack,
    suppresses gridlines, and applies consistent margins.
    """
    font_family = "Inter, Segoe UI, sans-serif"
    return {
        "title": {
            "text": title,
            "font": {"size": 20, "color": COLOR_PALETTE["text_primary"], "family": font_family},
            "x": 0.0,
            "xanchor": "left",
        },
        "height": height,
        "font": {"family": font_family, "color": COLOR_PALETTE["text_secondary"], "size": 14},
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "margin": {"l": 40, "r": 20, "t": 50, "b": 40},
        "xaxis": {
            "showgrid": False,
            "zeroline": False,
            "color": COLOR_PALETTE["text_secondary"],
        },
        "yaxis": {
            "showgrid": False,
            "zeroline": False,
            "color": COLOR_PALETTE["text_secondary"],
        },
        "legend": {
            "orientation": "h",
            "yanchor": "bottom",
            "y": -0.25,
            "xanchor": "center",
            "x": 0.5,
            "font": {"size": 14, "color": COLOR_PALETTE["text_primary"]},
        },
        "hoverlabel": {
            "bgcolor": COLOR_PALETTE["bg_card"],
            "font_size": 14,
            "font_family": font_family,
            "font": {"color": COLOR_PALETTE["text_primary"]},
        },
    }


# ---------------------------------------------------------------------------
# KPI Card HTML
# ---------------------------------------------------------------------------


def get_kpi_card_html(
    title: str,
    value: str,
    delta: Optional[str] = None,
    delta_color: str = "success",
) -> str:
    """Return an HTML string for a styled KPI card.

    Parameters
    ----------
    title : str
        The metric label (e.g. "Total Placed").
    value : str
        Pre-formatted display value (e.g. "1,234" or "85.3%").
    delta : str, optional
        Delta text such as "^ +5.2%".  If *None*, the delta row is omitted.
    delta_color : str
        Key from COLOR_PALETTE used to colour the delta text.
        Typically ``'success'``, ``'danger'``, or ``'warning'``.
    """
    color = COLOR_PALETTE.get(delta_color, COLOR_PALETTE["success"])

    delta_html = ""
    if delta is not None:
        delta_html = (
            f'<div style="font-size:1.0rem; color:{color}; '
            f'margin-top:4px; font-weight:600;">{delta}</div>'
        )

    return (
        f'<div style="'
        f"background:{COLOR_PALETTE['bg_card']}; "
        f"border:1px solid #D1D5DB; "
        f"border-radius:10px; "
        f"padding:20px 18px; "
        f"text-align:center; "
        f'box-shadow: 0 4px 6px rgba(0,0,0,0.05);'
        f'">'
        f'<div style="font-size:1.1rem; color:{COLOR_PALETTE["text_secondary"]}; '
        f'text-transform:uppercase; letter-spacing:0.6px; font-weight:600;">'
        f"{title}</div>"
        f'<div style="font-size:2.2rem; font-weight:700; '
        f'color:{COLOR_PALETTE["text_primary"]}; margin-top:6px;">'
        f"{value}</div>"
        f"{delta_html}"
        f"</div>"
    )
