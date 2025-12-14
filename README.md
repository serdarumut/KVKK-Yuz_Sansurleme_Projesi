# Yüz Tespiti ve Sansürleme Projesi (Face Blurring) 

Görüntü işleme dersi için hazırladığım bu proje, yüklenen fotoğraflardaki kişilerin yüzlerini bulup otomatik olarak gizler. Özellikle sosyal medyada veya veri setlerinde kişisel gizliliği korumak amacıyla geliştirdim.

## Neler Yapıyor?
Eski yöntemler (Haar Cascade gibi) bazen yüzleri kaçırabiliyordu. Bu yüzden projede **Derin Öğrenme (Deep Learning)** kullandım.
* Fotoğrafı yüklediğiniz an yüzleri tarar.
* Yüzü bulursa yeşil bir kutu içine alıp mozaikler.
* Yüz bulamazsa "Yüz tespit edilemedi" diye uyarı verir.
* Sonuç görüntüsünü indirmenize izin verir.

## Nasıl Çalıştırırım?
1.  Bu repoyu indirin (ZIP veya Git clone ile).
2.  `pip install flask opencv-python` komutuyla kütüphaneleri kurun.
3.  `python app.py` diyerek başlatın.
4.  Çıkan linke tıklayın, hepsi bu kadar!

## Kullanılan Teknolojiler
* Python
* OpenCV (DNN Modülü)
* Flask (Web Sunucusu)
* HTML/CSS (Arayüz)
