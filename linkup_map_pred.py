import folium
import streamlit as st 
from streamlit_folium import st_folium 
from folium import FeatureGroup  
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime

# ページ設定
st.set_page_config(
    page_title="子育て共働き家族のための物件探し",
    page_icon="🏠",
    # layout="wide",
    # initial_sidebar_state="expanded",
)

# データの読み込み
nursery_data = pd.read_csv("hoikuen2.csv")
bukken_data = pd.read_csv("bukken2.csv")

# >>> Streamlit タイトル >>>
st.header("子育て共働き家族のための物件探し")
st.text("""
        認可保育園の入りやすさを示す「新規入園率」からエリアを絞ったり、
        間取りや価格だけでなく、周辺の保育園情報も確認しながら物件を探すことができます。
        """)
# <<< Streamlit タイトル <<<

# >>> 検索条件設定 >>>
st.write("#### 物件の条件設定")
# >>> エリアを選ぶ >>>
areas = bukken_data['area'].unique().tolist()
st.write('不動産購入をエリアから探す<font color="red">*</font>', unsafe_allow_html=True)
selected_area = st.selectbox('不動産購入をエリアから探す*', areas, label_visibility="collapsed")
# <<< エリアを選ぶ <<<


# >>> 都道府県を選ぶ  >>>
prefectures = bukken_data[bukken_data['area'] == selected_area]['prefecture'].unique().tolist()
st.write('不動産購入を都道府県から探す<font color="red">*</font>', unsafe_allow_html=True)
selected_prefecture = st.selectbox ('不動産購入を都道府県から探す*', prefectures, label_visibility="collapsed")
# <<< 都道府県を選ぶ <<<


# >>> 市区群を選ぶ  >>>
# 選択された都道府県に該当する市区群名のリストを作成
cities = bukken_data[bukken_data['prefecture']==selected_prefecture]['city'].unique().tolist()
st.write('入園決定率を参考に市区群から探す<font color="red">*</font>', unsafe_allow_html=True)
# st.caption('入園決定率とは、2022年時点での保育園の入りやすさの目安です。既存児童の継続利用を除いた新規申込者のうち、実際に何人入園できたかを示します。')
st.caption('入園決定率とは保育園の入りやすさの目安です。既存児童の継続利用を除いた新規申込者のうち、実際に何人入園できたかを示します。記載の数値は2023年の出生数を予測し、2024年度の入園率を予測したものです。')
selected_city = st.selectbox ('入園決定率を参考に市区群から探す',cities, label_visibility="collapsed")


# >>> 物件種類を選ぶ  >>>
if selected_city != "選択してください":
    def select_categories():
        st.write('物件種類（複数選択可）') 
        selected_categories = []
        if st.checkbox('新築マンション'):
            selected_categories.append("新築マンション")
        if st.checkbox('中古マンション'):
            selected_categories.append("中古マンション")
        if st.checkbox('新築一戸建て'):
            selected_categories.append("新築一戸建て")
        if st.checkbox('中古一戸建て'):
            selected_categories.append("中古一戸建て")
        return selected_categories
    selected_categories = select_categories()
