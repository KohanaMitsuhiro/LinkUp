import streamlit as st                                    # streamlit
from streamlit_folium import st_folium                    # streamlitでfoliumを使う
import folium                                             # folium
from folium import FeatureGroup                           # FeatureGrop
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





# >>> 物件のプロット >>>
bukken_df = pd.read_csv('bukken_0301.csv')

new_mansion_data = bukken_df[bukken_df["category"].str.contains("新築マンション")]
used_mansion_data = bukken_df[bukken_df["category"].str.contains("中古マンション")]
new_kodate_data = bukken_df[bukken_df["category"].str.contains("新築一戸建て")]
used_kodate_data = bukken_df[bukken_df["category"].str.contains("中古一戸建て")]


# 新築マンションのプロット
new_mansion_group = FeatureGroup(name="新築マンション")

for i, row in new_mansion_data.iterrows():
    html= f'''
        <a href= '{row.loc['url']}' target='_blank'>SUUMOで確認</a>'''
    iframe = folium.IFrame('【カテゴリー】: ' + row.loc['category'] + '<br>' + '【物件名】:' + row.loc['name']+ '<br>' + '【住所】:' + row.loc['adress']+'<br>' + '【最高価格】:' + str(row.loc['max_price'])+'<br>' + '【最低価格】:' + str(row.loc['min_price'])+'<br>' + '【最大面積】:' + str(row.loc['max_tatemono_measure'])+'<br>' + '【最小面積】:' + str(row.loc['min_tatemono_measure'])+'<br>' + '【最大間取り】:' + str(row.loc['max_madori'])+'<br>' + '【最小間取り】:' + str(row.loc['min_madori'])+'<br>' + '【最寄路線】:' + str(row.loc['nearest_line'])+'<br>' + '【最寄駅】:' + str(row.loc['nearest_station'])+'<br>' + '【最寄駅まで】:' + str(row.loc['walk_time'])+'<br>' + '【引渡可能時期】:' + str(row.loc['hikiwatashi']) +'<br>' + '【SUUMO】:' + str(row.loc['url']) )
    popup = folium.Popup(iframe, min_width=300, max_width=300)
    folium.Marker(
        location= [row["latitude"], row["longitude"]],
        popup= popup,
        icon= folium.Icon(icon="home", prefix="fa", icon_color="white", color="purple")
    ).add_to(new_mansion_group)

new_mansion_group.add_to(map)


# # 中古マンションのプロット
# used_mansion_group = FeatureGroup(name="中古マンション")

# for i, row in used_mansion_data.iterrows():
#     iframe = folium.IFrame('【カテゴリー】: ' + row.loc['category'] + '<br>' + '【物件名】:' + row.loc['name']+ '<br>' + '【住所】:' + row.loc['adress']+'<br>' + '【最高価格】:' + str(row.loc['max_price'])+'<br>' + '【最低価格】:' + str(row.loc['min_price'])+'<br>' + '【最大面積】:' + str(row.loc['max_tatemono_measure'])+'<br>' + '【最小面積】:' + str(row.loc['min_tatemono_measure'])+'<br>' + '【最大間取り】:' + str(row.loc['max_madori'])+'<br>' + '【最小間取り】:' + str(row.loc['min_madori'])+'<br>' + '【最寄路線】:' + str(row.loc['nearest_line'])+'<br>' + '【最寄駅】:' + str(row.loc['nearest_station'])+'<br>' + '【最寄駅まで】:' + str(row.loc['walk_time'])+'<br>' + '【引渡可能時期】:' + str(row.loc['hikiwatashi']) +'<br>' + '【SUUMO】:' + str(row.loc['url']))
#     popup = folium.Popup(iframe, min_width=300, max_width=300)
#     folium.Marker(
#         location= [row["latitude"], row["longitude"]],
#         popup= popup,
#         icon= folium.Icon(icon="home", prefix="fa", icon_color="white", color="pink")
#     ).add_to(used_mansion_group)

# used_mansion_group.add_to(map)


#　新築一戸建てのプロット
new_kodate_group = FeatureGroup(name="中古マンション")

for i, row in new_kodate_data.iterrows():
    iframe = folium.IFrame('【カテゴリー】: ' + row.loc['category'] + '<br>' + '【物件名】:' + row.loc['name']+ '<br>' + '【住所】:' + row.loc['adress']+'<br>' + '【最高価格】:' + str(row.loc['max_price'])+'<br>' + '【最低価格】:' + str(row.loc['min_price'])+'<br>' + '【最大面積】:' + str(row.loc['max_tatemono_measure'])+'<br>' + '【最小面積】:' + str(row.loc['min_tatemono_measure'])+'<br>' + '【最大間取り】:' + str(row.loc['max_madori'])+'<br>' + '【最小間取り】:' + str(row.loc['min_madori'])+'<br>' + '【最寄路線】:' + str(row.loc['nearest_line'])+'<br>' + '【最寄駅】:' + str(row.loc['nearest_station'])+'<br>' + '【最寄駅まで】:' + str(row.loc['walk_time'])+'<br>' + '【引渡可能時期】:' + str(row.loc['hikiwatashi']) +'<br>' + '【SUUMO】:' + str(row.loc['url']))
    popup = folium.Popup(iframe, min_width=300, max_width=300)
    folium.Marker(
        location= [row["latitude"], row["longitude"]],
        popup= popup,
        icon= folium.Icon(icon="home", prefix="fa", icon_color="white", color="orange")
    ).add_to(new_kodate_group)

new_kodate_group.add_to(map)


# #　中古一戸建てのプロット
# used_kodate_group = FeatureGroup(name="中古マンション")

# for i, row in new_kodate_data.iterrows():
#     iframe = folium.IFrame('【カテゴリー】: ' + row.loc['category'] + '<br>' + '【物件名】:' + row.loc['name']+ '<br>' + '【住所】:' + row.loc['adress']+'<br>' + '【最高価格】:' + str(row.loc['max_price'])+'<br>' + '【最低価格】:' + str(row.loc['min_price'])+'<br>' + '【最大面積】:' + str(row.loc['max_tatemono_measure'])+'<br>' + '【最小面積】:' + str(row.loc['min_tatemono_measure'])+'<br>' + '【最大間取り】:' + str(row.loc['max_madori'])+'<br>' + '【最小間取り】:' + str(row.loc['min_madori'])+'<br>' + '【最寄路線】:' + str(row.loc['nearest_line'])+'<br>' + '【最寄駅】:' + str(row.loc['nearest_station'])+'<br>' + '【最寄駅まで】:' + str(row.loc['walk_time'])+'<br>' + '【引渡可能時期】:' + str(row.loc['hikiwatashi']) +'<br>' + '【SUUMO】:' + str(row.loc['url']))
#     popup = folium.Popup(iframe, min_width=300, max_width=300)
#     folium.Marker(
#         location= [row["latitude"], row["longitude"]],
#         popup= popup,
#         icon= folium.Icon(icon="home", prefix="fa", icon_color="white", color="beige")
#     ).add_to(used_kodate_group)

# used_kodate_group.add_to(map)


st_folium(map, width=700, height=700)