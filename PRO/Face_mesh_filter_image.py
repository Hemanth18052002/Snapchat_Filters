import cv2
import mediapipe as mp
import os
import tkinter.filedialog as filedialog

class mesh_image:
    
    def apply(self):
        
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_face_mesh = mp.solutions.face_mesh

        file = filedialog.askopenfilename(title='Select Image', filetypes=[('Image Files', '*.jpg *.png *.jpeg')])

        with mp_face_mesh.FaceMesh(static_image_mode=True,max_num_faces=5,refine_landmarks=True,
                                min_detection_confidence=0.5) as face_mesh:
                
            image = cv2.imread(file)
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            if results.multi_face_landmarks:
                annotated_image = image.copy()
                
                for face_landmarks in results.multi_face_landmarks:
                    
                    mp_drawing.draw_landmarks(image=annotated_image,landmark_list=face_landmarks,
                                                connections=mp_face_mesh.FACEMESH_TESSELATION,
                                                landmark_drawing_spec=None,
                                                connection_drawing_spec=mp_drawing_styles
                                                    .get_default_face_mesh_tesselation_style())
                    
                download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
                file_name, file_ext = os.path.splitext(os.path.basename(file))
                download_path = os.path.join(download_folder, file_name + "posa" +file_ext)
                cv2.imwrite(download_path, annotated_image)
                print(f'Successfully downloaded image to {download_path}')
                    
            else:
                print("no Face")
                
        print("DONE")
    
# a = mesh_image()
# a.apply()