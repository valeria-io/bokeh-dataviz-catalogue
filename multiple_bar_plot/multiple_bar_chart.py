import pandas as pd
from bokeh.plotting import output_file, show
from bokeh.layouts import Column, Row, layout
from plot_functions import plot_multiple_bar_chart
from bokeh.models.widgets import Div


df = pd.read_csv('../static/data/yearly_sales_by_store.csv')

output_file("multiple_bar_chart.html")

p = plot_multiple_bar_chart(
    df,
    title='Total sales by store and year',
    x_axis='year',
    y_axis= 'sales',
    x_axis_categories='store',
    y_tooltip_format='{0,0}',
    y_axis_format='0.0a'
)

show(p)