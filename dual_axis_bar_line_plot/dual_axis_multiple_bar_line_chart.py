import pandas as pd
from bokeh.plotting import output_file, show
from bokeh.layouts import Column, Row, layout
from plot_functions import plot_dual_axis_dual_bar_line, plot_table
from bokeh.models.widgets import Div

df = pd.read_csv('../static/data/max_profit_by_age_group.csv', index_col=[0]).rename(
    columns={'TruePositiveRate0': '+ 40', 'TruePositiveRate1': '< 40'})

df_melt = df.melt(id_vars=['IntervationName', 'Profit'],
                  value_vars=['+ 40', '< 40'],
                  var_name='GroupName',
                  value_name='TruePositiveRate')

output_file("../docs/index.html")

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


text_table = Div(
    text="""
    <h2 style='margin-block-end:0'> Data used in graph</h2>
    <span style='color: #616161'><i>Scrollable table</i></span>
    """
)


text_function_mandatory = Div(
    text="""
    <h2 style='margin-block-end:0'>Graph 1: Function with mandatory parameters</h2>
    <p style="font-family: 'Helvetica Neue', Arial"> Obligatory parameters are: title, group name for the x axis, the 
    column name for the bar variables, the column name for the line and the names for the left and right axis values.
    </p>
    <br>
    <div style='background: #424242; padding:20px'>
        <span style='font-family: courier; font-weight: 500; color: #e0e0e0'>plot_dual_axis_dual_bar_line(</span>
        <ul style='font-family: courier; font-weight: 500; color: #e0e0e0'>
                <li style='list-style-type : none'>
                <span style="color:#8c9eff">df = </span>
                df_melt
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #pd.DataFrame </span>
            </li>
            <li style='list-style-type : none'>
                <span style="color:#8c9eff">title = </span>
                "TPR by group and profit"
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #str </span>
            </li>
            <li style='list-style-type : none'>
                <span style="color:#8c9eff">groups_name =</span>
                "IntervationName"
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #str </span>
            </li>
            <li style='list-style-type : none'>
                <span style="color:#8c9eff">bar_value_name =</span>
                "TruePositiveRate"
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #str </span></li>
            <li style='list-style-type : none'>
                <span style="color:#8c9eff">bar_variable_name =</span>
                "GroupName"
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #str </span>
            </li>
            <li style='list-style-type : none'>
                <span style="color:#8c9eff">line_variable_name =</span>
                "Profit"<span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #str </span>
            </li>        
        </ul>
        <span style='font-family: courier; font-weight: 600; color: #e0e0e0'>)</span>
        <br><br>
    </div>
    """
)

text_mandatory = Div(
    text="""
    <h2 style='margin-block-end:0'> Graph 1: Using only default function parameters</h2>
    <br><br>
    """, width=700)


sep_text = Div(
    text="""
    <div style='border-bottom-style: solid;  border-bottom-width: 2px; width:1590px; height:2px; 
    border-bottom-color: #cfcfcf'>
    </div>
    """, width=1590
)

text_function_optional = Div(
    text="""
    <h2 style='margin-block-end:0'>Graph 2: Function with additional optional parameters</h2>
    <p style="font-family: 'Helvetica Neue', Arial"> In addition to the obligatory parameters, we can add many other
    optionals as seen in the function below.
    </p>
    <br>
    <div style='background: #424242; padding:20px'>
        <span style='font-family: courier; font-weight: 500; color: #e0e0e0'>plot_dual_axis_dual_bar_line(</span>
        <ul style='font-family: courier; font-weight: 500; color: #e0e0e0'>
            <li style='list-style-type : none'>
                <span><i>...all parameters as in the previous graph and optionally:</i></span></li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>left_axis_y_label</span>
                <span> = </span>
                <span>"TPR"</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #str </span>
            </li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>right_axis_y_label</span>
                <span> = </span>
                <span>"Profit"</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #str </span>
            </li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>plot_height</span>
                <span> = </span>
                <span>450</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #int </span>
            </li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>plot_width</span>
                <span> = </span>
                <span>800</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #int </span>
            </li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>bar_colours</span>
                <span> = </span>
                <span>['#039be5', '#29b6f6']</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #list </span>
            </li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>bar_width</span>
                <span> = </span>
                <span>0.95</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #float </span>
            </li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>line_colour</span>
                <span> = </span>
                <span>"#ff9800</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #str </span>
            </li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>line_width</span>
                <span> = </span>
                <span>3</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #int </span>
            </li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>circle_size</span>
                <span> = </span>
                <span>10</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #int </span>
            </li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>max_left_y_range</span>
                <span> = </span>
                <span>1.0</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #float </span>
            </li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>min_right_y_range</span>
                <span> = </span>
                <span>0.0</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #float </span>
            </li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>y_num_tick_formatter</span>
                <span> = </span>
                <span>'0 %'</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #str </span>
            </li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>bar_tooltip_format</span>
                <span> = </span>
                <span>'{0 %}'</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #str </span>
            </li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>legend_location</span>
                <span> = </span>
                <span>(10, 10)</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #Tuple(int, int) </span>
            </li>
            <li style='list-style-type : none'>
                <span style='color: #8c9eff'>legend_placement</span>
                <span> = </span>
                <span>"right"</span>
                <span style='color: #ff9100'>,</span>
                <span style='color: #9e9e9e'> #str </span>
            </li>
        </ul>
        <span style='font-family: courier; font-weight: 600; color: #e0e0e0'>)</span>
        <br><br>
    </div>
    """
)
text_optional = Div(
    text="""
    <h2 style='margin-block-end:0'> Graph 2: Using additional and optional function parameters</h2><br><br>
    """
    , width=700)



show(
    layout(
        Row(
            Column(text_function_mandatory, text_table, data_table, margin=[40, 80, 50, 50]),
            Column(text_mandatory, p_mandatory, margin=[40, 0, 25, 50]),
        ),
        Row(
          Column(sep_text)
        ),
        Row(
            Column(text_function_optional, text_table, data_table, margin=[40, 80, 25, 50]),
            Column(text_optional, p_optional, margin=[40, 0, 25, 50]),
        )
    )
)



