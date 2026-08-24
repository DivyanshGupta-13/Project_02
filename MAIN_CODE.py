import os
import cv2 as cv
import numpy as np
import csv
from datetime import datetime
from db_helper import get_db_connection

class FaceRecognitionSystem:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_no = 500
        self.res_display = (800, 500)
        self.res_face = (300, 300)
        self.max_count = 100
        self.threshold_value = 75.0  # LBPH distance threshold (lower = better match)
        
        self.model = None
        self.haar_cascade_classifier = None
        
        # Paths
        self.haar_path = os.path.join(self.base_dir, 'HAAR_CASCADE.xml')
        if not os.path.exists(self.haar_path):
            self.haar_path = os.path.join(self.base_dir, 'Haar_Cascade.xml')
            
        self.attendance_dir = os.path.join(self.base_dir, 'Attendence folder')
        os.makedirs(self.attendance_dir, exist_ok=True)
        self.attendance_csv = os.path.join(self.attendance_dir, 'ATTENDANCE.csv')

        self._init_classifier()
        self.create_and_train_model()

    def _init_classifier(self):
        if os.path.exists(self.haar_path):
            self.haar_cascade_classifier = cv.CascadeClassifier(self.haar_path)
        else:
            # Default OpenCV haar cascade fallback
            default_xml = cv.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.haar_cascade_classifier = cv.CascadeClassifier(default_xml)

    def _get_camera(self):
        """Attempts to open available camera index (0, 1, 2)"""
        for idx in [0, 1, 2]:
            cap = cv.VideoCapture(idx)
            if cap is not None and cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None and frame.size > 0:
                    return cap, idx
                cap.release()
        return None, -1

    def create_and_train_model(self):
        """Loads baseline LBPH model and updates with registered student data."""
        self.model = cv.face.LBPHFaceRecognizer.create(radius=1, neighbors=8, grid_x=8, grid_y=8)
        
        # Search for baseline model file
        baseline_file = None
        possible_paths = [
            os.path.join(self.base_dir, 'SAMPLE_DATA', f'MODEL_{self.model_no}', 'BASELINE_MODEL.yml'),
            os.path.join(self.base_dir, 'SAMPLE_DATA', 'MODEL_500', 'BASELINE_MODEL.yml'),
            os.path.join(self.base_dir, 'SAMPLE_DATA', 'MODEL_250', 'BASELINE_MODEL.yml'),
            os.path.join(self.base_dir, 'SAMPLE_DATA', 'MODEL_125', 'BASELINE_MODEL.yml'),
            os.path.join(self.base_dir, 'BASELINE_MODEL.yml')
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                baseline_file = path
                break
                
        if baseline_file:
            try:
                self.model.read(baseline_file)
            except Exception as e:
                print(f"Warning: Could not read baseline model file {baseline_file}: {e}")
                
        # Update with actual user data in ACTUAL_DATA
        actual_dir = os.path.join(self.base_dir, 'ACTUAL_DATA')
        if os.path.exists(actual_dir):
            for user in os.listdir(actual_dir):
                user_path = os.path.join(actual_dir, user)
                if os.path.isdir(user_path):
                    face_npy = os.path.join(user_path, 'FACE_ARRAY.npy')
                    label_npy = os.path.join(user_path, 'LABEL_ARRAY.npy')
                    if os.path.exists(face_npy) and os.path.exists(label_npy):
                        try:
                            arr1 = np.load(face_npy)
                            arr2 = np.load(label_npy)
                            if len(arr1) > 0 and len(arr2) > 0:
                                self.model.update(arr1, arr2)
                        except Exception as e:
                            print(f"Warning: Could not update model for user {user}: {e}")

    def preprocess_face(self, face_bgr):
        """Converts BGR face ROI to 300x300 grayscale with histogram equalization."""
        if face_bgr is None or face_bgr.size == 0:
            return None
        if len(face_bgr.shape) == 3:
            gray = cv.cvtColor(face_bgr, cv.COLOR_BGR2GRAY)
        else:
            gray = face_bgr
        gray_eq = cv.equalizeHist(gray)
        resized = cv.resize(gray_eq, self.res_face, interpolation=cv.INTER_LANCZOS4)
        return resized

    def register(self, user_id):
        """Captures face samples from webcam and trains model for student user_id."""
        user_dir = os.path.join(self.base_dir, 'ACTUAL_DATA', str(user_id))
        img_dir = os.path.join(user_dir, 'IMAGES')
        os.makedirs(img_dir, exist_ok=True)

        cap, cam_idx = self._get_camera()
        if cap is None:
            raise RuntimeError("Camera Error: No working webcam detected!")

        face_list = []
        label_list = []
        count = 1

        win_name = "REGISTRATION - Capturing Samples (Press 'Q' to cancel)"
        cv.namedWindow(win_name, cv.WINDOW_NORMAL)

        try:
            while count <= self.max_count:
                ret, frame = cap.read()
                if not ret or frame is None:
                    break

                frame = cv.flip(frame, 1)
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                gray_eq = cv.equalizeHist(gray)

                faces = self.haar_cascade_classifier.detectMultiScale(
                    gray_eq, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
                )

                display_frame = frame.copy()

                if len(faces) == 1:
                    (x, y, w, h) = faces[0]
                    face_roi = frame[y:y+h, x:x+w]
                    processed_face = self.preprocess_face(face_roi)

                    if processed_face is not None:
                        img_path = os.path.join(img_dir, f"{count}.jpg")
                        cv.imwrite(img_path, processed_face, [cv.IMWRITE_JPEG_QUALITY, 100])
                        face_list.append(processed_face)
                        label_list.append(int(user_id))

                        cv.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv.putText(display_frame, f"Sample: {count}/{self.max_count}",
                                   (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        count += 1
                elif len(faces) > 1:
                    cv.putText(display_frame, "Multiple faces detected! Show only 1 face",
                               (20, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    cv.putText(display_frame, "Position face in camera view",
                               (20, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                cv.imshow(win_name, display_frame)
                key = cv.waitKey(30) & 0xFF
                if key == ord('q') or key == 27:
                    break
                if cv.getWindowProperty(win_name, cv.WND_PROP_VISIBLE) < 1:
                    break
        finally:
            cap.release()
            cv.destroyAllWindows()

        if len(face_list) > 0:
            face_arr = np.array(face_list, dtype='uint8')
            label_arr = np.array(label_list, dtype='int32')
            np.save(os.path.join(user_dir, 'FACE_ARRAY.npy'), face_arr)
            np.save(os.path.join(user_dir, 'LABEL_ARRAY.npy'), label_arr)
            self.model.update(face_arr, label_arr)
            return len(face_list)
        else:
            raise RuntimeError("Registration cancelled or no valid face samples captured.")

    def delete_user(self, user_id):
        """Removes student face data and retrains the model."""
        import shutil
        user_dir = os.path.join(self.base_dir, 'ACTUAL_DATA', str(user_id))
        if os.path.exists(user_dir):
            shutil.rmtree(user_dir, ignore_errors=True)
        self.create_and_train_model()

    def update_user(self, user_id):
        self.delete_user(user_id)
        return self.register(user_id)

    def attendance(self):
        """Runs real-time face recognition camera loop and marks attendance."""
        cap, cam_idx = self._get_camera()
        if cap is None:
            raise RuntimeError("Camera Error: No working webcam detected!")

        win_name = "ATTENDANCE - Press 'Q' or 'A' or ESC to Exit"
        cv.namedWindow(win_name, cv.WINDOW_NORMAL)

        db = get_db_connection()

        try:
            while True:
                ret, frame = cap.read()
                if not ret or frame is None:
                    break

                frame = cv.flip(frame, 1)
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                gray_eq = cv.equalizeHist(gray)

                faces = self.haar_cascade_classifier.detectMultiScale(
                    gray_eq, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
                )

                for (x, y, w, h) in faces:
                    face_roi = frame[y:y+h, x:x+w]
                    processed_face = self.preprocess_face(face_roi)

                    if processed_face is not None:
                        label, confidence = self.model.predict(processed_face)

                        # Check if match is confident and label is a valid positive student ID
                        if confidence < self.threshold_value and label > 0:
                            try:
                                cursor = db.cursor()
                                cursor.execute("SELECT studentName, dep FROM student WHERE studentId=%s", (str(label),))
                                row = cursor.fetchone()
                                cursor.close()
                                if row and row[0]:
                                    std_name, dep = str(row[0]), str(row[1]) if row[1] else "N/A"
                                else:
                                    std_name, dep = f"ID: {label}", "Student"
                            except Exception:
                                std_name, dep = f"ID: {label}", "Student"

                            display_txt = f"{std_name} ({dep})"
                            color = (0, 255, 0) # Green for match
                            self.attendancecsv(label, std_name, dep)
                        else:
                            display_txt = "UNKNOWN"
                            color = (0, 0, 255) # Red for unknown

                        cv.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                        cv.rectangle(frame, (x, y-30), (x+w, y), color, cv.FILLED)
                        cv.putText(frame, display_txt, (x+5, y-8),
                                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                cv.imshow(win_name, frame)
                key = cv.waitKey(10) & 0xFF
                if key == ord('q') or key == ord('a') or key == 27:
                    break
                if cv.getWindowProperty(win_name, cv.WND_PROP_VISIBLE) < 1:
                    break
        finally:
            db.close()
            cap.release()
            cv.destroyAllWindows()

    def attendancecsv(self, std, result, dep):
        """Records student attendance to CSV for today's date if not already recorded."""
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%H:%M:%S")

        # Create file with headers if missing
        if not os.path.exists(self.attendance_csv) or os.path.getsize(self.attendance_csv) == 0:
            with open(self.attendance_csv, "w", newline="", encoding="utf-8") as f:
                f.write("Roll,Name,Department,Time,Date,Status\n")

        # Read existing records to avoid duplicate entry on SAME DAY
        already_marked = False
        with open(self.attendance_csv, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 5:
                    rec_roll = row[0].strip()
                    rec_date = row[4].strip()
                    if rec_roll == str(std).strip() and rec_date == date_str:
                        already_marked = True
                        break

        if not already_marked:
            with open(self.attendance_csv, "a", newline="", encoding="utf-8") as f:
                f.write(f"{str(std).strip()},{result.strip()},{dep.strip()},{time_str},{date_str},Present\n")

if __name__ == "__main__":
    fr = FaceRecognitionSystem()
    print("FaceRecognitionSystem initialized successfully!")
