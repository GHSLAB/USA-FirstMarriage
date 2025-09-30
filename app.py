import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd


## Data
data_file = "data/2023.xlsx"
df_m = pd.read_excel(data_file, sheet_name="Male", header=None)
df_f = pd.read_excel(data_file, sheet_name="Female", header=None)
df_m.columns = ["State", "M_Rank", "M_MedianAge"]
df_f.columns = ["State", "F_Rank", "F_MedianAge"]

### figure male
fig_m = px.bar(
    df_m,
    x="State",
    y="M_MedianAge",
    title="Median Age at First Marriage by State (Males)",
    color="M_MedianAge",
    labels={"M_MedianAge": "Median Age"},
)

fig_m.add_vline(
    x=df_m[df_m["State"] == "USA"].index[0],
    line_width=2,
    line_dash="dash",
    line_color="#d63031",
)

### figure Female
fig_f = px.bar(
    df_f,
    x="State",
    y="F_MedianAge",
    title="Median Age at First Marriage by State (Females)",
    color="F_MedianAge",
    labels={"F_MedianAge": "Median Age"},
)

fig_f.add_vline(
    x=df_f[df_f["State"] == "USA"].index[0],
    line_width=2,
    line_dash="dash",
    line_color="#d63031",
)


### figure vs
df_all = pd.merge(df_m, df_f, on="State")
df_all["MedianAge_diff"] = round(df_all["M_MedianAge"] - df_all["F_MedianAge"], 2)

# 创建条形图显示各州的中位数年龄
fig_vs = px.bar(
    df_all,
    x="State",
    y="MedianAge_diff",
    title="Median Age at First Marriage by State (M-F difference)",
    color="MedianAge_diff",
    labels={"MedianAge_diff": "Median Age Diff"},
)
# 为USA添加竖虚线
fig_vs.add_vline(
    x=df_all[df_all["State"] == "USA"].index[0],
    line_width=2,
    line_dash="dash",
    line_color="#d63031",
)

### Map
state_code = pd.read_csv("data/usa_state_code.csv")
df_all = pd.merge(df_all, state_code, on="State")

map_1 = px.choropleth(
    df_all,
    locations="Alpha code",  # 州名列
    locationmode="USA-states",  # 设置为美国州级地图
    color="M_MedianAge",  # 根据中位数年龄着色
    scope="usa",  # 限定美国地图范围
    title="Male Median Age at First Marriage by State",
    color_continuous_scale="Viridis",  # 颜色方案
    hover_data=["State", "M_Rank", "F_Rank", "M_MedianAge", "F_MedianAge"],
)

map_1.update_layout(
    showlegend=True,
    margin=dict(l=0, r=0, t=50, b=10),
    autosize=False,  # 禁用自动调整大小
)

# 假设您的数据框df_m包含'State'列和'MedianAge'列
map_2 = px.choropleth(
    df_all,
    locations="Alpha code",  # 州名列
    locationmode="USA-states",  # 设置为美国州级地图
    color="F_MedianAge",  # 根据中位数年龄着色
    scope="usa",  # 限定美国地图范围
    title="Female Median Age at First Marriage by State",
    color_continuous_scale="Viridis",  # 颜色方案
    hover_data=[
        "State",
        "M_Rank",
        "F_Rank",
        "M_MedianAge",
        "F_MedianAge",
        "MedianAge_diff",
    ],
)

map_2.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>"
    + "Male Rank: %{customdata[1]}<br>"
    + "Female Rank: %{customdata[2]}<br>"
    + "Male Median Age: %{customdata[3]}<br>"
    + "Female Median Age: %{customdata[4]}<br>"
    + "Difference: %{customdata[5]}<br>"
    + "<extra></extra>"
)

map_2.update_layout(
    showlegend=True,
    margin=dict(l=0, r=0, t=50, b=0),
    #    width=1000,  # 设置宽度
    # height=600,  # 设置高度
    autosize=False,  # 禁用自动调整大小
)


## APP
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="USA First Marriage Median Age"),
        #     html.P(
        #         children="""
        #     Median Age at First Marriage: Geographic Variation
        # """
        #     ),
        dcc.Graph(figure=fig_m),
        dcc.Graph(figure=fig_f),
        dcc.Graph(figure=fig_vs),
        html.Div(
            [
                html.Div(
                    dcc.Graph(figure=map_1),
                    style={"width": "50%", "display": "inline-block"},
                ),
                html.Div(
                    dcc.Graph(figure=map_2),
                    style={"width": "50%", "display": "inline-block"},
                ),
            ],
            style={"display": "flex", "justifyContent": "space-between"},
        ),
    ],
    style={"padding": 20},
)


if __name__ == "__main__":
    app.run(debug=True)
