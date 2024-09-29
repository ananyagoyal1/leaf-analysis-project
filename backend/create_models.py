import tensorflow as tf
from tensorflow.keras import layers, models

# Function to create a simple CNN model
def create_simple_cnn(num_classes, input_shape=(299, 299, 3)):
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

# Create and save disease detection model
disease_model = create_simple_cnn(num_classes=2)  # 2 classes: healthy, diseased
disease_model.save('disease_model.h5')

# Create and save pest damage detection model
pest_damage_model = create_simple_cnn(num_classes=2)  # 2 classes: no damage, pest damage
pest_damage_model.save('pest_damage_model.h5')

# Create and save species identification model
species_model = create_simple_cnn(num_classes=3)  # 3 classes: species1, species2, species3
species_model.save('species_model.h5')

print("Models created and saved successfully.")







