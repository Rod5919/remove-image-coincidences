import os
import numpy as np
import cv2
import glob
import pandas as pd
import shutil

class RIC:
    def __init__(self, input_path, output_path, width=403, height=276, image_extension=".jpg"):
        
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.current_dir = os.path.join(self.current_dir, "..")
        
        img_array: list = self.read_images(input_path+image_extension)
        path_array: list = glob.glob(input_path+image_extension)
                
        img_array = self.resize_images(images=img_array, width=width, height=height)
        
        filtered_images = self.remove_coincident_images(images=img_array, paths=path_array)
        
        self.move_files(filtered_images.image_path, output_path)
        print("Filtered images: " + str(len(img_array)-len(filtered_images)))
        
    def read_images(self, path) -> list:
        return [cv2.imread(file) for file in glob.glob(path)]
    
    def move_files(self, paths: list, destination: str):
        for path in paths:
            shutil.copy(path, destination)
            try:
                print(path)
                print(os.path.join(*path.split("/")[:-1],path.split("/")[-1].split(".")[0]+".xml"), destination)
                shutil.copy(os.path.join(*path.split("/")[:-1],path.split("/")[-1].split(".")[0]+".xml"), destination)
            except:
                print("No xml file found for: " + path)
    
    def resize_image(self, image: list, width: int, height: int):
        return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    
    def resize_images(self, images: list, width: int, height: int) -> list:
        # print("Resized images length: " + str(len(images)))
        return [self.resize_image(image, width, height) for image in images]
        
    def remove_coincident_images(self, images: list, paths: list) -> list:
        
        image_strings = self.np_arrays2strings(images)
        image_paths = paths
        df = pd.DataFrame({"image_string": image_strings, "image_path": image_paths})
        df = df.drop_duplicates(subset=["image_string"])
        return df
    
    def np_arrays2strings(self, arrays: list) -> list:
        return [array.tostring() for array in arrays]
    
    def strings2np_arrays(self, strings: list) -> list:
        return [np.fromstring(string, dtype=np.uint8) for string in strings]