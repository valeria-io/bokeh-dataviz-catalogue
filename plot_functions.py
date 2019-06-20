from material_design_colours import create_multi_colour_pallete

import pandas as pd
import numpy as np
import calendar
import matplotlib.pyplot as plt

from math import pi
from scipy import stats

from bokeh.plotting import figure, show
from bokeh.models import \
    HoverTool, \
    ColumnDataSource, \
    Legend, \
    NumeralTickFormatter, \
    FactorRange, \
    LinearAxis, \
    Range1d, \
    LegendItem
from bokeh.transform import jitter
from bokeh.io import export_svgs
from bokeh.layouts import gridplot

from bokeh.models.widgets import DataTable, HTMLTemplateFormatter, TableColumn, Div
from bokeh.layouts import widgetbox, Column






def plot_dual_axis_dual_bar_line(
        df: pd.DataFrame,
        title: str,
        groups_name: str,
        bar_value_name: str,
        bar_variable_name: list,
        line_variable_name: str,
        **kwargs
) -> figure:
    """
    :param df: long dataframe with groups, groups' variables, bar names, bar values and line values
    :param title: title of plot
    :param groups_name: name for the column where the groups are
    :param bar_value_name: column name where value for each group's bar are
    :param bar_variable_name: column name where variables indicate to which group the bar value belongs to
    :param line_variable_name: column name for the line chart
    :return: figure with bar chart in left axis and line chart in right axis
    """

    """ Prepares data for y values (bars) and x axis (groups and bar variables) """
    bar_variables = df[bar_variable_name].unique()
    df0 = df[df[bar_variable_name] == bar_variables[0]].reset_index(drop=True)
    df1 = df[df[bar_variable_name] == bar_variables[1]].reset_index(drop=True)

    multi_bar_values = [[df0.loc[index, bar_value_name],
                         df1.loc[index, bar_value_name]]
                        for index, row in df0.iterrows()]

    multi_bar_values = [item for sublist in multi_bar_values for item in sublist]

    groups = df[groups_name].unique()
    index_tuple = [(group_, bar_variable) for group_ in groups for bar_variable in bar_variables]

    """ Prepares hover tools"""
    hover_bar = HoverTool(names=['hover_info'])
    hover_line = HoverTool(names=['line_info'])

    """ Prepares graph's settings """
    p = figure(
        x_range=FactorRange(*index_tuple),
        plot_height=kwargs.get('plot_height', 400),
        plot_width=kwargs.get('plot_width', 700),
        title=title,
        tools=["save", hover_bar, hover_line])

    """ Creates multiple bar chart """
    bar_colours = kwargs.get('bar_colours', ["#8c9eff", "#536dfe"])
    colours = bar_colours * len(groups)

    source_bars = ColumnDataSource(
        data=dict(
            x=index_tuple,
            bar_values=multi_bar_values,
            line_values=list(df[line_variable_name]),
            colours=colours
        )
    )
    bar_chart = p.vbar(
        x='x',
        top='bar_values',
        width=kwargs.get('bar_width', 0.9),
        source=source_bars,
        color='colours',
        name='hover_info'
    )

    """ Creates line chart """
    source_lines = ColumnDataSource(
        data=dict(
            x=list(groups),
            line_values=list(df0[line_variable_name]),
        )
    )

    right_axis_y_label = kwargs.get('right_axis_y_label', line_variable_name)

    line_chart = p.line(
        x='x',
        y='line_values',
        y_range_name=right_axis_y_label,
        line_color=kwargs.get('line_colour', "#ffca28"),
        line_width=kwargs.get('line_width', 2),
        source=source_lines
    )
    line_chart = p.circle(
        x='x',
        y='line_values',
        y_range_name=right_axis_y_label,
        color=kwargs.get('line_colour', "#ffca28"),
        size=kwargs.get('circle_size', 7),
        source=source_lines,
        name='line_info'
    )

    """ Sets left axis """
    min_bar_value = df0[bar_value_name].min()
    max_bar_value = df1[bar_value_name].max()

    p.y_range = Range1d(
        kwargs.get('min_left_y_range', min(0, min_bar_value*1.1, min_bar_value*0.9)),
        kwargs.get('max_left_y_range', max(0, max_bar_value*1.1, max_bar_value*0.9)),

    )
    left_axis_y_label = kwargs.get('left_axis_y_label', bar_value_name)
    p.yaxis.axis_label = left_axis_y_label

    """ Sets right axis """
    min_line_value = df[line_variable_name].min()
    max_line_value = df[line_variable_name].max()

    p.extra_y_ranges = {
        right_axis_y_label: Range1d(
            start=kwargs.get('min_right_y_range', min(min_line_value*1.1, min_line_value*0.9)),
            end=kwargs.get('max_right_y_range', max(max_line_value*1.1, max_line_value*0.9)),
        )
    }
    p.add_layout(LinearAxis(y_range_name=right_axis_y_label, axis_label=right_axis_y_label), 'right')

    """ Formats rest of graph"""
    p = format_axis(p, **kwargs)
    p = format_grid(p, **kwargs)

    """ Assigns tooltips """
    tooltips_bar = [
        (kwargs.get('x_tooltip_name', 'Group'), '@x'),
        (kwargs.get('bar_tooltip_name', left_axis_y_label), '@bar_values' + kwargs.get('bar_tooltip_format', '')),
        (kwargs.get('line_tooltip_name', right_axis_y_label), '@line_values' + kwargs.get('line_tooltip_format', ''))
    ]
    hover_bar.tooltips = get_custom_hover_tooltips(tooltips_bar)

    p.add_tools(hover_bar)

    tooltips_line = [
        (kwargs.get('x_tooltip_name', 'Group'), '@x'),
        (kwargs.get('line_tooltip_name', right_axis_y_label), '@line_values' + kwargs.get('line_tooltip_format', ''))
    ]
    hover_line.tooltips = get_custom_hover_tooltips(tooltips_line)
    p.add_tools(hover_line)

    """ Adds legend"""
    legend = Legend(items=[
        LegendItem(label=left_axis_y_label + ': ' + bar_variables[0], renderers=[bar_chart], index=0),
        LegendItem(label=left_axis_y_label + ': ' + bar_variables[1], renderers=[bar_chart], index=1),
        LegendItem(label=right_axis_y_label, renderers=[line_chart], index=0),
    ], location=kwargs.get('legend_location', (0, 0)))

    p.add_layout(legend, kwargs.get('legend_placement', 'below'))


    return p


