import streamlit as st                                    # streamlit
from streamlit_folium import st_folium                    # streamlitでfoliumを使う
import folium                                             # folium
# from folium import FeatureGroup                           # FeatureGrop
import pandas as pd                                       # CSVをデータフレームとして読み込む
import datetime
import requests
from bs4 import BeautifulSoup

# 検索日の設定
def sarch_YMD():
    # 現在の日付を取得
    today = datetime.date.today()

    # 次の週の月曜日を取得(検索する日を月曜日に固定)
    next_monday = today + datetime.timedelta(days=(7-today.weekday()))

    # 2023年の日本の祝日のリストを作成
    holidays = {
        datetime.date(2023, 1, 1): "元日",
        datetime.date(2023, 1, 9): "成人の日",
        datetime.date(2023, 2, 11): "建国記念日",
        datetime.date(2023, 2, 23): "天皇誕生日",
        datetime.date(2023, 3, 21): "春分の日",
        datetime.date(2023, 4, 29): "昭和の日",
        datetime.date(2023, 5, 3): "憲法記念日",
        datetime.date(2023, 5, 4): "みどりの日",
        datetime.date(2023, 5, 5): "こどもの日",
        datetime.date(2023, 7, 17): "海の日",
        datetime.date(2023, 8, 11): "山の日",
        datetime.date(2023, 9, 18): "敬老の日",
        datetime.date(2023, 9, 23): "秋分の日",
        datetime.date(2023, 10, 9): "体育の日",
        datetime.date(2023, 11, 3): "文化の日",
        datetime.date(2023, 11, 23): "勤労感謝の日",
        datetime.date(2023, 12, 23): "天皇誕生日",
    }

    # 次の月曜日が日本の祝日の場合は、次の平日を計算
    if next_monday in holidays:
        next_monday = next_monday + datetime.timedelta(days=1)

    # 日付の抽出
    sarch_year = f'{next_monday.year:04}'
    sarch_month = f'{next_monday.month:02}'
    sarch_day = f'{next_monday.day:02}'

    return sarch_year,sarch_month,sarch_day

# 検索に時間が掛かるので、キャッシュに溜めておく。
@st.cache
def sarch_DepartureTime(route_url):
    #Requestsを利用してWebページを取得する
    route_response = requests.get(route_url)
    # BeautifulSoupを利用してWebページを解析する
    route_soup = BeautifulSoup(route_response.text, 'html.parser')
    # 経路の詳細を取得(1つ目を指定する)
    route_detail = route_soup.find("div",class_ = "routeDetail")
    # 出発発射時間の取得(詳細情報の1つ目の時間を取得) 
    staion_departure_time = route_detail.find("ul",class_ = "time").get_text()
    # 駅の出発時間を時刻に変換
    staion_departure_time = datetime.datetime.strptime(staion_departure_time, '%H:%M')
    # 徒歩時間を引いて、オフィスの出発時間に変換
    office_departure_time = staion_departure_time - datetime.timedelta(minutes=office_walk_Time)
    # 時間部分だけテキスト化
    office_departure_time = office_departure_time.time().strftime("%H:%M")

    return office_departure_time

# 表示するデータを読み込み
df = pd.read_csv("hoikuen.csv")

# DataFrameをst.session_stateに保存する
if "new_df" not in st.session_state:
    st.session_state.new_df = df

# 区分の列にあるすべての区分をリスト化する
type_list= list(df['区分'].unique())

st.header("出発時間")
office_station = st.text_input("事務所の最寄り駅を入力下さい 　例 ） 東京")
office_walk_Time = st.number_input("自分の席から最寄り駅改札までの時間を入力下さい", 0,59,1)

# 検索日の設定
sarch_year,sarch_month,sarch_day = sarch_YMD()

if st.button("検索") and office_station:
    with st.spinner("オフィスの出発時間を検索中..."):
        # 出発時間の検索
        for i, row in df.iterrows():
            # 閉所時間を時刻化
            hoikuen_end = pd.to_datetime(row["閉所時間"])

            # 閉所10分前に保育園到着換算
            arrival_time = hoikuen_end - datetime.timedelta(minutes=10) - datetime.timedelta(minutes=(int(row["walk_time"])))

            sarch_hour = f'{arrival_time.hour:02}'
            sarch_minute = arrival_time.minute
            sarch_m1 = str(sarch_minute // 10)
            sarch_m2 = str(sarch_minute % 10)

            # yahoo路線図
            route_url = f"https://transit.yahoo.co.jp/search/result?from={office_station}&to={row['nearlest_station']}&fromgid=&togid=&flatlon=&tlatlon=&via=&viacode=&y={sarch_year}&m={sarch_month}&d={sarch_day}&hh={sarch_hour}&m1={sarch_m1}&m2={sarch_m2}&type=4&ticket=ic&expkind=1&userpass=1&ws=3&s=0"

            office_departure_time = sarch_DepartureTime(route_url)
            
            df.loc[i,"office_departure_time"] = office_departure_time
            df.loc[i,"route_url"] = route_url

            st.session_state.new_df = df

        st.success("完了しました！")

else:
    st.write("条件を入力して下さい")

# カラム名をみて、出発時間の列が追加されている場合のみ地図を表示させる
column_name = st.session_state.new_df.columns.tolist()
if "office_departure_time" in column_name:
    st.markdown("#### 保育園を指定します")

    # マルチセレクトの作成
    selections= st.multiselect("ご希望の保育園区分をお選びください", type_list, default='認可保育園')

    # セレクトされた区分でデータフレームの中身をフィルタリングする
    df2 = st.session_state.new_df[(st.session_state.new_df['区分'].isin(selections))]


    # ベースの地図作成
    hoiku_map = folium.Map(
        # 地図の中心位置の指定(今回は世田谷区玉川地区の玉川総合支所を指定)
        location=[35.608730497916845, 139.64832587827124],
        # タイル（デフォルトはOpenStreetMap)、アトリビュート(attr:右下の出典情報はデフォルト指定時は不要)指定
        tiles="OpenStreetMap",
        # ズームを指定
        zoom_start=13
    )


    # 保育園の区分（マルチセレクト）とプロットを連動させる
    for i, row in df2.iterrows():
        iframe = folium.IFrame( '・区分: ' + row.loc['区分'] + '<br>' +
                            '・名称:' + row.loc['名称']+ '<br>' +
                            '・定員:' + str(row.loc['定員'])+ '<br>' + 
                            '・1歳定員:' + str(row.loc['1歳定員']) + '<br>' +
                            '・オフィス出発時間: ' + row.loc['office_departure_time'] + '<br>' +
                            '<a href ="'+ row.loc['route_url'] + '#route01" target="_blank">ルート詳細はこちら</a>'
                                )
        popup = folium.Popup(iframe, min_width=300, max_width=300)
        folium.Circle(
            location= [row["latitude"], row["longitude"]],
            tooltip= row["名称"],
            popup= popup,
            radius= 10,
            fill= True,
            color= 'red'
        ).add_to(hoiku_map)

    st_folium(hoiku_map, width=700, height=700)
