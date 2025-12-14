from flask import Flask, render_template, request, url_for
import cv2
import numpy as np
import os
import time

app = Flask(__name__)

# Ayarlar
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Model Ayarları
MODEL_PATH = "res10_300x300_ssd_iter_140000.caffemodel"
CONFIG_PATH = "deploy.prototxt"

# Modeli yükle
try:
    net = cv2.dnn.readNetFromCaffe(CONFIG_PATH, MODEL_PATH)
    print(" Yapay Zeka Hazır!")
except Exception as e:
    print(" HATA: Model dosyaları eksik!")
    exit()

def profesyonel_mozaik(image, x, y, w, h, mozaik_boyutu=15):
    """ Küçük yüzlerde çökme yapmayan mozaik fonksiyonu """
    roi = image[y:y+h, x:x+w]
    if roi.shape[0] == 0 or roi.shape[1] == 0: return image

    hedef_w = w // mozaik_boyutu
    hedef_h = h // mozaik_boyutu
    if hedef_w < 1: hedef_w = 1
    if hedef_h < 1: hedef_h = 1

    roi_kucuk = cv2.resize(roi, (hedef_w, hedef_h), interpolation=cv2.INTER_LINEAR)
    roi_mozaikli = cv2.resize(roi_kucuk, (w, h), interpolation=cv2.INTER_NEAREST)
    image[y:y+h, x:x+w] = roi_mozaikli
    return image

def yuz_sansurle_kontrol(image_path, save_path):
    img = cv2.imread(image_path)
    if img is None: return False

    (h, w) = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (640, 640)), 1.0,
        (640, 640), (104.0, 177.0, 123.0))

    net.setInput(blob)
    detections = net.forward()

    yuz_bulundu = False # Başlangıçta yüz yok varsayıyoruz

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.25:
            yuz_bulundu = True # Yüz bulduk! Flag'i kaldır.
            
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            face_w = endX - startX
            face_h = endY - startY

            if face_w > 0 and face_h > 0:
                img = profesyonel_mozaik(img, startX, startY, face_w, face_h, mozaik_boyutu=20)
        
    cv2.imwrite(save_path, img)
    return yuz_bulundu # Sonucu geri döndür

@app.route('/', methods=['GET', 'POST'])
def index():
    resim_adi = None
    uyari = None # Yeni uyarı değişkenimiz

    if request.method == 'POST':
        if 'dosya' not in request.files: return 'Dosya yok'
        dosya = request.files['dosya']
        if dosya.filename == '': return 'İsim boş'
        
        if dosya:
            filename = f"islenen_{int(time.time())}.jpg"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            dosya.save(file_path)
            
            # Fonksiyon artık True veya False döndürüyor
            sonuc = yuz_sansurle_kontrol(file_path, file_path)
            
            if sonuc == True:
                resim_adi = filename # Yüz varsa resmi göster
            else:
                uyari = "Fotoğrafta yüz tespit edilememiştir." 
                

    return render_template('index.html', goster_resim=resim_adi, uyari_mesaji=uyari)

if __name__ == '__main__':
    app.run(debug=True)