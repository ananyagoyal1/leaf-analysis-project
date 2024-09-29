# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb
from skimage.segmentation import slic
from skimage.measure import regionprops
import cv2

app = Flask(__name__)
CORS(app)

# Load pre-trained models
disease_model = tf.keras.models.load_model('models/disease_model.h5')
pest_damage_model = tf.keras.models.load_model('models/pest_damage_model.h5')
species_model = tf.keras.models.load_model('models/species_model.h5')

def preprocess_image(image_path):
    img = load_img(image_path, target_size=(299, 299))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

@app.route('/analyze', methods=['POST'])
def analyze_leaf():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image = request.files['image']
    image_path = 'temp_image.jpg'
    image.save(image_path)
    
    # Preprocess image
    processed_image = preprocess_image(image_path)
    
    # Disease detection
    disease_prediction = disease_model.predict(processed_image)
    disease_result = {
        'healthy': float(disease_prediction[0][0]),
        'diseased': float(disease_prediction[0][1])
    }
    
    # Pest damage detection
    pest_prediction = pest_damage_model.predict(processed_image)
    pest_result = {
        'no_damage': float(pest_prediction[0][0]),
        'pest_damage': float(pest_prediction[0][1])
    }
    
    # Leaf morphology analysis
    img = cv2.imread(image_path)
    lab = rgb2lab(img)
    segments = slic(lab, n_segments=100, compactness=10)
    regions = regionprops(segments + 1)
    
    avg_area = np.mean([r.area for r in regions])
    avg_perimeter = np.mean([r.perimeter for r in regions])
    
    morphology_result = {
        'avg_segment_area': float(avg_area),
        'avg_segment_perimeter': float(avg_perimeter)
    }
    
    # Chlorophyll content estimation
    l_channel = lab[:,:,0]
    chlorophyll_estimate = np.mean(l_channel)
    
    # Species identification
    species_prediction = species_model.predict(processed_image)
    species_result = {
        'species1': float(species_prediction[0][0]),
        'species2': float(species_prediction[0][1]),
        'species3': float(species_prediction[0][2])
    }
    
    result = {
        'disease_detection': disease_result,
        'pest_damage': pest_result,
        'leaf_morphology': morphology_result,
        'chlorophyll_content': float(chlorophyll_estimate),
        'species_identification': species_result
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)