import streamlit as st

st.set_page_config(
    page_title="🏠 Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Oyuncu Benzerlik Modeli",)
markdown_text = """
    Bu uygulama, **1997-2025** sezonunda seçilen bir oyuncu için NBA istatistiklerine 
    dayanarak en yakın **5 benzer oyuncuyu** tahmin eden bir algoritmadır. Ana sayfada 
    seçilen oyuncunun en benzer beş rakibi listelenirken, **“Player Separation”** sayfasında 
    seçilen oyuncunun ortalama NBA oyuncularına göre en çok ayrıştığı metrikler görselleştirilmektedir.
    
    ---
    
    ## Metrik Açıklamaları

    | Metrik               | Açıklama                                                                                                 |
    | -------------------- | -------------------------------------------------------------------------------------------------------- |
    | **OFF_RATING**       | 100 hücum pozisyonunda takımına kazandırdığı sayı.                                                       |
    | **DEF_RATING**       | 100 savunma pozisyonunda rakibe yedirdiği sayı.                                                          |
    | **NET_RATING**       | `OFF_RATING – DEF_RATING` (net verimlilik farkı).                                                        |
    | **AST_PCT**          | Oyuncunun, takımın hücum pozisyonlarındaki asist yüzdesi.                                                |
    | **AST_TO**           | Asist / Top kaybı oranı.                                                                                  |
    | **AST_RATIO**        | Oyuncunun asist ettiği hücum pozisyonlarının, takım asistlerinin yüzdesi.                                |
    | **OREB_PCT**         | Hücum ribaundlarının, takımın toplam hücum ribaundlarına oranı.                                          |
    | **DREB_PCT**         | Savunma ribaundlarının, takımın toplam savunma ribaundlarına oranı.                                      |
    | **REB_PCT**          | Toplam ribaundlarının (hücum+savunma), takımın toplam ribaundlarına oranı.                               |
    | **TM_TOV_PCT**       | Takımın hücum pozisyonlarında yaptığı top kayıplarının yüzdesi.                                          |
    | **EFG_PCT**          | Etkili şut yüzdesi: `(FGM + 0.5 × 3PM) / FGA`.                                                           |
    | **TS_PCT**           | Gerçek şut yüzdesi: `PTS / (2 × (FGA + 0.44 × FTA))`.                                                     |
    | **USG_PCT**          | Kullanım yüzdesi: Oyuncunun takım hücum potansiyelindeki bireysel şut, asist ve top kaybı payı.         |
    | **PACE**             | Takımın 48 dakikada oynadığı tahmini hücum sayısı (possession).                                          |
    | **PIE**              | Player Impact Estimate – oyuncunun maç üzerindeki genel etki tahmini.                                    |
    | **POSS**             | Oyuncunun tahmini topa sahip olduğu pozisyon sayısı.                                                     |
    | **FG_PCT**           | Saha içi şut yüzdesi: `FGM / FGA`.                                                                       |
    | **season**           | İstatistiğin ait olduğu sezon.                                                                           |
    | **TEAM_ID**          | Takımın benzersiz kimlik numarası.                                                                       |
    | **W**                | Sezondaki galibiyet sayısı.                                                                              |
    | **L**                | Sezondaki mağlubiyet sayısı.                                                                             |
    | **FGM**              | Saha içi isabet sayısı (Field Goals Made).                                                               |
    | **FGA**              | Saha içi deneme sayısı (Field Goals Attempted).                                                          |
    | **FG3M**             | Üç sayılık isabet sayısı (3-Point Field Goals Made).                                                     |
    | **FG3A**             | Üç sayılık deneme sayısı (3-Point Field Goals Attempted).                                                |
    | **FTM**              | Serbest atış isabet sayısı (Free Throws Made).                                                          |
    | **FTA**              | Serbest atış deneme sayısı (Free Throws Attempted).                                                     |
    | **OREB**             | Hücum ribaund toplamı.                                                                                   |
    | **DREB**             | Savunma ribaund toplamı.                                                                                 |
    | **REB**              | Toplam ribaund (hücum + savunma).                                                                        |
    | **AST**              | Asist sayısı.                                                                                             |
    | **TOV**              | Top kaybı sayısı (Turnovers).                                                                            |
    | **STL**              | Top çalma sayısı (Steals).                                                                                |
    | **BLK**              | Blok sayısı (Blocks).                                                                                     |
    | **BLKA**             | Rakip oyuncunun blokladığı şut sayısı (Blocks Against).                                                  |
    | **PF**               | Kişisel faul sayısı (Personal Fouls).                                                                    |
    | **PFD**              | Rakip tarafından yapılan faul sonucu kazanılan serbest atış sayısı (Personal Fouls Drawn).              |
    | **PTS**              | Toplam sayı.                                                                                              |
    | **PCT_PTS_2PT**      | Toplam sayıya göre 2 sayılık basketlerin yüzdesi.                                                        |
    | **PCT_PTS_2PT_MR**   | Toplam sayıya göre orta mesafeden 2 sayılık yüzdesi.                                                     |
    | **PCT_PTS_3PT**      | Toplam sayıya göre 3 sayılık basketlerin yüzdesi.                                                        |
    | **PCT_PTS_FB**       | Toplam sayıya göre hızlı hücumdan gelen sayı yüzdesi.                                                     |
    | **PCT_PTS_OFF_TOV**  | Toplam sayıya göre rakip top kaybı sonrası elde edilen sayı yüzdesi.                                     |
    | **PCT_PTS_PAINT**    | Toplam sayıya göre boyalı alan (paint) sayı yüzdesi.                                                     |
    | **PCT_AST_2PM**      | 2 sayılık isabetlerin içinde asistli yapılanların oranı.                                                 |
    | **PCT_UAST_2PM**     | 2 sayılık isabetlerin içinde asistsiz yapılanların oranı.                                                |
    | **PCT_AST_3PM**      | 3 sayılık isabetlerin içinde asistli yapılanların oranı.                                                 |
    | **PCT_UAST_3PM**     | 3 sayılık isabetlerin içinde asistsiz yapılanların oranı.                                                |
    """

st.markdown(markdown_text)
