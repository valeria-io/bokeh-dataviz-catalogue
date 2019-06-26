import pandas as pd
from bokeh.plotting import output_file, show
from bokeh.layouts import Column, layout
from plot_functions import plot_dual_axis_dual_bar_line, plot_table
from bokeh.models.widgets import Div

df = pd.read_csv('../static/data/max_profit_by_age_group.csv', index_col=[0]).rename(
    columns={'TruePositiveRate0': '+ 40', 'TruePositiveRate1': '< 40'})

df_melt = df.melt(id_vars=['IntervationName', 'Profit'],
                  value_vars=['+ 40', '< 40'],
                  var_name='GroupName',
                  value_name='TruePositiveRate')

output_file("dual_axis_multiple_bar_line_chart.html")

p_mandatory = plot_dual_axis_dual_bar_line(
    df=df_melt,
    title="TPR by group and profit",
    groups_name='IntervationName',
    bar_value_name='TruePositiveRate',
    bar_variable_name='GroupName',
    line_variable_name='Profit',
)

p_optional = plot_dual_axis_dual_bar_line(
    df_melt,
    title="TPR by group and profit",
    groups_name='IntervationName',
    bar_value_name='TruePositiveRate',
    bar_variable_name='GroupName',
    line_variable_name='Profit',
    left_axis_y_label='TPR',
    right_axis_y_label='Profit',
    plot_height=450,
    plot_width=800,
    bar_colours=['#c5cae9', '#7986cb'],
    bar_width=0.95,
    line_colour='#ff9800',
    line_width=3,
    circle_size=10,
    max_left_y_range=1.0,
    min_right_y_range=0.0,
    y_num_tick_formatter='0 %',
    bar_tooltip_format='{0 %}',
    legend_location=(10, 10),
    legend_placement='right'
)

data_table = plot_table(
    df_melt[['GroupName', 'IntervationName', 'Profit', 'TruePositiveRate']].sort_values(by=['IntervationName'])
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



