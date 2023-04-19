import streamlit as st                                    # streamlit
from streamlit_folium import st_folium                    # streamlitでfoliumを使う
import folium                                             # folium
from folium import FeatureGroup                           # FeatureGrop
import pandas as pd                                       # CSVをデータフレームとして読み込む

# 表示するデータを読み込み
df = pd.read_csv("0224_hoikuen.csv")

# 区分ごとのデータを抽出
all_data = (df[df["区分"].str.contains("認可保育園|認証保育園|認可外保育施設")]) #全区分
ninka_data = df[df["区分"].str.contains("認可保育園")]
ninshou_data = df[df["区分"].str.contains("認証保育園")]
ninkagai_data = df[df["区分"].str.contains("認可外保育施設")]


# >>> Streamlit タイトル >>>
st.header("保育園マップ")
st.text("""
        左に表示されているプルダウンから保育園の区分を選んでください。
        選んだ区分の保育園が地図上に表示されます。
        """)
# <<< Streamlit タイトル <<<


# >>> Streamlit サイドバー >>>
# セレクトボックス
bland_options = st.sidebar.selectbox(
    "希望の保育園の区分をお選びください。",
    ["全て", "認可保育園", "認証保育園", "認可外保育施設"])
st.sidebar.write("現在の選択:", bland_options)



# >>> 地図 map の作成  >>>
# 地図の中心の緯度/経度、タイル、初期のズームサイズを指定
map = folium.Map(
    # 地図の中心位置の指定(今回は世田谷区玉川地区の玉川総合支所を指定)
    location=[35.608730497916845, 139.64832587827124],
    # タイル（デフォルトはOpenStreetMap)、アトリビュート(attr:右下の出典情報はデフォルト指定時は不要)指定
    tiles="OpenStreetMap",
    # ズームを指定
    # 参考URL：https://maps.gsi.go.jp/development/ichiran.html#pale
    zoom_start=13
)


# >>> 認可保育園のプロット (ninka_group) >>>
ninka_group = FeatureGroup(name="認可")

for i, row in ninka_data.iterrows():
    iframe = folium.IFrame('・区分: ' + row.loc['区分'] + '<br>' + '・名称:' + row.loc['名称']+ '<br>' + '・定員:' + row.loc['定員']+'<br>' + '・1歳定員:' + str(row.loc['1歳定員']) )
    popup = folium.Popup(iframe, min_width=300, max_width=300)
    folium.Circle(
        location= [row["latitude"], row["longitude"]],
        popup= popup,
        radius= 10,
        fill= True,
        color= 'blue'
    ).add_to(ninka_group)
# <<<  認可保育園のプロット (ninka_group) <<<


# >>> 認証保育園のプロット (nishou_group) >>>    
ninshou_group = FeatureGroup(name="認証")

for i, row in ninshou_data.iterrows():
    iframe = folium.IFrame('・区分: ' + row.loc['区分'] + '<br>' + '・名称:' + row.loc['名称']+ '<br>' + '・定員:' + row.loc['定員']+'<br>' + '・1歳定員:' + str(row.loc['1歳定員']) )
    popup = folium.Popup(iframe, min_width=300, max_width=300)
    folium.Circle(
        location= [row["latitude"], row["longitude"]],
        popup= popup,
        radius= 10,
        fill= True,
        color= 'green'
    ).add_to(ninshou_group)
# <<<  認証保育園のプロット (nishou_group)<<<



# >>> 認可外保育施設のプロット (nishou_group) >>>      
ninkagai_group = FeatureGroup(name="認可外")

for i, row in ninkagai_data.iterrows():
    iframe = folium.IFrame('・区分: ' + row.loc['区分'] + '<br>' + '・名称:' + row.loc['名称']+ '<br>' + '・定員:' + row.loc['定員']+'<br>' + '・1歳定員:' + str(row.loc['1歳定員']) )
    popup = folium.Popup(iframe, min_width=300, max_width=300)
    folium.Circle(
        location= [row["latitude"], row["longitude"]],
        popup= popup,
        radius= 10,
        fill= True,
        color= 'red'
    ).add_to(ninkagai_group)
# <<< 認可外保育施設のプロット (nishou_group) <<<



# セレクトボックスの選択支に合わせて表示させる
if bland_options == "全て":
    ninka_group.add_to(map)
    ninshou_group.add_to(map)
    ninkagai_group.add_to(map)
    st_folium(map, width=700, height=700)

if bland_options == "認可保育園":
    ninka_group.add_to(map)
    st_folium(map, width=700, height=700)

if bland_options == "認証保育園":
    ninshou_group.add_to(map)
    st_folium(map, width=700, height=700)

if bland_options == "認可外保育施設":
    ninkagai_group.add_to(map)
    st_folium(map, width=700, height=700)


