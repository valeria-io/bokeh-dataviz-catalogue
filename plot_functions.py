import pandas as pd
import numpy as np
import warnings
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
        bar_variable_name: str,
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

    """ figure"""
    hover_bar = HoverTool(names=['hover_info'])
    hover_line = HoverTool(names=['line_info'])

    p = figure(
        x_range=FactorRange(*index_tuple),
        plot_height=kwargs.get('plot_height', 400),
        plot_width=kwargs.get('plot_width', 700),
        title=title,
        tools=["save", hover_bar, hover_line])

    """ multiple bar chart """
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

    """ line chart """
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

    """ left axis """
    min_bar_value = df0[bar_value_name].min()
    max_bar_value = df1[bar_value_name].max()

    p.y_range = Range1d(
        kwargs.get('min_left_y_range', min(0, min_bar_value * 1.1, min_bar_value * 0.9)),
        kwargs.get('max_left_y_range', max(0, max_bar_value * 1.1, max_bar_value * 0.9)),

    )
    left_axis_y_label = kwargs.get('left_axis_y_label', bar_value_name)
    p.yaxis.axis_label = left_axis_y_label

    """ right axis """
    min_line_value = df[line_variable_name].min()
    max_line_value = df[line_variable_name].max()

    p.extra_y_ranges = {
        right_axis_y_label: Range1d(
            start=kwargs.get('min_right_y_range', min(min_line_value * 1.1, min_line_value * 0.9)),
            end=kwargs.get('max_right_y_range', max(max_line_value * 1.1, max_line_value * 0.9)),
        )
    }
    p.add_layout(LinearAxis(y_range_name=right_axis_y_label, axis_label=right_axis_y_label), 'right')

    p = format_axis(p, **kwargs)
    p = format_grid(p, **kwargs)

    """ hover tooltips """
    tooltips_bar = [
        (kwargs.get('x_tooltip_name', 'Group'), '@x'),
        (kwargs.get('bar_tooltip_name', left_axis_y_label),
         '@bar_values' + kwargs.get('bar_tooltip_format', '')
         ),
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

    """ legend"""
    legend = Legend(items=[
        LegendItem(label=left_axis_y_label + ': ' + bar_variables[0], renderers=[bar_chart], index=0),
        LegendItem(label=left_axis_y_label + ': ' + bar_variables[1], renderers=[bar_chart], index=1),
        LegendItem(label=right_axis_y_label, renderers=[line_chart], index=0),
    ], location=kwargs.get('legend_location', (10, 10)))

    p.add_layout(legend, kwargs.get('legend_placement', 'below'))

    return p


def plot_multiple_bar_chart(df: pd.DataFrame, title: str, x_axis: str, y_axis: str, x_axis_categories: str,
                            md_color_shade: str = 'lightblue', show_legend: bool = False, **kwargs) -> figure:
    """
    Creates a Bokeh multiple bar chart

    :param df: dataframe with the x and y values
    :param title: title for figure
    :param x_axis: column name in df used for the x axis
    :param y_axis: column name in df used for the y axis
    :param x_axis_categories: column name in df used to assign x axis categories
    :param md_color_shade: the colour name used by Material Design
    :param show_legend: if legend should be shown
    :param kwargs: extra information
    :return: Bokeh figure with multiple bar chart
    """
    """ prepare data """
    if (x_axis in df.index.names) | (y_axis in df.index.names):
        df.reset_index(inplace=True)

    df_pivot = df.pivot(index=x_axis, columns=x_axis_categories, values=y_axis)

    x = [(x_ind, y_ind) for x_ind in df_pivot.index.map(str) for y_ind in df_pivot.columns.map(str)]

    df_pivot_as_list = [item for sublist in df_pivot.as_matrix() for item in sublist]

    """ colours """
    try:
        colours = create_multi_colour_pallete(md_color_shade)
    except KeyError:
        md_colour_names = get_material_design_colours().keys()
        warnings.warn(
            """{} is not in the colour palette of Material Design. Select one of the following colours:\n{}"""
                .format(md_color_shade, ', '.join(md_colour_names))
        )
        colours = create_multi_colour_pallete('lightblue')

    palette = colours[0:len(df_pivot.columns)] * len(df_pivot.index)

    """ bar chart """
    source = ColumnDataSource(data=dict(x=x, y=df_pivot_as_list, palette=palette))

    custom_hover = HoverTool()

    p = figure(
        x_range=FactorRange(*x),
        title=title,
        plot_width=kwargs.get('plot_width', 700),
        plot_height=kwargs.get('plot_height', 400),
        tools=[custom_hover, 'save'])

    if len(colours) < len(df_pivot.columns):
        raise IndexError("""There are more categories ({} categories) than colours ({} colours). 
                            Increase number of colours or reduce category number.""".format(len(df_pivot.columns),
                                                                                            len(colours)))
    bar_chart = p.vbar(
        x='x',
        top='y',
        fill_color='palette',
        source=source,
        width=kwargs.get('bar_width', 0.9),
        line_color="white",
    )

    """ hover tooltips """
    tooltips = [
        ('{},{}'.format(x_axis, x_axis_categories), "@x" + kwargs.get('x_tooltip_format', '')),
        (y_axis, "@y" + kwargs.get('y_tooltip_format', ''))
    ]
    custom_hover.tooltips = get_custom_hover_tooltips(tooltips)

    p.add_tools(custom_hover)

    """ axis """
    y_axis_label = kwargs.get('y_axis_label', y_axis)
    x_axis_label = kwargs.get('x_axis_label', x_axis)
    x_category_label = kwargs.get('x_categories', x_axis_categories)

    p.xaxis.axis_label = '{} by {}'.format(x_category_label, x_axis_label)
    p.yaxis.axis_label = y_axis_label
    p = format_axis(p, **kwargs)
    p = format_grid(p, **kwargs)

    """ legend """
    if show_legend:
        bar_variables = df[x_axis_categories].unique()
        legend = Legend(items=[
            LegendItem(label=x_category_label + ': ' + bar_variables[i].astype(str), renderers=[bar_chart], index=i)
            for i in range(len(bar_variables))
        ], location=kwargs.get('legend_location', (10, 10)))

        p.add_layout(legend, kwargs.get('legend_placement', 'right'))

    return p


def plot_single_line(df: pd.DataFrame, x_axis: str, y_axis: str, title: str, x_axis_type: str = 'datetime',
                     colour_name: str = 'blue', colour_code: str = '500', md_design_colour: bool = True,
                     show_legend: bool = False, **kwargs) -> figure:
    """
    Creates a single line Bokeh chart

    :param df: dataframe with the x and y values
    :param x_axis: column name in df used for the x axis
    :param y_axis: column name in df used for the y axis
    :param title: title for figure
    :param x_axis_type: if axis type is datetime or linear (default: datetime)
    :param colour_name: colour name used by material design
    :param colour_code: colour code used by material desgin
    :param md_design_colour: if we should use Material Design's colours, otherwise a hex code can be passed in line_colour
    :param show_legend: if legend should be shown
    :param kwargs: extra information that can be passed
    :return: Bokehfigure with line chart
    """
    """ prepare data """
    if (x_axis in df.index.names) | (y_axis in df.index.names):
        df.reset_index(inplace=True)

    if x_axis_type == 'datetime':
        df = df.sort_values(x_axis, ascending=True)

    source = ColumnDataSource(df)

    """ line plot """
    custom_hover = HoverTool()

    p = figure(x_axis_type=x_axis_type, title=title, plot_width=kwargs.get('plot_width', 700),
               plot_height=kwargs.get('plot_height', 350), tools=[custom_hover, 'save'])

    if md_design_colour:
        line_colour = get_colour_hex_code(
            colour_name,
            colour_code
        )
    else:
        line_colour = kwargs.get('line_colour', '#2196f3')

    line_chart = p.line(x_axis, y_axis, line_width=kwargs.get('line_width', 1), color=line_colour, source=source)

    """ hover tooltips """
    x_axis_default_format = "{%F, %A}" if x_axis_type == 'datetime' else ''
    tooltips = [(x_axis, "@" + x_axis + kwargs.get('x_tooltip_format', x_axis_default_format)),
                (y_axis, "@" + y_axis + kwargs.get('y_tooltip_format', '{0,0}'))]
    custom_hover.tooltips = get_custom_hover_tooltips(tooltips)
    custom_hover.formatters = {x_axis: x_axis_type}
    p.add_tools(custom_hover)

    """ legend """
    if show_legend:
        legend = Legend(
            items=[LegendItem(label=kwargs.get('y_axis_label', y_axis), renderers=[line_chart], index=0)],
            location=kwargs.get('legend_location', (10, 10))
        )

        p.add_layout(legend, kwargs.get('legend_placement', 'below'))

    """ axis """
    p.xaxis.axis_label = kwargs.get('x_axis_label', x_axis)
    p.yaxis.axis_label = kwargs.get('y_axis_label', y_axis)
    p = format_axis(p, **kwargs)
    p = format_grid(p, **kwargs)

    return p


def plot_multiple_lines(df: pd.DataFrame, title: str, x_axis: str, y_axis: str, category_column: str,
                        x_axis_type: str = 'datetime', **kwargs):
    """
    Cretes plot with multiple lines
    :param df:
    :param title:
    :param x_axis:
    :param y_axis:
    :param category_column:
    :param x_axis_type:
    :param kwargs:
    :return:
    """

    """ prepare data """
    if (x_axis in df.index.names) | (y_axis in df.index.names):
        df.reset_index(inplace=True)

    df[category_column] = df[category_column].apply(str)
    df_pivoted = df.pivot(index=x_axis, columns=category_column, values=y_axis)

    """ Multiple line chart """
    custom_hover = HoverTool()
    p = figure(x_axis_type=x_axis_type, title=title, plot_width=kwargs.get('plot_width', 800),
               plot_height=kwargs.get('plot_height', 400), tools=[custom_hover, 'save'])

    legend_list = []

    source = ColumnDataSource(df_pivoted)

    colours = create_multi_colour_pallete()
    if len(colours) < len(df[category_column].unique()):
        raise IndexError("""There are more categorical ({} categories) columns than there are colours ({} colours). 
                                Reduce categories or add more colours.""".format(str(len(df[category_column].unique())),
                                                                                 str(len(colours))))

    for ind, category_line in enumerate(df_pivoted.columns):
        line_g = p.line(
            x_axis,
            category_line,
            line_width=kwargs.get('line_width', 1),
            color=colours[ind],
            line_alpha=kwargs.get('line_alpha', 0.9),
            source=source
        )
        legend_list.append(LegendItem(label=category_line, renderers=[line_g], index=ind))

    """ hover tooltips """
    x_axis_default_format = '{%F, %A}' if x_axis_type == 'datetime' else ''
    tooltips = [(x_axis, "@" + x_axis + kwargs.get('x_tooltip_format', x_axis_default_format))] + \
               [("{} of {} {}".format(y_axis, category_column, y),
                 "@" + y + kwargs.get('y_tooltip_format', '{0,0}')) for y in df_pivoted.columns]

    custom_hover.tooltips = get_custom_hover_tooltips(tooltips)
    custom_hover.formatters = {x_axis: x_axis_type}

    """ legend """
    legend = Legend(items=legend_list, location=kwargs.get('legend_location', (10, 10)))
    p.add_layout(legend, kwargs.get('legend_placement', 'right'))

    """ axis """
    p.xaxis.axis_label = kwargs.get('x_axis_label', x_axis)
    p.yaxis.axis_label = kwargs.get('y_axis_label', y_axis)
    p = format_axis(p, **kwargs)
    p = format_grid(p, **kwargs)
    return p


def format_axis(p: figure, **kwargs) -> figure:
    p.yaxis[0].formatter = NumeralTickFormatter(format=kwargs.get("y_num_tick_formatter", '0.0'))
    p.x_range.range_padding = kwargs.get("x_range_padding", 0.1)
    p.xaxis.major_label_orientation = kwargs.get('x_label_orientation', 1)
    return p


def format_grid(p: figure, **kwargs) -> figure:
    p.xgrid.grid_line_color = kwargs.get('grid_line_colour', None)
    return p


# .bk-tooltip>div:not(:first-child) {display:none;}
def get_custom_hover_tooltips(tooltips: list) -> str:
    """ Function that forces only one hover tooltip to show at a time"""
    html_code = \
        """
        <style>
            .bk-tooltip:not(:first-child) ~ .bk-tooltip {display:none}
        </style>
        """
    for tooltip in tooltips:
        html_code += "<b>{} : </b> {} <br>".format(tooltip[0], tooltip[1])

    return html_code


def plot_table(df,
               header_style="color: #757575; font-family: Courier; font-weight:800",
               table_style="color: #757575; font-family: Courier; font-weight:normal",
               height=250):
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


def get_colour_hex_code(colour_name, colour_code):
    """
    Calls for the dictionary with colour and codes from Material Design and finds the right hex code based on colour
    name name and colour code.
    :param colour_name: name of MD colour #@todo: add names here
    :param colour_code:  the number of the gradient colour. #@todo: add codes here
    :return: hex code based on Material Design's colour name and colour code
    """
    md_colour_dict = get_material_design_colours()
    return md_colour_dict[colour_name][colour_code]


def create_multi_colour_pallete(colour_name: str = 'multi_colour', colour_number: str = '500') -> list:
    """
    Returns a pallete of colours.
    If a colour name is given, it returns all codes for that specific colour.
    Otherwise, it returns all colour codes that matches the colour number.

    Args:
        colour_name (str) -- colour name (e.g. red) as used by Material Design (default: multi_colour)
        colour_number (str) -- code used for colour strength for each colour

    Returns:
        colour palette as a list

    """
    material_design_colours = pd.DataFrame(get_material_design_colours())
    if colour_name == 'multi_colour':
        return list(material_design_colours.loc[colour_number])
    else:
        return list(material_design_colours[colour_name])


def get_material_design_colours() -> dict:
    """
    This function returns a dictionary with all colours of Material design. The keys are the names of the colours (e.g.:
    pink and the values are dictionaries, in which the key indicates the colour code number and the value the HEX code.
    :return: dictionary with colours, code numbers and HEX codes.
    """
    return {
        "red": {
            "50": "#ffebee",
            "100": "#ffcdd2",
            "200": "#ef9a9a",
            "300": "#e57373",
            "400": "#ef5350",
            "500": "#f44336",
            "600": "#e53935",
            "700": "#d32f2f",
            "800": "#c62828",
            "900": "#b71c1c",
            "a100": "#ff8a80",
            "a200": "#ff5252",
            "a400": "#ff1744",
            "a700": "#d50000"
        },
        "pink": {
            "50": "#fce4ec",
            "100": "#f8bbd0",
            "200": "#f48fb1",
            "300": "#f06292",
            "400": "#ec407a",
            "500": "#e91e63",
            "600": "#d81b60",
            "700": "#c2185b",
            "800": "#ad1457",
            "900": "#880e4f",
            "a100": "#ff80ab",
            "a200": "#ff4081",
            "a400": "#f50057",
            "a700": "#c51162"
        },
        "purple": {
            "50": "#f3e5f5",
            "100": "#e1bee7",
            "200": "#ce93d8",
            "300": "#ba68c8",
            "400": "#ab47bc",
            "500": "#9c27b0",
            "600": "#8e24aa",
            "700": "#7b1fa2",
            "800": "#6a1b9a",
            "900": "#4a148c",
            "a100": "#ea80fc",
            "a200": "#e040fb",
            "a400": "#d500f9",
            "a700": "#aa00ff"
        },
        "deeppurple": {
            "50": "#ede7f6",
            "100": "#d1c4e9",
            "200": "#b39ddb",
            "300": "#9575cd",
            "400": "#7e57c2",
            "500": "#673ab7",
            "600": "#5e35b1",
            "700": "#512da8",
            "800": "#4527a0",
            "900": "#311b92",
            "a100": "#b388ff",
            "a200": "#7c4dff",
            "a400": "#651fff",
            "a700": "#6200ea"
        },
        "indigo": {
            "50": "#e8eaf6",
            "100": "#c5cae9",
            "200": "#9fa8da",
            "300": "#7986cb",
            "400": "#5c6bc0",
            "500": "#3f51b5",
            "600": "#3949ab",
            "700": "#303f9f",
            "800": "#283593",
            "900": "#1a237e",
            "a100": "#8c9eff",
            "a200": "#536dfe",
            "a400": "#3d5afe",
            "a700": "#304ffe"
        },
        "blue": {
            "50": "#e3f2fd",
            "100": "#bbdefb",
            "200": "#90caf9",
            "300": "#64b5f6",
            "400": "#42a5f5",
            "500": "#2196f3",
            "600": "#1e88e5",
            "700": "#1976d2",
            "800": "#1565c0",
            "900": "#0d47a1",
            "a100": "#82b1ff",
            "a200": "#448aff",
            "a400": "#2979ff",
            "a700": "#2962ff"
        },
        "lightblue": {
            "50": "#e1f5fe",
            "100": "#b3e5fc",
            "200": "#81d4fa",
            "300": "#4fc3f7",
            "400": "#29b6f6",
            "500": "#03a9f4",
            "600": "#039be5",
            "700": "#0288d1",
            "800": "#0277bd",
            "900": "#01579b",
            "a100": "#80d8ff",
            "a200": "#40c4ff",
            "a400": "#00b0ff",
            "a700": "#0091ea"
        },
        "cyan": {
            "50": "#e0f7fa",
            "100": "#b2ebf2",
            "200": "#80deea",
            "300": "#4dd0e1",
            "400": "#26c6da",
            "500": "#00bcd4",
            "600": "#00acc1",
            "700": "#0097a7",
            "800": "#00838f",
            "900": "#006064",
            "a100": "#84ffff",
            "a200": "#18ffff",
            "a400": "#00e5ff",
            "a700": "#00b8d4"
        },
        "teal": {
            "50": "#e0f2f1",
            "100": "#b2dfdb",
            "200": "#80cbc4",
            "300": "#4db6ac",
            "400": "#26a69a",
            "500": "#009688",
            "600": "#00897b",
            "700": "#00796b",
            "800": "#00695c",
            "900": "#004d40",
            "a100": "#a7ffeb",
            "a200": "#64ffda",
            "a400": "#1de9b6",
            "a700": "#00bfa5"
        },
        "green": {
            "50": "#e8f5e9",
            "100": "#c8e6c9",
            "200": "#a5d6a7",
            "300": "#81c784",
            "400": "#66bb6a",
            "500": "#4caf50",
            "600": "#43a047",
            "700": "#388e3c",
            "800": "#2e7d32",
            "900": "#1b5e20",
            "a100": "#b9f6ca",
            "a200": "#69f0ae",
            "a400": "#00e676",
            "a700": "#00c853"
        },
        "lightgreen": {
            "50": "#f1f8e9",
            "100": "#dcedc8",
            "200": "#c5e1a5",
            "300": "#aed581",
            "400": "#9ccc65",
            "500": "#8bc34a",
            "600": "#7cb342",
            "700": "#689f38",
            "800": "#558b2f",
            "900": "#33691e",
            "a100": "#ccff90",
            "a200": "#b2ff59",
            "a400": "#76ff03",
            "a700": "#64dd17"
        },
        "lime": {
            "50": "#f9fbe7",
            "100": "#f0f4c3",
            "200": "#e6ee9c",
            "300": "#dce775",
            "400": "#d4e157",
            "500": "#cddc39",
            "600": "#c0ca33",
            "700": "#afb42b",
            "800": "#9e9d24",
            "900": "#827717",
            "a100": "#f4ff81",
            "a200": "#eeff41",
            "a400": "#c6ff00",
            "a700": "#aeea00"
        },
        "yellow": {
            "50": "#fffde7",
            "100": "#fff9c4",
            "200": "#fff59d",
            "300": "#fff176",
            "400": "#ffee58",
            "500": "#ffeb3b",
            "600": "#fdd835",
            "700": "#fbc02d",
            "800": "#f9a825",
            "900": "#f57f17",
            "a100": "#ffff8d",
            "a200": "#ffff00",
            "a400": "#ffea00",
            "a700": "#ffd600"
        },
        "amber": {
            "50": "#fff8e1",
            "100": "#ffecb3",
            "200": "#ffe082",
            "300": "#ffd54f",
            "400": "#ffca28",
            "500": "#ffc107",
            "600": "#ffb300",
            "700": "#ffa000",
            "800": "#ff8f00",
            "900": "#ff6f00",
            "a100": "#ffe57f",
            "a200": "#ffd740",
            "a400": "#ffc400",
            "a700": "#ffab00"
        },
        "orange": {
            "50": "#fff3e0",
            "100": "#ffe0b2",
            "200": "#ffcc80",
            "300": "#ffb74d",
            "400": "#ffa726",
            "500": "#ff9800",
            "600": "#fb8c00",
            "700": "#f57c00",
            "800": "#ef6c00",
            "900": "#e65100",
            "a100": "#ffd180",
            "a200": "#ffab40",
            "a400": "#ff9100",
            "a700": "#ff6d00"
        },
        "deeporange": {
            "50": "#fbe9e7",
            "100": "#ffccbc",
            "200": "#ffab91",
            "300": "#ff8a65",
            "400": "#ff7043",
            "500": "#ff5722",
            "600": "#f4511e",
            "700": "#e64a19",
            "800": "#d84315",
            "900": "#bf360c",
            "a100": "#ff9e80",
            "a200": "#ff6e40",
            "a400": "#ff3d00",
            "a700": "#dd2c00"
        },
        "brown": {
            "50": "#efebe9",
            "100": "#d7ccc8",
            "200": "#bcaaa4",
            "300": "#a1887f",
            "400": "#8d6e63",
            "500": "#795548",
            "600": "#6d4c41",
            "700": "#5d4037",
            "800": "#4e342e",
            "900": "#3e2723"
        },
        "grey": {
            "50": "#fafafa",
            "100": "#f5f5f5",
            "200": "#eeeeee",
            "300": "#e0e0e0",
            "400": "#bdbdbd",
            "500": "#9e9e9e",
            "600": "#757575",
            "700": "#616161",
            "800": "#424242",
            "900": "#212121"
        },
        "bluegrey": {
            "50": "#eceff1",
            "100": "#cfd8dc",
            "200": "#b0bec5",
            "300": "#90a4ae",
            "400": "#78909c",
            "500": "#607d8b",
            "600": "#546e7a",
            "700": "#455a64",
            "800": "#37474f",
            "900": "#263238"
        }
    }
