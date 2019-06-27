import pandas as pd
from plot_functions import plot_single_line
from bokeh.layouts import Column, layout
from bokeh.plotting import output_file, show

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

show(
    layout(Column(p_mandatory, p_optional))
)
