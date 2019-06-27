import pandas as pd
from plot_functions import plot_single_line, plot_table
from bokeh.layouts import Column, Row, layout
from bokeh.plotting import output_file, show
from bokeh.models.widgets import Div


df = pd.read_csv('../static/data/daily_sales.csv')
df['date'] = pd.to_datetime(df['date'])

output_file("line_chart.html")

p_mandatory = plot_single_line(
    df=df,
    x_axis='date',
    y_axis='sales',
    title='Total sales',
)

p_optional = plot_single_line(
    df=df,
    x_axis='date',
    y_axis='sales',
    title='Total sales',
    show_legend=True,
    colour_name='amber',
    colour_code='600',
    plot_width=900,
    plot_height=450,
    legend_placement='right',
    line_width=1.5,
    y_num_tick_formatter='0.0a',
    y_axis_label='Total Sales',
    x_axis_label=''
)

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
# show(
#     layout(
#         Row(Column(text_mandatory, p_mandatory, text_optional, p_optional, text_table, data_table)),
#         )
# )
from tabulate import tabulate
print(tabulate(df.sort_values('date'), tablefmt="github", headers="keys", showindex=False))