NBA Analitik Panosu

Hakkında

NBA Analitik Panosu, Streamlit ile geliştirilmiş etkileşimli bir web uygulamasıdır. Bu pano sayesinde kullanıcılar NBA oyuncu istatistiklerini görselleştirebilir, farklı metriklere göre karşılaştırma yapabilir ve belirledikleri kriterlere uygun benzer oyuncuları kolayca bulabilir.

Özellikler

Çok Sayfalı Düzen: Genel bakış, oyuncu karşılaştırma ve benzerlik arama sayfaları arasında kolayca gezinme.

Dinamik Özellik Seçimi: Yan çubuktaki multiselect ile geleneksel ve gelişmiş istatistikleri seçin. Seçimler Streamlit oturum durumu (st.session_state) ile korunur.

Renkli Metrikler: Gelişmiş metrikler yeşil, geleneksel metrikler kırmızı renkte vurgulanır ve etkileşimli bir lejant içerir.

En Yakın Oyuncuları Bulma: Bir oyuncu, sezon ve dakika eşiği girerek NearestNeighbors ile istatistiksel olarak benzer oyuncuları listeleyin.

Etkileşimli Görselleştirmeler: Histogramlar, ayrım grafikleri ve yüzde bazlı performans tabloları Matplotlib ile oluşturulur ve st.pyplot ile görüntülenir.
