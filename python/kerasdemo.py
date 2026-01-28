"""
Keras Example: Classifying Odd and Even Numbers
This example demonstrates how to build a simple neural network to classify whether a number is odd or even.
"""

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

# Set random seed for reproducibility
np.random.seed(42)

# Generate training data
# Create numbers from 0 to 999
numbers = np.arange(0, 1000)

# Labels: 0 for even, 1 for odd
labels = numbers % 2

# Reshape data for neural network (samples, features)
X = numbers.reshape(-1, 1)
y = labels

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the input data (optional but helpful for neural networks)
X_train_normalized = X_train / 1000.0
X_test_normalized = X_test / 1000.0

print("Training data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)
print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")
print(f"Sample data - Number: {X_train[0][0]}, Label: {'Odd' if y_train[0] == 1 else 'Even'}\n")

# Build the neural network model
model = keras.Sequential([
    layers.Dense(16, activation='relu', input_shape=(1,)),
    layers.Dense(8, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Display model architecture
print("Model Architecture:")
model.summary()
print()

# Train the model
print("Training the model...")
history = model.fit(
    X_train_normalized,
    y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

# Evaluate the model
print("\nEvaluating on test data...")
test_loss, test_accuracy = model.evaluate(X_test_normalized, y_test, verbose=0)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")
print(f"Test Loss: {test_loss:.4f}\n")

# Make predictions on new numbers
print("Testing predictions on specific numbers:")
test_numbers = np.array([5, 10, 17, 24, 33, 42, 99, 100, 257, 888])
test_numbers_normalized = test_numbers.reshape(-1, 1) / 1000.0

predictions = model.predict(test_numbers_normalized, verbose=0)
predicted_classes = (predictions > 0.5).astype(int).flatten()

for num, pred_prob, pred_class in zip(test_numbers, predictions.flatten(), predicted_classes):
    actual = num % 2
    predicted = "Odd" if pred_class == 1 else "Even"
    actual_label = "Odd" if actual == 1 else "Even"
    confidence = pred_prob if pred_class == 1 else (1 - pred_prob)
    correct = "✓" if pred_class == actual else "✗"
    print(f"Number: {num:3d} | Predicted: {predicted:4s} | Actual: {actual_label:4s} | Confidence: {confidence:.4f} | {correct}")

# Plot training history (optional - requires matplotlib)
try:
    import matplotlib.pyplot as plt
    
    print("\nGenerating training plots...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Plot accuracy
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    # Plot loss
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('keras_odd_even_training.png')
    print("Training plots saved to 'keras_odd_even_training.png'")
    
except ImportError:
    print("\nMatplotlib not installed. Skipping visualization.")

# Additional example: Using the model with a custom function
def classify_number(number):
    """Classify a single number as odd or even using the trained model."""
    normalized = np.array([[number / 1000.0]])
    prediction = model.predict(normalized, verbose=0)[0][0]
    predicted_class = "Odd" if prediction > 0.5 else "Even"
    confidence = prediction if prediction > 0.5 else (1 - prediction)
    return predicted_class, confidence

print("\n" + "="*60)
print("Custom Classification Function:")
print("="*60)
for num in [7, 12, 25, 50, 101, 500]:
    pred_class, conf = classify_number(num)
    actual = "Odd" if num % 2 == 1 else "Even"
    print(f"classify_number({num:3d}) -> {pred_class} (confidence: {conf:.4f}) [Actual: {actual}]")
