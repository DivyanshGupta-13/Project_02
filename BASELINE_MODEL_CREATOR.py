import cv2 as cv
import numpy as np
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

haar_path = os.path.join(base_dir, "HAAR_CASCADE.xml")
if not os.path.exists(haar_path):
    haar_path = os.path.join(base_dir, "Haar_Cascade.xml")

if os.path.exists(haar_path):
    haar = cv.CascadeClassifier(haar_path)
else:
    haar = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

def train(model_no):
    dataset_path = os.path.join(base_dir, 'SAMPLE_DATA', f'MODEL_{model_no}', f'DATASET_{model_no}')
    if not os.path.exists(dataset_path):
        print(f"Dataset path {dataset_path} does not exist, skipping model {model_no}.")
        return

    model = cv.face.LBPHFaceRecognizer.create(radius=1, neighbors=8, grid_x=8, grid_y=8)
    i = -1
    images_list = []
    images_label = []

    for name in os.listdir(dataset_path):
        sub_dir = os.path.join(dataset_path, name)
        if os.path.isdir(sub_dir):
            for img_name in os.listdir(sub_dir):
                img_path = os.path.join(sub_dir, img_name)
                img = cv.imread(img_path)
                if img is not None:
                    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                    gray_eq = cv.equalizeHist(gray)
                    faces = haar.detectMultiScale(gray_eq, scaleFactor=1.1, minNeighbors=3)
                    if len(faces) >= 1:
                        (x, y, w, h) = faces[0]
                        face = gray_eq[y:y+h, x:x+w]
                        face = cv.resize(face, (300, 300), interpolation=cv.INTER_LANCZOS4)
                        images_list.append(face)
                        images_label.append(int(i))
            i -= 1

    if len(images_list) > 0:
        face_arr = np.array(images_list, dtype='uint8')
        label_arr = np.array(images_label, dtype='int32')

        out_dir = os.path.join(base_dir, 'SAMPLE_DATA', f'MODEL_{model_no}')
        os.makedirs(out_dir, exist_ok=True)

        np.save(os.path.join(out_dir, 'FACE_ARRAY.npy'), face_arr)
        np.save(os.path.join(out_dir, 'LABEL_ARRAY.npy'), label_arr)

        model.train(face_arr, label_arr)
        model.save(os.path.join(out_dir, 'BASELINE_MODEL.yml'))
        print(f"MODEL_{model_no} : Baseline training completed successfully with {len(face_arr)} samples.")

if __name__ == "__main__":
    for model_no in [125, 250, 500, 1000]:
        out_dir = os.path.join(base_dir, 'SAMPLE_DATA', f'MODEL_{model_no}')
        for f in ['FACE_ARRAY.npy', 'LABEL_ARRAY.npy', 'BASELINE_MODEL.yml', 'BASELINE_MODEL.npy']:
            p = os.path.join(out_dir, f)
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass
        train(model_no)
