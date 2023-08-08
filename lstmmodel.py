import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import Series
# %matplotlib inline
import warnings
warnings.filterwarnings("ignore")
import tensorflow as tf
import random as rn
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation, SimpleRNN, GRU
from sklearn.preprocessing import MinMaxScaler
import os
from keras import optimizers
from keras.utils.vis_utils import plot_model
from keras import backend as K
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
import io
from keras.models import load_model
import csv
import matplotlib.pyplot as plt
from keras.callbacks import Callback
import keras.backend as K
import numpy as np
from keras import regularizers
os.environ['PYTHONHASHSEED'] = '0'
np.random.seed(2017)  
rn.seed(12345)



def apply():
    '''
    from google.colab import files
    uploaded = files.upload()
    '''
    xy = pd.read_csv('corr_op.csv', )#skiprows=(10))



    xy = xy.replace(-999, np.nan)
    #x2 = x2.replace(-999, np.nan)
    #x3 = x3.replace(-999, np.nan)

    xy = xy.fillna(xy.mean())
    #x2 = x2.fillna(x2.mean())
    #x3 = x3.fillna(x3.mean())
    xy = xy.set_index(['year', 'month', 'date'])
    #xy.columns
    #xy.describe()
    # convert series to supervised learning
    def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
        n_vars = 1 if type(data) is list else data.shape[1]
        df = pd.DataFrame(data)
        cols, names = list(), list()
        # input sequence (t-n, ... t-1)
        for i in range(n_in, 0, -1):
            cols.append(df.shift(i))
            names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
        # forecast sequence (t, t+1, ... t+n)
        for i in range(0, n_out):
            cols.append(df.shift(-i))
            if i == 0:
                names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
            else:
                names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
        # put it all together
        agg = pd.concat(cols, axis=1)
        agg.columns = names
        # drop rows with NaN values
        if dropnan:
            agg.dropna(inplace=True)
        return agg

    # load dataset
    values = xy.values
    # ensure all data is float
    values = values.astype('float32')
    ## normalize features
    #scaler = MinMaxScaler(feature_range=(0, 1))
    #scaled = scaler.fit_transform(values)
    # frame as supervised learning
    reframed = series_to_supervised(values, 9, 1)
    # drop columns we don't want to predict
    #print(reframed.head())
    #reframed.columns
    reframed = reframed[reframed.columns]
    #reframed.columns
    #reframed.shape
    reframed_shape_x=reframed.shape[0]
    reframed_shape_y=reframed.shape[1]
    values = reframed.values
    #values
    while(reframed_shape_x%4!=0):
        reframed_shape_x= reframed_shape_x - 1
        reframed_shape_y=reframed_shape_y - 1
        dataset = np.array(values)
        x = dataset[:,0:reframed_shape_y]
        y = dataset[:,[reframed_shape_y]]


    scaler1 = MinMaxScaler(feature_range=(0, 1))
    x = scaler1.fit_transform(x)
    scaler2 = MinMaxScaler(feature_range=(0, 1))
    y = scaler2.fit_transform(y)
    '''
    print(x.shape)
    print(y.shape)
    print(x[0:10])
    print(y[0:10])
    '''
    '''
    plt.figure()
    plt.plot(y)
    '''
    # x.shape, y.shape

    # split to train and testing
    '''
    train_size = 5196
    test_size = 2598
    '''
    total_values_by_2 = int(reframed_shape_x/2)
    train_size = int(total_values_by_2*2/3)
    test_size = total_values_by_2-train_size
    '''
    train_size = 160
    test_size = 80
    '''

    test_index = train_size + test_size
    trainX, testX = np.array(x[0:train_size]), np.array(
        x[train_size:test_index])
    trainY, testY = np.array(y[0:train_size]), np.array(
        y[train_size:test_index])
    '''
    print(len(trainX))
    print(len(testX))
    print(trainX.shape)
    print(testX.shape)
    len(trainX)
    '''
    # reshape input to be [samples, time steps, features]

    trainX = np.reshape(trainX, (trainX.shape[0], int(trainX.shape[1]/4), 4))#pehle yaha 9,4 tha 7*4==trainX.shape[1]
    testX = np.reshape(testX, (testX.shape[0], int(testX.shape[1]/4), 4))

    #print(trainX)

    class SGDRScheduler(Callback):
        '''Cosine annealing learning rate scheduler with periodic restarts.
        # Usage
            ```python
                schedule = SGDRScheduler(min_lr=1e-5,
                                        max_lr=1e-2,
                                        steps_per_epoch=np.ceil(epoch_size/batch_size),
                                        lr_decay=0.9,
                                        cycle_length=5,
                                        mult_factor=1.5)
                model.fit(X_train, Y_train, epochs=100, callbacks=[schedule])
            ```
        # Arguments
            min_lr: The lower bound of the learning rate range for the experiment.
            max_lr: The upper bound of the learning rate range for the experiment.
            steps_per_epoch: Number of mini-batches in the dataset. Calculated as `np.ceil(epoch_size/batch_size)`. 
            lr_decay: Reduce the max_lr after the completion of each cycle.
                    Ex. To reduce the max_lr by 20% after each cycle, set this value to 0.8.
            cycle_length: Initial number of epochs in a cycle.
            mult_factor: Scale epochs_to_restart after each full cycle completion.
        # References
            Blog post: jeremyjordan.me/nn-learning-rate
            Original paper: http://arxiv.org/abs/1608.03983
        '''
        def __init__(self,
                    min_lr,
                    max_lr,
                    steps_per_epoch,
                    lr_decay=1,
                    cycle_length=10,
                    mult_factor=2):

            self.min_lr = min_lr
            self.max_lr = max_lr
            self.lr_decay = lr_decay

            self.batch_since_restart = 0
            self.next_restart = cycle_length

            self.steps_per_epoch = steps_per_epoch

            self.cycle_length = cycle_length
            self.mult_factor = mult_factor

            self.history = {}

        def clr(self):
            '''Calculate the learning rate.'''
            fraction_to_restart = self.batch_since_restart / (self.steps_per_epoch * self.cycle_length)
            lr = self.min_lr + 0.5 * (self.max_lr - self.min_lr) * (1 + np.cos(fraction_to_restart * np.pi))
            return lr

        def on_train_begin(self, logs={}):
            '''Initialize the learning rate to the minimum value at the start of training.'''
            logs = logs or {}
            K.set_value(self.model.optimizer.lr, self.max_lr)

        def on_batch_end(self, batch, logs={}):
            '''Record previous batch statistics and update the learning rate.'''
            logs = logs or {}
            self.history.setdefault('lr', []).append(K.get_value(self.model.optimizer.lr))
            for k, v in logs.items():
                self.history.setdefault(k, []).append(v)

            self.batch_since_restart += 1
            K.set_value(self.model.optimizer.lr, self.clr())

        def on_epoch_end(self, epoch, logs={}):
            '''Check for end of current cycle, apply restarts when necessary.'''
            if epoch + 1 == self.next_restart:
                self.batch_since_restart = 0
                self.cycle_length = np.ceil(self.cycle_length * self.mult_factor)
                self.next_restart += self.cycle_length
                self.max_lr *= self.lr_decay
                self.best_weights = self.model.get_weights()

        def on_train_end(self, logs={}):
            '''Set weights to the values from the end of the most recent cycle for best performance.'''
            self.model.set_weights(self.best_weights)


    epoch_size=len(trainX)
    batch_size=32
    #print(trainX.shape, trainY.shape)

    schedule = SGDRScheduler(min_lr=1e-5, max_lr=1e-2, steps_per_epoch=np.ceil(epoch_size/batch_size), lr_decay=0.9, cycle_length=5, mult_factor=1.5)
    from keras import regularizers

    model = Sequential()
    model.add(LSTM(12, input_shape=(trainX.shape[1], trainX.shape[2]), return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(2, return_sequences=True))
    model.add(LSTM(2, return_sequences=True))
    model.add(LSTM(2, return_sequences=True))
    model.add(LSTM(2, return_sequences=False))
    model.add(Dense(trainY.shape[1]))
    model.add(Activation("linear"))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])

    #model.summary()

    history=model.fit(trainX, trainY, epochs=100, batch_size=32, validation_split = 0.2, callbacks=[schedule])

    '''
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()
    '''


    model.save('model_10rnnadam.h5')  # creates a HDF5 file 'my_model.h5'
    #del model  # deletes the existing model

    # returns a compiled model
    # identical to the previous one
    #model = load_model('my_model.h5')
    trainPredict1 = model.predict(trainX)
    testPredict1 = model.predict(testX)
    '''
    plt.plot(trainY)
    plt.plot(trainPredict1)
    plt.show()
    plt.plot(testY)
    plt.plot(testPredict1)
    plt.show()


    from sklearn.metrics import mean_squared_error
    from math import sqrt
    MSE1=mean_squared_error(testY, testPredict1)
    print("MSE:",MSE1)

    RMSE1=sqrt(MSE1)
    print("RMSE:",RMSE1)

    from sklearn.metrics import r2_score
    R2_score1=r2_score(testY, testPredict1)
    print("R2 score:", R2_score1)
    '''


    # split to train and testing
    start_new = test_size
    end_new = test_size+train_size
    trainX2, testX2 = np.array(x[start_new:end_new]), np.array(
        x[end_new:end_new+test_size])
    trainY2, testY2 = np.array(y[start_new:end_new]), np.array(
        y[end_new:end_new+test_size])
    '''
    print(len(trainX2))
    print(len(testX2))
    '''
    # reshape input to be [samples, time steps, features]
    trainX2 = np.reshape(trainX2, (trainX2.shape[0], int(trainX.shape[1]), 4))
    testX2 = np.reshape(testX2, (testX2.shape[0], int(testX.shape[1]), 4))

    #print(trainX2)

    model = load_model('model_10rnnadam.h5')

    #model.summary()
    #print(trainX2.shape, trainY2.shape)
    history2=model.fit(trainX2, trainY2, epochs=100, batch_size=32, validation_split = 0.2, callbacks=[schedule])
    '''
    # summarize history for loss
    plt.plot(history2.history['loss'])
    plt.plot(history2.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()
    model.save('model_10rnnadam.h5')
    trainPredict2 = model.predict(trainX2)
    testPredict2 = model.predict(testX2)

    plt.plot(trainY2)
    plt.plot(trainPredict2)
    plt.show()
    plt.plot(testY2)
    plt.plot(testPredict2)
    plt.show()

    from sklearn.metrics import mean_squared_error
    from math import sqrt
    MSE2=mean_squared_error(testY2, testPredict2)
    print("MSE:",MSE2)

    RMSE2=sqrt(MSE2)
    print("RMSE:",RMSE2)

    from sklearn.metrics import r2_score
    R2_score2=r2_score(testY2, testPredict2)
    print("R2 score:", R2_score2)
    '''
    start_new = len(trainX2)
    end_new = 2*start_new
    # split to train and testing

    trainX3, testX3 = np.array(x[start_new:end_new]), np.array(
        x[end_new:end_new+test_size])
    trainY3, testY3 = np.array(y[start_new:end_new]), np.array(
        y[end_new:end_new+test_size])
    '''
    print(len(trainX3))
    print(len(testX3))
    '''
    # reshape input to be [samples, time steps, features]
    trainX3 = np.reshape(trainX3, (trainX3.shape[0], int(trainX.shape[1]), 4))
    testX3 = np.reshape(testX3, (testX3.shape[0], int(testX.shape[1]), 4))

    # print(trainX3)


    model = load_model('model_10rnnadam.h5')

    # model.summary()
    # print(trainX3.shape, trainY3.shape)
    history3=model.fit(trainX3, trainY3, epochs=100, batch_size=32, validation_split = 0.2, callbacks=[schedule])
    '''
    # summarize history for loss
    plt.plot(history3.history['loss'])
    plt.plot(history3.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()
    '''
    model.save('model_10rnnadam.h5')

    trainPredict3 = model.predict(trainX3)
    testPredict3 = model.predict(testX3)
    '''
    plt.plot(trainY3)
    plt.plot(trainPredict3)
    plt.show()
    plt.plot(testY3)
    plt.plot(testPredict3)
    plt.show()
    from sklearn.metrics import mean_squared_error
    from math import sqrt
    MSE3=mean_squared_error(testY3, testPredict3)
    print("MSE:",MSE3)

    RMSE3=sqrt(MSE3)
    print("RMSE:",RMSE3)

    from sklearn.metrics import r2_score
    R2_score3=r2_score(testY3, testPredict3)
    print("R2 score:", R2_score3)
    AvMSE=(MSE1+MSE2+MSE3)/3
    AvRMSE=(RMSE1+RMSE2+RMSE3)/3
    Avr2=(R2_score1+R2_score2+R2_score3)/3

    print("Average MSE:",AvMSE)
    print("Average RMSE:",AvRMSE)
    print("Average R2 score:",Avr2)
    '''
    # print(testPredict3)
    header_csv = ['year', 'month','date','value']
    with open('lstm_output.csv','w',newline='') as csvfile:
        df = pd.read_csv('corr_op.csv')
        req_len = len(testPredict3)
        yr = df['year'].tolist()
        yr = yr[-req_len:]
        mo = df['month'].tolist()
        mo = mo[-req_len:]
        da = df['date'].tolist()
        da = da[-req_len:]
        csvwriter = csv.writer(csvfile)
        csvwriter.writer(header_csv)
        csvwriter.writerows(zip(yr,mo,da,testPredict3))
        