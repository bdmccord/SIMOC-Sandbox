from keras.models import Sequential
from keras.layers import Dense
import numpy as np

np.random.seed(4)
trainData = np.loadtxt("../trainData.csv", delimiter=",")

train_x = trainData[0:,0:23]
train_y = trainData[0:,[24,25]]

# create model
model = Sequential()
model.add(Dense(10, input_dim=23, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(2, activation='sigmoid'))

# Compile model

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(train_x, train_y, epochs=50, batch_size=40)

# evaluate the model
scores = model.evaluate(train_x, train_y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
