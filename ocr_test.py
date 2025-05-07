import cv2
import easyocr

# EasyOCR okuyucuyu tanımla
reader = easyocr.Reader(['en']) 

# Kamera başlat
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

print("📷 Kamera açık. 's' ile fotoğraf çek ve OCR yap, 'q' ile çık.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Kamera OCR", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        # Görüntüyü OCR için
        result = reader.readtext(frame)
        print("\n📄 Algılanan Metin:")
        for detection in result:
            print("-", detection[1])  

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
