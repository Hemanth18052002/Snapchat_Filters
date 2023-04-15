import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import itertools
import numpy as np

class smoke_cam:
    
    def apply(self):

        self.mp_face_mesh = mp.solutions.face_mesh

        cap = cv2.VideoCapture(0)
        
        cap.set(3,1280)
        cap.set(4,960)
        
        cv2.namedWindow('Face Filter', cv2.WINDOW_NORMAL)
        
        left_eye = cv2.imread("left.png")
        right_eye = cv2.imread("right.png")
        smoke_animation = cv2.VideoCapture("smoke_animation.mp4")
        smoke_frame_counter = 0

        with self.mp_face_mesh.FaceMesh(max_num_faces=4,refine_landmarks=True,
                            min_detection_confidence=0.5,min_tracking_confidence=0.5) as face_mesh:
            
            while cap.isOpened():
                ok, frame = cap.read()
                
                if not ok:
                    continue
                
                _, smoke_frame = smoke_animation.read()
                smoke_frame_counter += 1
                
                if smoke_frame_counter == smoke_animation.get(cv2.CAP_PROP_FRAME_COUNT):    
                    smoke_animation.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    smoke_frame_counter = 0
                
                frame = cv2.flip(frame, 1)
                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(frame)
                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                face_mesh_results=results
                
                if face_mesh_results.multi_face_landmarks:
                    
                    _, mouth_status = self.isOpen(frame, face_mesh_results, 'MOUTH', threshold=15, 
                                            display=False)
                    _, left_eye_status = self.isOpen(frame, face_mesh_results, 'LEFT EYE', 
                                                    threshold=4.5,display=False)
                    _, right_eye_status = self.isOpen(frame, face_mesh_results, 'RIGHT EYE', 
                                                    threshold=4.5,display=False)
                    
                    for face_num, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
                        
                        if left_eye_status[face_num] == 'OPEN':
                            frame = self.overlay(frame, left_eye, face_landmarks,
                                        'LEFT EYE', self.mp_face_mesh.FACEMESH_LEFT_EYE, display=False)
                            
                        if right_eye_status[face_num] == 'OPEN':
                            frame = self.overlay(frame, right_eye, face_landmarks,
                                        'RIGHT EYE', self.mp_face_mesh.FACEMESH_RIGHT_EYE, display=False)
                            
                        if mouth_status[face_num] == 'OPEN':
                            frame = self.overlay(frame, smoke_frame, face_landmarks, 
                                            'MOUTH', self.mp_face_mesh.FACEMESH_LIPS, display=False)
                            
                cv2.imshow('Face Filter', frame)
                k = cv2.waitKey(1) & 0xFF    
                if(k == 27):
                    break
                    
        cap.release()
        cv2.destroyAllWindows()
        
    def isOpen(self,image, face_mesh_results, face_part, threshold=5, display=True):
        
        image_height, image_width, _ = image.shape
        output_image = image.copy()
        status={}
        
        if face_part == 'MOUTH':
            INDEXES = self.mp_face_mesh.FACEMESH_LIPS
            loc = (10, image_height - image_height//40)
            increment=-30  
            
        elif face_part == 'LEFT EYE':
            INDEXES = self.mp_face_mesh.FACEMESH_LEFT_EYE
            loc = (10, 30)
            increment=30
            
        elif face_part == 'RIGHT EYE':
            INDEXES = self.mp_face_mesh.FACEMESH_RIGHT_EYE 
            loc = (image_width-300, 30)
            increment=30
            
        else:
            return
        
        for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
            
            _, height, _ = self.getSize(image, face_landmarks, INDEXES)
            _, face_height, _ = self.getSize(image, face_landmarks, self.mp_face_mesh.FACEMESH_FACE_OVAL)
            
            if (height/face_height)*100 > threshold:
                status[face_no] = 'OPEN'
                color=(0,255,0)

            else:
                status[face_no] = 'CLOSE'
                color=(0,0,255)
                
            cv2.putText(output_image, f'FACE {face_no+1} {face_part} {status[face_no]}.', 
                        (loc[0],loc[1]+(face_no*increment)), cv2.FONT_HERSHEY_PLAIN, 5.0, color, 5)
            
        if display:
            plt.figure(figsize=[10,10])
            plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
            
        else:
            return output_image, status            


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


    def overlay(self,image, filter_img, face_landmarks, face_part, INDEXES, display=True):
        
        annotated_image = image.copy()
        
        try:
            
            filter_img_height, filter_img_width, _  = filter_img.shape
            _, face_part_height, landmarks = self.getSize(image, face_landmarks, INDEXES)
            required_height = int(face_part_height*2.5) 
            
            resized_filter_img = cv2.resize(filter_img, (int(filter_img_width*
                                                            (required_height/filter_img_height)),
                                                        required_height))
            
            filter_img_height, filter_img_width, _  = resized_filter_img.shape
            _, filter_img_mask = cv2.threshold(cv2.cvtColor(resized_filter_img, cv2.COLOR_BGR2GRAY),
                                            25, 255, cv2.THRESH_BINARY_INV)
            
            center = landmarks.mean(axis=0).astype("int")
            
            if face_part == 'MOUTH':
                location = (int(center[0] - filter_img_width / 3), int(center[1]))
            else: 
                location = (int(center[0]-filter_img_width/2), int(center[1]-filter_img_height/2))
                
            ROI = image[location[1]: location[1] + filter_img_height,
                        location[0]: location[0] + filter_img_width]
            
            resultant_image = cv2.bitwise_and(ROI, ROI, mask=filter_img_mask)
            resultant_image = cv2.add(resultant_image, resized_filter_img)
            
            annotated_image[location[1]: location[1] + filter_img_height,
                            location[0]: location[0] + filter_img_width] = resultant_image
            
        except:
            pass
        
        if display:
            plt.figure(figsize=[10,10])
            plt.imshow(annotated_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
            
        else:
            return annotated_image

# a = smoke_cam()
# a.apply()