# <<< 物件種類を選ぶ <<<


    # >>> 間取りを選ぶ  >>>
    def select_madori():
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
        return selected_madori
    selected_madori = select_madori()
    # <<< 間取りを選ぶ <<<


    # エリア × 都道府県 × 市区群 × 物件種類 × 間取りの絞り込みデータを取得
    filtered_data = bukken_data[(bukken_data['area'] == selected_area) & (bukken_data['prefecture'] == selected_prefecture) & (bukken_data['city'] == selected_city)]
    # 物件種類と間取りのリストが存在するときのみfiltered_dataに条件を含める（物件種類と間取りを任意項目に）
    if len(selected_categories) > 0:
        filtered_data = filtered_data[filtered_data['main_category'].isin(selected_categories)]
    if len(selected_madori) > 0:
        filtered_data = filtered_data[filtered_data['main_madori'].isin(selected_madori)]
    

    # >>> 予算を選ぶ  >>>
    # 物件データの最低価格（min_price)が未定のものは削除
    slider_data = bukken_data.dropna(subset=['min_price']).dropna(subset=['max_price'])
    slider_data["min_price"].astype(int)

    # 物件データのmin_price（最低価格）からそれぞれ最小値, 最大値を算出し、スライダーバーの値に定義
    min_min_price = int(slider_data['min_price'].min())
    max_min_price = int(slider_data['min_price'].max())
    st.write("予算")
    min_price_slider, max_price_slider = st.slider("予算",min_min_price, 40000, (5000, 9000), step=100, label_visibility="collapsed" )  #最大値、デフォルトはペルソナを参考に設定
    # 予算スライダーで選んだ範囲の価格のデータを抽出
    selected_price_data = filtered_data[(filtered_data['min_price'] >= min_price_slider) & (filtered_data['min_price'] <= max_price_slider)]
    # <<< 予算を選ぶ <<<


    # >>> 建物面積を選ぶ  >>>
    # 物件データの最小建築面積(min_tatemono_measure)が欠損値のものは削除
    tatemono_measure_data = bukken_data.dropna(subset=['min_tatemono_measure']).dropna(subset=['max_tatemono_measure'])
    tatemono_measure_data["min_tatemono_measure"].astype(float)
    # 物件データの最小面積(min_tatemono_measure)からそれぞれ最小値、最大値を算出し、スライダーバーの値に定義
    min_min_tatemono_measure = tatemono_measure_data['min_tatemono_measure'].min()
    max_min_tatemono_measure = tatemono_measure_data['min_tatemono_measure'].max()
    st.write("建物面積（延べ面積）")
    min_tatemono_measure_slider, max_tatemono_measure_slider = st.slider("建物面積（延べ面積）",min_min_tatemono_measure, 400.0, (60.0, 120.0), step=10.0, label_visibility="collapsed")  #最大値、デフォルトはペルソナを参考に設定
    # 建物面積スライダーで選んだ面積範囲のデータを抽出
    selected_measure_data = selected_price_data[(selected_price_data['min_tatemono_measure'] >= min_tatemono_measure_slider) & (selected_price_data['min_tatemono_measure'] <= max_tatemono_measure_slider)]
    # <<< 建物面積を選ぶ <<<


    # # >>> 築年数を選ぶ  >>>
    # 完成年月日が未来のものは築年数の計算でマイナスになるので、便宜上0に設定
    bukken_data.loc[bukken_data['chiku_nensu'] < 0, 'chiku_nensu'] = 0
    # 築年数のスライダーを作る
    min_chikunensu = int(bukken_data['chiku_nensu'].min())
    max_chikunensu = int(bukken_data['chiku_nensu'].max())
    st.write("築年数")
    min_year_slider, max_year_slider = st.slider("築年数",min_chikunensu, max_chikunensu, (0, 5), step=1, label_visibility="collapsed") 
    # 築年数のスライダーで選んだ範囲を抽出する
    selected_year = selected_measure_data[(selected_measure_data['chiku_nensu'] >= min_year_slider) & (selected_measure_data['chiku_nensu'] <= max_year_slider)]
    # <<< 築年数を選ぶ <<<


    # >>> 徒歩分  >>>
    # セレクトボックス
    st.write('最寄り駅から物件までの徒歩分')
    walk_time = st.selectbox ('最寄り駅から物件までの徒歩分', ( 'お選びください', '指定なし', '1分以内', '3分以内', '5分以内', '7分以内', '10分以内', '15分以内', '20分以内'), label_visibility="collapsed" )
    # セレクトボックスで選んだ徒歩分以下のものを抽出
    def filter_walk_time(selected_year, walk_time):
        if walk_time == '指定なし':
            filtered_walk_time = selected_year
        elif walk_time == '1分以内':
            filtered_walk_time = selected_year[selected_year['walk_time'] <= 1]
        elif walk_time == '3分以内':
            filtered_walk_time = selected_year[selected_year['walk_time'] <= 3]
        elif walk_time == '5分以内':
            filtered_walk_time = selected_year[selected_year['walk_time'] <= 5]
        elif walk_time == '7分以内':
            filtered_walk_time = selected_year[selected_year['walk_time'] <= 7]
        elif walk_time == '10分以内':
            filtered_walk_time = selected_year[selected_year['walk_time'] <= 10]
        elif walk_time == '15分以内':
            filtered_walk_time = selected_year[selected_year['walk_time'] <= 15]
        elif walk_time == '20分以内':
            filtered_walk_time = selected_year[selected_year['walk_time'] <= 20]
        elif walk_time == 'お選びください':
            filtered_walk_time = selected_year
        return filtered_walk_time
    
    filtered_walk_time = filter_walk_time(selected_year, walk_time)


    # >>> nursery_dataの調整 >>>
    # 各年齢の定員及び受入年齢、対象年齢の列に欠損値がある⇒欠損値処理（-を入れる）※Popupでnanの際は"-"を表示せせるため
    nursery_data = nursery_data.fillna({"定員":"-", "0歳定員":"-", "1歳定員":"-", "2歳定員":"-", "3歳定員":"-","4歳定員":"-","5歳定員":"-","受入年齢":"-", "対象年齢":"-", "延長保育時間（開始）":"-", "延長保育時間（終了）":"-"})
    # 各定員の列にて、try関数を使用し数値だったらint化、欠損値(-)だったら-を表示させる
    def convert_to_int(x):
        try:
            return int(x)
        except:
            return x

    for col in ["定員", "0歳定員", "1歳定員", "2歳定員", "3歳定員", "4歳定員", "5歳定員","受入年齢", "対象年齢", "延長保育時間（開始）", "延長保育時間（終了）"]:
        nursery_data[col] = nursery_data[col].apply(convert_to_int)
        nursery_data[col] = nursery_data[col].replace({None: '-'})
    # <<< nursery_dataの調整 <<<

    # nursery_dataの都道府県 ×　市区群 の絞込みデータ
    nursery_area_data = nursery_data[(nursery_data['都道府県'] == selected_prefecture) & (nursery_data['市区群'] == selected_city)]