def format_axis(p: figure, **kwargs) -> figure:
    p.yaxis[0].formatter = NumeralTickFormatter(format=kwargs.get("y_num_tick_formatter", '0.0'))
    p.x_range.range_padding = kwargs.get("x_range_padding", 0.1)
    p.xaxis.major_label_orientation = kwargs.get('x_label_orientation', 1)
    return p


def format_grid(p: figure, **kwargs) -> figure:
    p.xgrid.grid_line_color = kwargs.get('grid_line_colour', None)
    return p


def get_custom_hover_tooltips(tooltips):
    """ Function that forces only one hover tooltip to show at a time"""
    html_code = \
        """
        <style>
            .bk-tooltip>div:not(:first-child) {display:none;}
        </style>
        """
    for tooltip in tooltips:
        html_code += "<b>{} : </b> {} <br>".format(tooltip[0], tooltip[1])

    return html_code


def plot_table(df,
               header_style="color: #757575; font-family: Courier; font-weight:800",
               table_style="color: #757575; font-family: Courier; font-weight:normal",
               height=120):

    source = ColumnDataSource(df)

    header = Div(text="<style>.slick-header.ui-state-default{" + header_style + "}</style>")

    template = """
    <div style="{}"> 
        <%= value %>
    </div>
    """.format(table_style)

    columns = [
        TableColumn(field=col,
                    title=col,
                    formatter=HTMLTemplateFormatter(template=template)
                    )
        for col in df.columns
    ]
    data_table = DataTable(source=source,
                           columns=columns,
                           fit_columns=True,
                           header_row=True,
                           index_position=None,
                           height=height
                           )
    return Column(header, widgetbox(data_table))


