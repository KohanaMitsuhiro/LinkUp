# LinkUp
linkup_map_perd.py  :最終成果物コード(Streamlit run で起動)
bukken2.csv         :上記で使用する物件情報
hoikuen2.csv        :上記で使用する保育園情報
requirements.txt    :デプロイ用パッケージリスト


フォルダ構成
.streamlit          : streamlitの設定ファイル
Document            : 発表時の資料を格納
Hirose
 +-lat_lon          : 保育園/物件の住所→緯度経度算出
 +-map              : streamlit/foliumを使った地図表示のテスト版
 +-scraping         : マンション情報のスクレイピング
kohana
 +-map              : 保育園のpopにｵﾌｨｽ出発時間を追加したテスト版
 +-nearest_station  : 保育園の緯度経度から最寄駅を算出 
 +-predict          : 2023年の出生数を予測し、2024年の入園率予測
 +-scraping         : 戸建て情報のスクレイピング
