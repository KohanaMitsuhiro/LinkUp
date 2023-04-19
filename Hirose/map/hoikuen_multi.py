import folium
import streamlit as st 
from streamlit_folium import st_folium 
from folium import FeatureGroup  
import pandas as pd
from datetime import datetime

# データの読み込み
nursery_data = pd.read_csv("hoikuen_0317.csv")
bukken_data = pd.read_csv("bukken_0322.csv")

# 各年齢の定員の列に欠損値がある⇒欠損値処理（-を入れる）
nursery_data = nursery_data.fillna({"0歳定員":"-", "1歳定員":"-", "2歳定員":"-", "3歳定員":"-","4歳定員":"-","5歳定員":"-"})


# >>> Streamlit タイトル >>>
st.header("保活者のための物件検索サイト")
st.text("""
        認可保育園の入りやすさを示す「新規入園率」からエリアを絞ったり、
        間取りや価格だけでなく、周辺の保育園情報も確認しながら物件を探すことができます。
        """)
# <<< Streamlit タイトル <<<


# >>> 検索条件設定 >>>

# >>> 都道府県を選ぶ  >>>
prefectures = bukken_data['prefecture'].unique().tolist()
selected_prefecture = st.selectbox ('不動産購入を都道府県から探す', prefectures)
# <<< 都道府県を選ぶ <<<


# >>> 市区群を選ぶ  >>>
# 選択された都道府県に該当する市区群名のリストを作成
cities = bukken_data[bukken_data['prefecture']==selected_prefecture]['city'].unique().tolist()
selected_city = st.selectbox ('市区群から探す', cities)

# 都道府県 ×　市区群 の絞込みデータ
area_data = bukken_data[(bukken_data['prefecture'] == selected_prefecture) & (bukken_data['city'] == selected_city)]

# <<< 市区群を選ぶ <<<


# >>> 物件種類を選ぶ  >>>
st.write('物件種類（複数選択可）') 

selected_categories = []
if st.checkbox('新築マンション'):
    selected_categories.append("新築マンション")
if st.checkbox('中古マンション'):
    selected_categories.append("中古マンション")
if st.checkbox('新築戸建て'):
    selected_categories.append("新築戸建て")
if st.checkbox('中古一戸建て'):
    selected_categories.append("中古一戸建て")

# 都道府県 ×　市区群 ×　物件種類 の絞込みデータ
categorized_bukken_data = bukken_data[(bukken_data['prefecture'] == selected_prefecture) & (bukken_data['city'] == selected_city) & (bukken_data['main_category'].isin(selected_categories))]

# ==マルチセレクトにするときはこっちのコード＝＝
# bukken_categories = bukken_data['main_category'].unique().tolist()
# selected_categories = st.multiselect('物件種類を選ぶ', bukken_categories)

# <<< 物件種類を選ぶ <<<



# >>> 間取りを選ぶ  >>>
st.write('間取り（複数選択可）')

selected_madori = []
if st.checkbox('ワンルーム'):
    selected_madori.append('ワンルーム')
if st.checkbox('1K/DK/LDK'):
    selected_madori.append('1K/DK/LDK')
if st.checkbox('2K/DK/LDK'):
    selected_madori.append('2K/DK/LDK')
if st.checkbox('3K/DK/LDK'):
    selected_madori.append('3K/DK/LDK')
if st.checkbox('4K/DK/LDK'):
    selected_madori.append('4K/DK/LDK')
if st.checkbox('5K以上'):
    selected_madori.append('5K以上')

# ===マルチセレクトの時はこちらのコード===
# madori = bukken_data['main_madori'].unique().tolist() #最大か最小かで最小間取りを採用
# selected_madori = st.multiselect('間取り', madori)

# 都道府県 ×　市区群 ×　物件種類 ×　間取りの絞込みデータ
madori_filtered_data = bukken_data[(bukken_data['prefecture'] == selected_prefecture) & (bukken_data['city'] == selected_city) & (bukken_data['main_category'].isin(selected_categories)) & (bukken_data['main_madori'].isin(selected_madori))]

# <<< 間取りを選ぶ <<<


# >>> 予算を選ぶ  >>>
st.write('予算')
# 物件データの最低価格（min_price)が未定のものは削除
slider_data = bukken_data.dropna(subset=['min_price']).dropna(subset=['max_price'])
slider_data["min_price"].astype(int)

# 物件データのmin_price（最低価格）からそれぞれ最小値, 最大値を算出し、スライダーバーの値に定義
min_min_price = int(slider_data['min_price'].min())
max_min_price = int(slider_data['min_price'].max())
min_price_slider, max_price_slider = st.slider("予算",min_min_price, max_min_price, (5000, 9000), step=100)  #デフォルトはペルソナを参考に設定
# 予算スライダーで選んだ範囲の価格のデータを抽出
selected_price_data = madori_filtered_data[(madori_filtered_data['min_price'] >= min_price_slider) & (madori_filtered_data['min_price'] <= max_price_slider)]

