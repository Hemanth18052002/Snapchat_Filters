import cv2
import mediapipe as mp
import os
import tkinter.filedialog as filedialog
from datetime import datetime as dt

class mesh_set_image:
    
    def apply(self):
        
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_face_mesh = mp.solutions.face_mesh

        di = filedialog.askdirectory()
        imag = []
        
        for i in os.listdir(di):
            imag.append(i)

        with mp_face_mesh.FaceMesh(static_image_mode=True,max_num_faces=5,refine_landmarks=True,
                                min_detection_confidence=0.5) as face_mesh:
            
            tar = os.path.join(os.path.expanduser('~'), 'Downloads')
            now = dt.now()
            s = now.strftime("%d_%m_%Y__%H_%M_%S")
            tar = os.path.join(tar,s)
            os.makedirs(tar)
            
            for ind, pic in enumerate(imag):
                
                image = cv2.imread(os.path.join(di,pic))
                results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

                if not results.multi_face_landmarks:
                    continue
                
                annotated_image = image.copy()
                
                for face_landmarks in results.multi_face_landmarks:
                    # print('face_landmarks:', face_landmarks)
                    mp_drawing.draw_landmarks(image=annotated_image,landmark_list=face_landmarks,
                                                connections=mp_face_mesh.FACEMESH_TESSELATION,
                                                landmark_drawing_spec=None,
                                                connection_drawing_spec=mp_drawing_styles
                                                .get_default_face_mesh_tesselation_style())
                
                
                cv2.imwrite(os.path.join(tar,f"{ind}mesh.jpg"), annotated_image)
                
        print("DONE")

# a = mesh_set_image()
# a.apply()