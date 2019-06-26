import pandas as pd
from bokeh.plotting import output_file, show
from bokeh.layouts import Column, Row, layout
from plot_functions import plot_multiple_bar_chart, plot_table
from bokeh.models.widgets import Div


df = pd.read_csv('../static/data/yearly_sales_by_store.csv')

output_file("multiple_bar_chart.html")

p_mandatory = plot_multiple_bar_chart(
    df,
    title='Total sales by store and year',
    x_axis='year',
    y_axis='sales',
    x_axis_categories='store',
)

p_optional = plot_multiple_bar_chart(
    df,
    title='Total sales by store and year',
    x_axis='year',
    y_axis='sales',
    x_axis_categories='store',
    md_color_shade='indigo',
    bar_width=0.95,
    y_tooltip_format='{0,0}',
    y_num_tick_formatter='0.0a',
    plot_width=800,
    plot_height=500,
    x_label_orientation=0.5,
    y_axis_label='Sales',
    x_axis_label='Year',
    x_categories='Store Nr',
    show_legend=True
)

data_table = plot_table(
    df
)

text_mandatory = Div(
    text="""
    <h2 style='margin-block-end:0'> Graph 1: Using mandatory parameters only </h2>
    """
)
text_optional= Div(
    text="""
    <h2 style='margin-block-end:0'> Graph 2: Using additional and optional function parameters </h2>
    """
)
text_table = Div(
    text="""
    <h2 style='margin-block-end:0'> Data used in graph</h2>
    <span style='color: #616161'><i>Scrollable table</i></span>
    """
)

show(
    layout(
        Column(text_mandatory, p_mandatory, text_optional, p_optional, text_table, data_table)
    )
)


#print(tabulate(df_, tablefmt="github", headers="keys", showindex=False))