# 絞込み条件の適用
# <<< 予算を選ぶ <<<


# >>> 建物面積を選ぶ  >>>
st.write('建物面積（延べ面積）')
# 物件データの最小建築面積(min_tatemono_measure)が欠損値のものは削除
tatemono_measure_data = bukken_data.dropna(subset=['min_tatemono_measure']).dropna(subset=['max_tatemono_measure'])
tatemono_measure_data["min_tatemono_measure"].astype(float)
# 物件データの最小面積(min_tatemono_measure)からそれぞれ最小値、最大値を算出し、スライダーバーの値に定義
min_min_tatemono_measure = tatemono_measure_data['min_tatemono_measure'].min()
max_min_tatemono_measure = tatemono_measure_data['min_tatemono_measure'].max()
min_tatemono_measure_slider, max_tatemono_measure_slider = st.slider("建物面積（延べ面積）",min_min_tatemono_measure, max_min_tatemono_measure, (60.0, 120.0), step=10.0)  #デフォルトはペルソナを参考に設定
# 建物面積スライダーで選んだ面積範囲のデータを抽出
selected_measure_data = selected_price_data[(selected_price_data['min_tatemono_measure'] >= min_tatemono_measure_slider) & (selected_price_data['min_tatemono_measure'] <= max_tatemono_measure_slider)]
# <<< 建物面積を選ぶ <<<


# # >>> 築年数を選ぶ  >>>
# # 築年数
st.write('築年数')

# 完成年月日が未来のものは築年数の計算でマイナスになるので、便宜上0に設定
bukken_data.loc[bukken_data['chiku_nensu'] < 0, 'chiku_nensu'] = 0
# 築年数のスライダーを作る
min_chikunensu = int(bukken_data['chiku_nensu'].min())
max_chikunensu = int(bukken_data['chiku_nensu'].max())
min_year_slider, max_year_slider = st.slider("築年数",min_chikunensu, max_chikunensu, (0, 5), step=1) 
# 築年数のスライダーで選んだ範囲を抽出する
selected_year = selected_measure_data[(selected_measure_data['chiku_nensu'] >= min_year_slider) & (selected_measure_data['chiku_nensu'] <= max_year_slider)]
# <<< 築年数を選ぶ <<<




# >>> ベースマップ作成 >>>
# ベースマップの中心を設定
map_center = [35.608730497916845, 139.64832587827124]  # 地図の中心位置の指定(今回は世田谷区玉川地区の玉川総合支所を指定)

# ベースマップを作成
nursery_map = folium.Map(location=map_center, zoom_start=13)
# <<< ベースマップ作成 <<<


# >>> 保育園マップ作成 >>>
# 選択された保育園区分を取得
selected_categories = st.multiselect("希望する保育園区分を選択してください", list(nursery_data["区分"].unique()),default='認可保育園')

# 選択された保育園区分のデータを抽出
filtered_nursery_data = nursery_data[nursery_data["区分"].isin(selected_categories)]

# 保育園区分ごとにマーカーの色を設定
colors = {
    "認可保育園": "blue",
    "認証保育園": "green",
    "認可外保育施設": "red"
}

# 保育園マーカーを設置
for _, row in filtered_nursery_data.iterrows():
    iframe = folium.IFrame('【名称】:' + row['名称']+ '<br>' +'【区分】: ' + row['区分'] + '<br>'  + '【定員】:' + row['定員']+ '人' + '<br>' + '【1歳定員】:'+ str(row['1歳定員'])+ '人'+ '<br>'+'【2歳定員】:' + str(row['2歳定員'])+ '人'+ '<br>'+'【3歳定員】:' + str(row['3歳定員'])+ '人'+ '<br>'+'【4歳定員】:' + str(row['4歳定員'])+ '人'+ '<br>'+'【5歳定員】:' + str(row['5歳定員'])+ '人')
    popup = folium.Popup(iframe, min_width=300, max_width=300)
    folium.Circle(
        location=[row['latitude'], row['longitude']],
        tooltip= row['名称'],
        popup= popup,
        radius= 10,
        fill= True,
        color=colors[row['区分']],
    ).add_to(nursery_map)
# <<< 保育園マップ作成 <<<


