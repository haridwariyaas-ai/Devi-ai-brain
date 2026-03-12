import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def build_model():

    model = Sequential()

    model.add(Dense(32, activation="relu", input_shape=(3,)))
    model.add(Dense(16, activation="relu"))
    model.add(Dense(2, activation="softmax"))

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model
