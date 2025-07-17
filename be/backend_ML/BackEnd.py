from skimage.feature import graycomatrix, graycoprops
import cv2
import pandas as pd
import numpy as np
from skimage import io, exposure, img_as_ubyte
import joblib, pickle, os

# Set the current working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Now open the file using its relative path
with open('label_encoder.pkl', 'rb') as le_file:
    le = pickle.load(le_file)

size = 128

def feature_extractor(dataset):

    distances = [1, 3, 5, 9]
    distances_arr = np.array(distances)
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4, 5*np.pi/4, 3*np.pi/2, 7*np.pi/4]
    image_dataset = pd.DataFrame()

    #for image in range(dataset.shape[0]):  # iterate through each file
    df = pd.DataFrame()  # Temporary data frame to capture information for each loop. Will be reset each time

    #img = dataset[image, :, :]  # Extract current image from dataset
    img = dataset
    # Loop over distances
    #for distance in distances_arr:
        # Loop over angles
            #for angle in angles:
            # Compute GLCM for the current combination of distance and angle

    GLCM = graycomatrix(img, distances_arr, angles, levels=256, symmetric=True, normed=True)
            # Compute properties of GLCM
    GLCM_energy = graycoprops(GLCM, 'energy')[0]
    df[f'Energy'] = GLCM_energy

    GLCM_corr = graycoprops(GLCM, 'correlation')[0]
    df[f'Corr'] = GLCM_corr

    GLCM_diss = graycoprops(GLCM, 'dissimilarity')[0]
    df[f'Diss_sim'] = GLCM_diss

    GLCM_hom = graycoprops(GLCM, 'homogeneity')[0]
    df[f'Homogen'] = GLCM_hom

    GLCM_contr = graycoprops(GLCM, 'contrast')[0]
    df[f'Contrast'] = GLCM_contr

    # Concatenate the dataframe for each image to the image_dataset dataframe
    image_dataset = pd.concat([image_dataset, df], ignore_index=True)

    return image_dataset


def main(image_path):
    frac_class_model = joblib.load('Exported_ML_Model.pkl')
    global size, le
    img_path = image_path 
    raw_img=io.imread(img_path, as_gray=True)
    hist_img = exposure.equalize_adapthist(raw_img)
    ub_img = img_as_ubyte(hist_img)
    img = cv2.resize(ub_img, (size, size))

    #input_img = np.expand_dims(img, axis=0) #Expand dims so the input is (num images, x, y, c)
    input_img_features = feature_extractor(img)

    input_img_features = np.expand_dims(input_img_features, axis=0)

    #input_img_for_SVM = np.reshape(input_img_features, (img.shape[0], -1))
    input_img_for_SVM = np.reshape(input_img_features, (1, -1))

    #Predict
    img_prediction = frac_class_model.predict(input_img_for_SVM)
    img_prediction=np.argmax(img_prediction, axis=0)


    img_prediction = le.inverse_transform([img_prediction])  #Reverse the label encoder to original name
    output =  str(img_prediction[0])

    print("The prediction for this image is: ", output)
    print(f'Data type is:{type(output)}')
    
    return output

