"""
Reusable Plotly visualization functions with consistent professional theme.
All charts use a dark theme with the project color palette.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Theme constants
# ---------------------------------------------------------------------------
CHART_COLORS = [
    '#2E86AB', '#A23B72', '#F18F01', '#22A06B', '#6554C0',
    '#00B8D9', '#FF8B6A', '#36B37E', '#FF5630', '#8993A4',
]
OUTCOME_COLORS = {'Placed': '#22A06B', 'Higher Studies': '#2E86AB', 'Unplaced': '#BF2600'}
BG_TRANSPARENT = 'rgba(0,0,0,0)'
FONT_FAMILY = 'Inter, Segoe UI, Roboto, sans-serif'
GRID_COLOR = '#E5E7EB'
TEXT_COLOR = '#111827'
MUTED_TEXT = '#4B5563'


def _base_layout(title='', height=420, showlegend=True):
    """Return a standard Plotly layout dict."""
    return dict(
        title=dict(text=title, font=dict(size=16, color=TEXT_COLOR, family=FONT_FAMILY)),
        paper_bgcolor=BG_TRANSPARENT,
        plot_bgcolor=BG_TRANSPARENT,
        font=dict(family=FONT_FAMILY, color=MUTED_TEXT, size=12),
        height=height,
        margin=dict(l=50, r=30, t=50, b=50),
        showlegend=showlegend,
        legend=dict(bgcolor=BG_TRANSPARENT, font=dict(size=11)),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        hoverlabel=dict(bgcolor='#1E2330', font_size=12, font_family=FONT_FAMILY),
    )


# ---------------------------------------------------------------------------
# Line Charts
# ---------------------------------------------------------------------------
def line_chart(df, x, y, title='', color=None, markers=True, height=420, y_label=''):
    """Single or multi-line chart with labelled data points."""
    if df.empty:
        return _empty_fig(title, height)
    if isinstance(y, list):
        fig = go.Figure()
        for i, col in enumerate(y):
            text_vals = df[col].apply(lambda v: f'{v:.1f}' if isinstance(v, (int, float)) else str(v))
            fig.add_trace(go.Scatter(
                x=df[x], y=df[col], mode='lines+markers+text' if markers else 'lines+text',
                name=col.replace('_', ' ').title(),
                line=dict(color=CHART_COLORS[i % len(CHART_COLORS)], width=2.5),
                marker=dict(size=7),
                text=text_vals,
                textposition='top center',
                textfont=dict(size=10, color=CHART_COLORS[i % len(CHART_COLORS)]),
            ))
    else:
        c = color or CHART_COLORS[0]
        text_vals = df[y].apply(lambda v: f'{v:.1f}' if isinstance(v, (int, float)) else str(v))
        fig = go.Figure(go.Scatter(
            x=df[x], y=df[y], mode='lines+markers+text' if markers else 'lines+text',
            name=y.replace('_', ' ').title(),
            line=dict(color=c, width=2.5), marker=dict(size=7),
            text=text_vals,
            textposition='top center',
            textfont=dict(size=10, color=c),
        ))
    layout = _base_layout(title, height)
    if y_label:
        layout['yaxis']['title'] = y_label
    fig.update_layout(**layout)
    return fig


def forecast_line(historical, forecast, x, y, title='', height=420):
    """Line chart with historical (solid) and forecast (dashed) segments, labelled."""
    fig = go.Figure()
    if not historical.empty:
        text_vals = historical[y].apply(lambda v: f'{v:.1f}' if isinstance(v, (int, float)) else str(v))
        fig.add_trace(go.Scatter(
            x=historical[x], y=historical[y], mode='lines+markers+text',
            name='Historical', line=dict(color=CHART_COLORS[0], width=2.5),
            marker=dict(size=7),
            text=text_vals,
            textposition='top center',
            textfont=dict(size=10, color=CHART_COLORS[0]),
        ))
    if not forecast.empty:
        text_vals = forecast[y].apply(lambda v: f'{v:.1f}' if isinstance(v, (int, float)) else str(v))
        fig.add_trace(go.Scatter(
            x=forecast[x], y=forecast[y], mode='lines+markers+text',
            name='Forecast', line=dict(color='#F18F01', width=2.5, dash='dash'),
            marker=dict(size=8, symbol='diamond'),
            text=text_vals,
            textposition='top center',
            textfont=dict(size=10, color='#F18F01'),
        ))
    fig.update_layout(**_base_layout(title, height))
    return fig


# ---------------------------------------------------------------------------
# Bar Charts
# ---------------------------------------------------------------------------
def bar_chart(df, x, y, title='', color=None, horizontal=False, height=420,
              color_continuous=False, text_auto=False, y_label=''):
    """Standard bar chart with data labels on every bar."""
    if df.empty:
        return _empty_fig(title, height)
    orientation = 'h' if horizontal else 'v'
    x_col, y_col = (y, x) if horizontal else (x, y)

    if color_continuous:
        fig = px.bar(df, x=x_col, y=y_col, orientation=orientation, title=title,
                     color=y if not horizontal else x,
                     color_continuous_scale=['#BF2600', '#F18F01', '#22A06B'],
                     text_auto='.1f')
    else:
        val_col = y_col if orientation == 'v' else x_col
        text_vals = df[val_col].apply(lambda v: f'{v:.1f}' if isinstance(v, (int, float)) else str(v))
        fig = go.Figure(go.Bar(
            x=df[x_col], y=df[y_col], orientation=orientation,
            marker_color=color or CHART_COLORS[0],
            text=text_vals,
            textposition='outside',
            textfont=dict(size=10, color=TEXT_COLOR),
        ))
    layout = _base_layout(title, height)
    if y_label:
        layout['yaxis']['title'] = y_label
    fig.update_layout(**layout)
    return fig


def grouped_bar(df, x, y_cols, title='', height=420, barmode='group'):
    """Grouped or stacked bar chart with data labels."""
    if df.empty:
        return _empty_fig(title, height)
    fig = go.Figure()
    for i, col in enumerate(y_cols):
        text_vals = df[col].apply(lambda v: f'{v:.0f}' if isinstance(v, (int, float)) else str(v))
        fig.add_trace(go.Bar(
            x=df[x], y=df[col],
            name=col.replace('_', ' ').title(),
            marker_color=CHART_COLORS[i % len(CHART_COLORS)],
            text=text_vals,
            textposition='outside' if barmode == 'group' else 'inside',
            textfont=dict(size=9),
        ))
    fig.update_layout(**_base_layout(title, height), barmode=barmode)
    return fig


def stacked_bar(df, x, y_cols, title='', height=420, colors=None):
    """Stacked bar chart."""
    return grouped_bar(df, x, y_cols, title, height, barmode='stack')


# ---------------------------------------------------------------------------
# Donut / Pie Charts
# ---------------------------------------------------------------------------
def donut_chart(labels, values, title='', height=400, colors=None):
    """Donut chart with center hole and value labels."""
    if not values or sum(values) == 0:
        return _empty_fig(title, height)
    c = colors or CHART_COLORS[:len(labels)]
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55, marker=dict(colors=c, line=dict(color='#0E1117', width=2)),
        textinfo='label+value+percent', textfont=dict(size=12, color=TEXT_COLOR),
        hoverinfo='label+value+percent',
    ))
    fig.update_layout(**_base_layout(title, height, showlegend=False))
    return fig


# ---------------------------------------------------------------------------
# Heatmaps
# ---------------------------------------------------------------------------
def heatmap(z, x_labels, y_labels, title='', height=450, colorscale='Blues'):
    """Annotated heatmap."""
    if len(z) == 0:
        return _empty_fig(title, height)
    fig = go.Figure(go.Heatmap(
        z=z, x=x_labels, y=y_labels, colorscale=colorscale,
        texttemplate='%{z:.1f}', textfont=dict(size=11),
        hovertemplate='%{y} x %{x}: %{z:.1f}<extra></extra>',
    ))
    fig.update_layout(**_base_layout(title, height, showlegend=False))
    return fig


def correlation_heatmap(df, columns=None, title='Correlation Matrix', height=500):
    """Correlation matrix heatmap from numeric columns."""
    if df.empty:
        return _empty_fig(title, height)
    if columns:
        df = df[columns]
    corr = df.select_dtypes(include=[np.number]).corr()
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.columns,
        colorscale='RdBu_r', zmid=0,
        texttemplate='%{z:.2f}', textfont=dict(size=10),
    ))
    fig.update_layout(**_base_layout(title, height, showlegend=False))
    return fig


# ---------------------------------------------------------------------------
# Scatter Plots
# ---------------------------------------------------------------------------
def scatter_plot(df, x, y, title='', color_col=None, size_col=None, height=420,
                 x_label='', y_label='', trendline=False, text_col=None):
    """Scatter plot with optional color grouping, trend line, and labelled points."""
    if df.empty:
        return _empty_fig(title, height)
    if color_col and color_col in df.columns:
        fig = px.scatter(df, x=x, y=y, color=color_col, size=size_col, text=text_col,
                         color_discrete_sequence=CHART_COLORS, title=title,
                         trendline='ols' if trendline else None)
        fig.update_traces(textposition='top center', textfont_size=10)
    else:
        text_vals = df[text_col] if text_col else df[y].apply(lambda v: f'{v:.1f}' if isinstance(v, (int, float)) else str(v))
        fig = go.Figure(go.Scatter(
            x=df[x], y=df[y], mode='markers+text', text=text_vals,
            textposition='top center',
            textfont=dict(size=9, color=TEXT_COLOR),
            marker=dict(color=CHART_COLORS[0], size=8 if not size_col else df[size_col],
                        opacity=0.7, line=dict(width=0.5, color='#FAFAFA')),
        ))
        if trendline and len(df) > 2:
            z = np.polyfit(df[x].astype(float), df[y].astype(float), 1)
            p = np.poly1d(z)
            x_line = np.linspace(df[x].min(), df[x].max(), 50)
            fig.add_trace(go.Scatter(x=x_line, y=p(x_line), mode='lines',
                                     line=dict(color='#F18F01', dash='dash', width=1.5),
                                     name='Trend'))
    layout = _base_layout(title, height)
    if x_label:
        layout['xaxis']['title'] = x_label
    if y_label:
        layout['yaxis']['title'] = y_label
    fig.update_layout(**layout)
    return fig


# ---------------------------------------------------------------------------
# Box Plots
# ---------------------------------------------------------------------------
def box_plot(df, x, y, title='', height=420):
    """Box plot grouped by category."""
    if df.empty:
        return _empty_fig(title, height)
    categories = df[x].unique()
    fig = go.Figure()
    for i, cat in enumerate(categories):
        fig.add_trace(go.Box(
            y=df[df[x] == cat][y], name=str(cat),
            marker_color=CHART_COLORS[i % len(CHART_COLORS)],
            boxmean=True,
        ))
    fig.update_layout(**_base_layout(title, height))
    return fig


def violin_plot(df, x, y, title='', height=420):
    """Violin plot grouped by category."""
    if df.empty:
        return _empty_fig(title, height)
    categories = df[x].unique()
    fig = go.Figure()
    for i, cat in enumerate(categories):
        fig.add_trace(go.Violin(
            y=df[df[x] == cat][y], name=str(cat),
            marker_color=CHART_COLORS[i % len(CHART_COLORS)],
            box_visible=True, meanline_visible=True,
        ))
    fig.update_layout(**_base_layout(title, height))
    return fig


# ---------------------------------------------------------------------------
# Histogram
# ---------------------------------------------------------------------------
def histogram(df, col, title='', bins=30, height=420, color=None):
    """Histogram for distribution analysis with bin count labels."""
    if df.empty:
        return _empty_fig(title, height)
    fig = go.Figure(go.Histogram(
        x=df[col], nbinsx=bins,
        marker_color=color or CHART_COLORS[0],
        marker_line=dict(color='#0E1117', width=1),
    ))
    # Show count on top of each bin
    fig.update_traces(texttemplate='%{y}', textposition='outside', textfont_size=9)
    fig.update_layout(**_base_layout(title, height))
    return fig


# ---------------------------------------------------------------------------
# Radar Chart
# ---------------------------------------------------------------------------
def radar_chart(categories, values_dict, title='', height=450):
    """Radar chart comparing multiple entities across categories."""
    if not values_dict:
        return _empty_fig(title, height)
    fig = go.Figure()
    for i, (name, vals) in enumerate(values_dict.items()):
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],  # close the polygon
            theta=categories + [categories[0]],
            fill='toself', fillcolor=f'rgba({_hex_to_rgb(CHART_COLORS[i % len(CHART_COLORS)])},0.15)',
            name=name,
            line=dict(color=CHART_COLORS[i % len(CHART_COLORS)], width=2),
        ))
    fig.update_layout(
        **_base_layout(title, height),
        polar=dict(
            bgcolor=BG_TRANSPARENT,
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=GRID_COLOR,
                            tickfont=dict(size=10, color=MUTED_TEXT)),
            angularaxis=dict(gridcolor=GRID_COLOR,
                             tickfont=dict(size=11, color=TEXT_COLOR)),
        ),
    )
    return fig


# ---------------------------------------------------------------------------
# Funnel Chart
# ---------------------------------------------------------------------------
def funnel_chart(stages, values, title='', height=450):
    """Placement funnel chart."""
    if not values or sum(values) == 0:
        return _empty_fig(title, height)
    fig = go.Figure(go.Funnel(
        y=stages, x=values,
        textinfo='value+percent initial',
        textfont=dict(size=12, color=TEXT_COLOR),
        marker=dict(
            color=CHART_COLORS[:len(stages)],
            line=dict(width=1, color='#0E1117'),
        ),
        connector=dict(line=dict(color=GRID_COLOR, width=1)),
    ))
    fig.update_layout(**_base_layout(title, height, showlegend=False))
    return fig


# ---------------------------------------------------------------------------
# Bubble Chart
# ---------------------------------------------------------------------------
def bubble_chart(df, x, y, size, color_col=None, title='', height=450,
                 x_label='', y_label='', text_col=None):
    """Bubble chart for risk matrix / multi-dimensional comparison."""
    if df.empty:
        return _empty_fig(title, height)
    fig = px.scatter(
        df, x=x, y=y, size=size, color=color_col or x,
        text=text_col,
        color_discrete_sequence=CHART_COLORS,
        title=title, size_max=50,
    )
    layout = _base_layout(title, height)
    if x_label:
        layout['xaxis']['title'] = x_label
    if y_label:
        layout['yaxis']['title'] = y_label
    fig.update_layout(**layout)
    fig.update_traces(textposition='top center', textfont_size=10)
    return fig


# ---------------------------------------------------------------------------
# Pareto Chart
# ---------------------------------------------------------------------------
def pareto_chart(df, category, value, title='', height=420):
    """Pareto chart (bar + cumulative line) with data labels."""
    if df.empty:
        return _empty_fig(title, height)
    sorted_df = df.sort_values(value, ascending=False).reset_index(drop=True)
    cumulative = sorted_df[value].cumsum() / sorted_df[value].sum() * 100

    bar_text = sorted_df[value].apply(lambda v: f'{v:.0f}' if isinstance(v, (int, float)) else str(v))
    cum_text = cumulative.apply(lambda v: f'{v:.0f}%')

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=sorted_df[category], y=sorted_df[value],
        marker_color=CHART_COLORS[0], name='Count',
        text=bar_text, textposition='outside', textfont=dict(size=10),
    ))
    fig.add_trace(go.Scatter(
        x=sorted_df[category], y=cumulative,
        mode='lines+markers+text', name='Cumulative %',
        line=dict(color='#F18F01', width=2.5),
        marker=dict(size=6), yaxis='y2',
        text=cum_text, textposition='top center', textfont=dict(size=9, color='#F18F01'),
    ))
    layout = _base_layout(title, height)
    layout['yaxis2'] = dict(
        title='Cumulative %', overlaying='y', side='right',
        range=[0, 110], gridcolor=GRID_COLOR,
    )
    fig.update_layout(**layout)
    return fig


# ---------------------------------------------------------------------------
# KPI Card (HTML based)
# ---------------------------------------------------------------------------
def render_kpi_cards(kpi_list, columns_per_row=4):
    """Render a row of KPI cards using st.columns and st.markdown.
    
    kpi_list: list of dicts with keys: title, value, delta (optional), delta_color (optional)
    """
    import streamlit as st
    rows = [kpi_list[i:i + columns_per_row] for i in range(0, len(kpi_list), columns_per_row)]
    for row in rows:
        cols = st.columns(len(row))
        for col, kpi in zip(cols, row):
            delta_html = ''
            if kpi.get('delta') is not None:
                d_val = kpi['delta']
                if isinstance(d_val, (int, float)):
                    arrow = '\u25b2' if d_val >= 0 else '\u25bc'
                    d_color = '#22A06B' if d_val >= 0 else '#BF2600'
                    delta_html = f'<div style="font-size:13px;color:{d_color};margin-top:2px;">{arrow} {abs(d_val):.1f}%</div>'
                else:
                    delta_html = f'<div style="font-size:16px;color:#4B5563;margin-top:2px;font-weight:600;">{d_val}</div>'

            html = f'''
            <div style="background:#FFFFFF;border:1px solid #D1D5DB;box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                        border-radius:10px;padding:20px 18px;text-align:center;">
                <div style="font-size:17.6px;color:#4B5563;text-transform:uppercase;
                            letter-spacing:0.6px;margin-bottom:6px;font-weight:600;">{kpi["title"]}</div>
                <div style="font-size:35.2px;font-weight:700;color:#111827;">{kpi["value"]}</div>
                {delta_html}
            </div>
            '''
            col.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _empty_fig(title='', height=400):
    """Return a blank figure with a 'No data' annotation."""
    fig = go.Figure()
    fig.update_layout(
        **_base_layout(title, height, showlegend=False),
        annotations=[dict(
            text='No data available', x=0.5, y=0.5, xref='paper', yref='paper',
            showarrow=False, font=dict(size=16, color=MUTED_TEXT),
        )],
    )
    return fig


def _hex_to_rgb(hex_color):
    """Convert hex to comma-separated RGB string."""
    h = hex_color.lstrip('#')
    return ','.join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))
