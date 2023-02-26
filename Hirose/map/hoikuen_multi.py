import streamlit as st                                    # streamlit
from streamlit_folium import st_folium                    # streamlitでfoliumを使う
import folium                                             # folium
# from folium import FeatureGroup                         # FeatureGrop
import pandas as pd                                       # CSVをデータフレームとして読み込む


# 表示するデータを読み込み
df = pd.read_csv("0224_hoikuen.csv")

ninka_data = df[df["区分"].str.contains("認可保育園")]
ninshou_data = df[df["区分"].str.contains("認証保育園")]
ninkagai_data = df[df["区分"].str.contains("認可外保育施設")]

# Streamlit タイトル 
st.header("保育園マップ")

# 区分の列にあるすべての区分をリスト化する
type_list= list(df['区分'].unique())

# マルチセレクトの作成
selections= st.multiselect("ご希望の保育園区分をお選びください", type_list, default='認可保育園')

# セレクトされた区分でデータフレームの中身をフィルタリングする
df2 = df[(df['区分'].isin(selections))]

# 地図の作成
map = folium.Map(
    # 地図の中心位置の指定(今回は世田谷区玉川地区の玉川総合支所を指定)
    location=[35.608730497916845, 139.64832587827124],
    # タイル（デフォルトはOpenStreetMap)、アトリビュート(attr:右下の出典情報はデフォルト指定時は不要)指定
    tiles="OpenStreetMap",
    # ズームを指定
    # 参考URL：https://maps.gsi.go.jp/development/ichiran.html#pale
    zoom_start=13
)


# # マルチセレクトで選んだ区分によってマーカーのカラーを指定する関数
# def color_producer(selections):
#     if selections == "認可保育園":
#         return 'red'
#     if selections == '認証保育園':
#         return 'blue'
#     if selections =='認可外保育園':
#         return 'green'


# 保育園の区分（マルチセレクト）とプロットを連動させる
for i, row in df2.iterrows():
    iframe = folium.IFrame('・区分: ' + row.loc['区分'] + '<br>' + '・名称:' + row.loc['名称']+ '<br>' + '・定員:' + row.loc['定員']+'<br>' + '・1歳定員:' + str(row.loc['1歳定員']) )
    popup = folium.Popup(iframe, min_width=300, max_width=300)
    folium.Circle(
        location= [row["latitude"], row["longitude"]],
        tooltip= row["名称"],
        popup= popup,
        radius= 10,
        fill= True,
        color= 'red'
    ).add_to(map)

st_folium(map, width=700, height=700)