# >>> 送迎出発時間設定 >>>
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
    @st.cache_data
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

    # DataFrameをst.session_stateに保存する
    if "new_nursery_area_data" not in st.session_state:
        st.session_state.new_nursery_area_data = nursery_area_data

    # 区分の列にあるすべての区分をリスト化する
    type_list= list(nursery_area_data['区分'].unique())

    #余白
    st.write("\n")
    st.write("\n")
    # >>> 送迎出発時間設定 >>>
    if walk_time != 'お選びください':
        st.write("#### お迎え時間の設定")
        st.caption('オフィス最寄り駅と、オフィス⇔最寄り駅の所用時間を入力することで、保育園の開所時間内に間に合うお迎え出発時間を検索できます。')
        office_station = st.text_input("オフィスの最寄り駅を入力下さい 　例 ） 東京")
        office_walk_Time = st.number_input("自分の席から最寄り駅改札までの時間を入力下さい（分）", 0,59,1)

        # 検索日の設定
        sarch_year,sarch_month,sarch_day = sarch_YMD()

        # <<< 送迎出発時間設定 <<<

        # >>> ベースマップ作成 >>>
        # ベースマップの中心を設定
        map_center = [35.608730497916845, 139.64832587827124]  # 地図の中心位置の指定(今回は世田谷区玉川地区の玉川総合支所を指定)
        # ベースマップを作成
        nursery_map = folium.Map(location=map_center, zoom_start=13)
        # <<< ベースマップ作成 <<<


        # 選択された保育園区分を取得
        selected_categories = st.multiselect("希望する保育園の種類を選択してください", ('認可保育園', '認証保育園', '認可外保育施設'),default='認可保育園')

        # >>> 絞り込んだ物件データをプロット >>>
        # 物件プロットの色を指定
        plot_colors = {"new_mansion":"pink","old_mansion":"orange","new_kodate":"purple","old_kodate":"lightblue"}
        plot_icons = {"mansion":"building","kodate":"home"}

        # 物件プロットを作成する関数
        @st.cache_data
        def folium_plot(data,_group,color,icon):
            for i, row in data.iterrows():
                folium.Marker(
                    location= [row["latitude"], row["longitude"]],
                    popup= f"<div style='width:300px'>{row['category']}<br><b> {row['name']}</b><br>{row['adress']}<br>\
                        【価格】{row['min_price']}円<br>【建物面積】{row['min_tatemono_measure']}㎡<br>【間取り】{row['min_madori']}<br>\
                        【最寄路線】{row['nearest_line']}<br>【最寄り駅】{row['nearest_station']}駅<br>【最寄り駅まで】徒歩{int(row['walk_time'])}分<br>\
                        <a href='{row['url']}' target='_blank'>SUUMOで詳細を確認する</a></div>",
                    icon= folium.Icon(icon=icon, prefix="fa", icon_color="white", color=color),
                    tooltip= row['name']
                ).add_to(_group)

            return _group


        # 絞り込みされた物件データを更に物件種別毎に分ける（プロットカラーを変える為）
        new_mansion_data = filtered_walk_time[filtered_walk_time["category"].str.contains("新築マンション")]
        old_mansion_data = filtered_walk_time[filtered_walk_time["category"].str.contains("中古マンション")]
        new_kodate_data = filtered_walk_time[filtered_walk_time["category"].str.contains("新築一戸建て")]
        old_kodate_data = filtered_walk_time[filtered_walk_time["category"].str.contains("中古一戸建て")]

        #　新築マンションのプロット
        new_mansion_group = FeatureGroup(name="新築マンション")
        folium_plot(new_mansion_data,new_mansion_group,plot_colors["new_mansion"],plot_icons["mansion"]).add_to(nursery_map)

        #　中古マンションのプロット
        old_mansion_group = FeatureGroup(name="中古マンション")
        folium_plot(old_mansion_data,old_mansion_group,plot_colors["old_mansion"],plot_icons["mansion"]).add_to(nursery_map)

        #　新築戸建のプロット
        new_kodate_group = FeatureGroup(name="新築戸建")
        folium_plot(new_kodate_data,new_kodate_group,plot_colors["new_kodate"],plot_icons["kodate"]).add_to(nursery_map)

        #　中古戸建のプロット
        old_kodate_group = FeatureGroup(name="中古戸建")
        folium_plot(old_kodate_data,old_kodate_group,plot_colors["old_kodate"],plot_icons["kodate"]).add_to(nursery_map)


        # <<< 絞り込んだ物件データをプロット <<<

        #ボタン周りの余白
        st.write("\n")
        st.write("\n")


        # >>> ボタンのcss設定 >>>
        button_css = f"""
        <style>
        div.stButton > button:first-child  {{
        background   : #1BA37B  ;
        border       : 1px solid ;
        color        : #FFFFFF ;
        }}
        </style>
        """
        st.markdown(button_css, unsafe_allow_html=True)
        # <<< ボタンのcss設定 <<<

        # >>> kohana 追記部分
        # sesson_stateにフラグを設定
        if "button_on" not in st.session_state:
            st.session_state.button_on =  0

        # ボタンが押されたらフラグを記憶
        if st.columns(3)[1].button("この条件で物件検索"):
            st.session_state.button_on =  1
        # session_stateの
        if st.session_state.button_on:

            # 選択された保育園区分のデータを抽出
            # filtered_nursery_data = nursery_data[nursery_data["区分"].isin(selected_categories)]
            filtered_nursery_area_data = st.session_state.new_nursery_area_data[st.session_state.new_nursery_area_data["区分"].isin(selected_categories)]

            # >>> オフィス出発時間の算出
            with st.spinner("オフィスの出発時間を検索中..."):
                # 出発時間の検索
                for i, row in filtered_nursery_area_data.iterrows():
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
                    
                    filtered_nursery_area_data.loc[i,"office_departure_time"] = office_departure_time
                    # filtered_nursery_area_data.loc[i,"office_departure_time"] = "-"
                    filtered_nursery_area_data.loc[i,"route_url"] = route_url

            # <<< オフィス出発時間の算出


            # >>> 保育園マップ作成 >>>
            # 保育園区分ごとにマーカーの色を設定
            colors = {
                "認可保育園": "blue",
                "認証保育園": "green",
                "認可外保育施設": "red"
            }
            # 保育園マーカーを設置
            for _, row in filtered_nursery_area_data.iterrows():    
                folium.Circle(
                    location=[row['latitude'], row['longitude']],
                    tooltip= row['名称'],
                    popup= f"<div style='width:300px'>{row['区分']}<br><b>\
                        {row['名称']}</b><br>\
                        {row['住所']}<br>\
                        【定員】{row['定員']}人<br>\
                        【0歳児定員】{(row['0歳定員'])}人<br>\
                        【1歳児定員】{row['1歳定員']}人<br>\
                        【2歳児定員】{(row['2歳定員'])}人<br>\
                        【3歳児定員】{(row['3歳定員'])}人<br>\
                        【4歳児定員】{(row['4歳定員'])}人<br>\
                        【5歳児定員】{(row['5歳定員'])}人<br>\
                        【受入年齢】】{(row['受入年齢'])}～<br>\
                        【対象年齢】】{(row['対象年齢'])}～<br>\
                        【開所時間】{(row['開所時間'])}～{(row['閉所時間'])}<br>\
                        【延長保育時間】{(row['延長保育時間（開始）'])}～{(row['延長保育時間（終了）'])}<br>\
                        【オフィス出発時間】{(row['office_departure_time'])}<br>\
                            <a href ={row.loc['route_url']}#route01 target='_blank'>ルート詳細はこちら</a></div>",
                    radius= 10,
                    fill= True,
                    color=colors[row['区分']]
                ).add_to(nursery_map)
            # <<< 保育園マップ作成 <<<

            st_folium(nursery_map, width=700, height=700)

            # >>> Streamlit フッター >>>
            st.write("""
                    <font color="gray">出典：保育園情報は「100都市保育力充実度チェック　2022」及び、各自治体HPより。<br>
                    物件情報及は2023年3月時点のものです。物件情報は変動する可能性がありますので、ご理解の上でお使いください。</font>
                    """, unsafe_allow_html=True)
            # <<< Streamlit フッター <<<
