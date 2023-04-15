import cv2
import mediapipe as mp


class mesh_cam:
    
    def apply(self):
        
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_face_mesh = mp.solutions.face_mesh

        cap = cv2.VideoCapture(0)
        cap.set(3,500)
        cap.set(4,500)
        
        with mp_face_mesh.FaceMesh(max_num_faces=4,refine_landmarks=True,min_detection_confidence=0.5,
                                                            min_tracking_confidence=0.5) as face_mesh:
            
            while cap.isOpened():
                
                success, image = cap.read()
                
                if not success:
                    continue
                    
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(image)
                
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                if results.multi_face_landmarks:
                    
                    try:
                        
                        for face_landmarks in results.multi_face_landmarks:

                            mp_drawing.draw_landmarks(image=image,landmark_list=face_landmarks,
                                connections=mp_face_mesh.FACEMESH_TESSELATION,
                                landmark_drawing_spec=None,
                                connection_drawing_spec=
                                mp_drawing_styles.get_default_face_mesh_tesselation_style())

                    except:
                        
                        pass
                    
                cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
                if cv2.waitKey(5) & 0xFF == 27:
                    break

        cap.release()
        cv2.destroyAllWindows()

# a = mesh_cam()
# a.apply()