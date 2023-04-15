import mediapipe as mp
import cv2
import itertools
import numpy as np
import tkinter.filedialog as filedialog
import os


class tuglife_image:
    
    def apply(self):
        
        mp_face_mesh = mp.solutions.face_mesh
        
        file = filedialog.askopenfilename(title='Select Image', filetypes=[('Image Files', '*.jpg *.png *.jpeg')])
        frame = cv2.imread(file)
        
        glass = cv2.imread("thug_glasses.png")
        cigar = cv2.imread("thug_life.png")
        
        with mp_face_mesh.FaceMesh(max_num_faces=4,refine_landmarks=True,min_detection_confidence=0.5) as face_mesh:
                                                    
            results = face_mesh.process(frame)
            
            if results.multi_face_landmarks:
                
                for face_landmarks in results.multi_face_landmarks:

                    frame = self.overlay(frame, cigar, face_landmarks,mp_face_mesh.FACEMESH_LIPS)

                    frame = self.overlay1(frame, glass, face_landmarks,'RIGHT EYE',mp_face_mesh.FACEMESH_RIGHT_EYE)

                download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
                file_name, file_ext = os.path.splitext(os.path.basename(file))
                download_path = os.path.join(download_folder, file_name + "posa" +file_ext)
                cv2.imwrite(download_path, frame)
                print(f'Successfully downloaded image to {download_path}')
    
    
    def getSize(self,image, face_landmarks, INDEXES):
        
        image_height, image_width, _ = image.shape
        INDEXES_LIST = list(itertools.chain(*INDEXES))
        landmarks = []
        
        for INDEX in INDEXES_LIST:
            
            landmarks.append([int(face_landmarks.landmark[INDEX].x * image_width),
                                int(face_landmarks.landmark[INDEX].y * image_height)])
            
        _, _, width, height = cv2.boundingRect(np.array(landmarks))
        landmarks = np.array(landmarks)
        
        return width, height, landmarks


    def overlay(self,image, filter_img, face_landmarks, INDEXES):
        
        annotated_image = image.copy()
        
        try:
            
            filter_img_height, filter_img_width, _  = filter_img.shape
            _, face_part_height, landmarks = self.getSize(image, face_landmarks, INDEXES)
            required_height = int(face_part_height*2.0) 
            
            resized_filter_img = cv2.resize(filter_img, (int(filter_img_width*
                                                            (required_height/filter_img_height)),
                                                        required_height))
            
            filter_img_height, filter_img_width, _  = resized_filter_img.shape
            _, filter_img_mask = cv2.threshold(cv2.cvtColor(resized_filter_img, cv2.COLOR_BGR2GRAY),
                                            25, 255, cv2.THRESH_BINARY_INV)
            
            center = landmarks.mean(axis=0).astype("int")
            location = (int(center[0]), int(center[1]))
            
            ROI = image[location[1]: location[1] + filter_img_height,
                        location[0]: location[0] + filter_img_width] 
            
            resultant_image = cv2.bitwise_and(ROI, ROI, mask=filter_img_mask)
            resultant_image = cv2.add(resultant_image, resized_filter_img)
            
            annotated_image[location[1]: location[1] + filter_img_height,
                            location[0]: location[0] + filter_img_width] = resultant_image
            
        except:
            pass
        
        return annotated_image
        
        
    def overlay1(self,image, filter_img, face_landmarks, face_part, INDEXES):
        
        annotated_image = image.copy()
        
        try:
            
            filter_img_height, filter_img_width, _  = filter_img.shape
            _, face_part_height, landmarks = self.getSize(image, face_landmarks, INDEXES)
            required_height = int(face_part_height*2.5) 
            
            resized_filter_img = cv2.resize(filter_img, (int(filter_img_width*
                                                            1.2*(required_height/filter_img_height))
                                                         ,required_height))
            filter_img_height, filter_img_width, _  = resized_filter_img.shape
            
            center = landmarks.mean(axis=0).astype("int")
            
            if face_part == 'RIGHT EYE':
                location = (int(center[0] - filter_img_width / 4), int(center[1]-filter_img_height/2))
            else: 
                location = (int(center[0]-filter_img_width/2), int(center[1]-filter_img_height/2))
            
            annotated_image[location[1]: location[1] + filter_img_height,
                            location[0]: location[0] + filter_img_width] = resized_filter_img
            
        except:
            pass
        
        return annotated_image

# a = tuglife_image()
# a.apply()