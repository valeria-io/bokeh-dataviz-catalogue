import pandas as pd
from plot_functions import plot_multiple_lines, plot_table
from bokeh.layouts import Column, Row, layout
from bokeh.plotting import output_file, show
from bokeh.models.widgets import Div


df = pd.read_csv('../static/data/daily_sales_by_store.csv')
df = df[df['store'] < 6]
df['date'] = pd.to_datetime(df['date'])

output_file("multiple_line_chart.html")

p_mandatory = plot_multiple_lines(
    df=df,
    x_axis='date',
    y_axis='sales',
    category_column='store',
    title='Total sales',
)

p_optional = plot_multiple_lines(
    df=df,
    x_axis='date',
    y_axis='sales',
    category_column='store',
    title='Total sales',
    show_legend=True,
    plot_width=900,
    plot_height=450,
    legend_placement='right',
    line_width=1.5,
    line_alpha=0.5,
    y_num_tick_formatter='0.0a',
    y_axis_label='Total Sales by Store',
    x_axis_label=''
)
df['date'] = pd.to_datetime(df['date']).astype(str)
data_table = plot_table(df)

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
        Row(Column(text_mandatory, p_mandatory, text_optional, p_optional, text_table, data_table)),
        )
)