# >>> 絞り込んだ物件データをプロット >>>
# 絞り込みされた物件データを更に物件種別毎に分ける（プロットカラーを変える為）
new_mansion_data = selected_measure_data[selected_measure_data["category"].str.contains("新築マンション")]
old_mansion_data = selected_measure_data[selected_measure_data["category"].str.contains("中古マンション")]
new_kodate_data = selected_measure_data[selected_measure_data["category"].str.contains("新築一戸建て")]
old_kodate_data = selected_measure_data[selected_measure_data["category"].str.contains("中古一戸建て")]


#　新築マンションのプロット
new_mansion_group = FeatureGroup(name="新築マンション")

for i, row in new_mansion_data .iterrows():
    folium.Marker(
        location= [row["latitude"], row["longitude"]],
        popup= f"<div style='width:300px'>{row['category']}<br><b>{row['name']}</b><br>{row['adress']}<br>【価格】{row['min_price']}<br>【建物面積】{row['min_tatemono_measure']}<br>【間取り】{row['min_madori']}<br>【最寄路線】{row['nearest_line']}<br>【最寄り駅】{row['nearest_station']}駅<br>【最寄り駅まで】徒歩{row['walk_time']}分<br><a href='{row['url']}' target='_blank'>SUUMOで詳細を確認する</a></div>",
        icon= folium.Icon(icon="home", prefix="fa", icon_color="white", color="pink"),
        tooltip= row['name']
    ).add_to(new_mansion_group)

new_mansion_group.add_to(nursery_map)


#　中古マンションのプロット
old_mansion_group = FeatureGroup(name="中古マンション")

for i, row in old_mansion_data .iterrows():
    folium.Marker(
        location= [row["latitude"], row["longitude"]],
        popup= f"<div style='width:300px'>{row['category']}<br><b>{row['name']}</b><br>{row['adress']}<br>【価格】{row['min_price']}<br>【建物面積】{row['min_tatemono_measure']}<br>【間取り】{row['min_madori']}<br>【最寄路線】{row['nearest_line']}<br>【最寄り駅】{row['nearest_station']}駅<br>【最寄り駅まで】徒歩{row['walk_time']}分<br><a href='{row['url']}' target='_blank'>SUUMOで詳細を確認する</a></div>",
        icon= folium.Icon(icon="home", prefix="fa", icon_color="white", color="orange"),
        tooltip= row['name']
    ).add_to(old_mansion_group)

old_mansion_group.add_to(nursery_map)


#　新築戸建のプロット
new_kodate_group = FeatureGroup(name="新築戸建")

for i, row in new_kodate_data .iterrows():
    folium.Marker(
        location= [row["latitude"], row["longitude"]],
        popup= f"<div style='width:300px'>{row['category']}<br><b>{row['name']}</b><br>{row['adress']}<br>【価格】{row['min_price']}<br>【建物面積】{row['min_tatemono_measure']}<br>【間取り】{row['min_madori']}<br>【最寄路線】{row['nearest_line']}<br>【最寄り駅】{row['nearest_station']}駅<br>【最寄り駅まで】徒歩{row['walk_time']}分<br><a href='{row['url']}' target='_blank'>SUUMOで詳細を確認する</a></div>",
        icon= folium.Icon(icon="home", prefix="fa", icon_color="white", color="purple"),
        tooltip= row['name']
    ).add_to(new_kodate_group)

new_kodate_group.add_to(nursery_map)


#　中古戸建のプロット
old_kodate_group = FeatureGroup(name="新築戸建")

for i, row in old_kodate_data .iterrows():
    folium.Marker(
        location= [row["latitude"], row["longitude"]],
        popup= f"<div style='width:300px'>{row['category']}<br><b>{row['name']}</b><br>{row['adress']}<br>【価格】{row['min_price']}<br>【建物面積】{row['min_tatemono_measure']}<br>【間取り】{row['min_madori']}<br>【最寄路線】{row['nearest_line']}<br>【最寄り駅】{row['nearest_station']}駅<br>【最寄り駅まで】徒歩{row['walk_time']}分<br><a href='{row['url']}' target='_blank'>SUUMOで詳細を確認する</a></div>",
        icon= folium.Icon(icon="home", prefix="fa", icon_color="white", color="lightblue"),
        tooltip= row['name']
    ).add_to(old_kodate_group)

old_kodate_group.add_to(nursery_map)
# <<< 絞り込んだ物件データをプロット <<<


# >>> kohana 追記部分
# sesson_stateにフラグを設定
if "button_on" not in st.session_state:
    st.session_state.button_on =  0

# btn_on = st.button("この条件で物件検索")
# ボタンが押されたらフラグを記憶
if st.button("この条件で物件検索"):
    st.session_state.button_on =  1

if st.session_state.button_on:
    st_folium(nursery_map, width=700, height=700)
# <<<

# # ボタンが押されたらマップ表示
# if st.button('この条件で物件検索'):
#     st_folium(nursery_map, width=700, height=700)

