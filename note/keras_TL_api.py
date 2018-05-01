TL
fine-turning 全连接层最好是sigmod,relu的主要用途是避免梯度消失或爆炸，往往最后通过预训练的模型参数用于模型会导致
NAN，用sigmod可以起clip作用。
lower learning-rate(e-7)
http://keras-cn.readthedocs.io/en/latest/other/application/

from keras.layers import Input, Flatten,Lambda,GlobalAveragePooling2D,Dense, Dropout, Activation, BatchNormalization, GlobalMaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.models import Model
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.applications import ResNet50,InceptionV3,Xception,VGG16,VGG19,inception_v3,xception
import h5py
from tqdm import tqdm



# 自己导出特征向量
def write_gap(MODEL, image_size, lambda_func=None):#None==0
    width = image_size[0]
    height = image_size[1]
    # Keras    API
    input_tensor = Input((height, width, 3))
    # x = input_tensor
    if lambda_func:
        x = Lambda(lambda_func)(input_tensor)
    base_model = MODEL(input_tensor=input_tensor, weights='imagenet', include_top=False)
    # base_model.input:keras input tensor [?,224,224,3] 指明输入和输出
    model = Model(base_model.input, GlobalAveragePooling2D()(base_model.output))#[?,1,1,2048] input
    
    gen = ImageDataGenerator()
    train_generator = gen.flow_from_directory("/home/naruto/PycharmProjects/data/cats_dogs/train2", image_size, shuffle=False,
                                              batch_size=16)
    test_generator = gen.flow_from_directory("/home/naruto/PycharmProjects/data/cats_dogs/test2", image_size, shuffle=False,
                                             batch_size=16, class_mode=None)
    # 导出特征向量
    train = model.predict_generator(train_generator, train_generator.nb_sample)
    test = model.predict_generator(test_generator, test_generator.nb_sample)
    with h5py.File("gap_%s.h5"%MODEL.func_name) as h:
        h.create_dataset("train", data=train)
        h.create_dataset("test", data=test)
        h.create_dataset("label", data=train_generator.classes)
write_gap(ResNet50, (224, 224))
write_gap(InceptionV3, (299, 299), inception_v3.preprocess_input)
write_gap(Xception, (299, 299), xception.preprocess_input)

# 利用模型
for filename in ["gap_ResNet50.h5", "gap_Xception.h5", "gap_InceptionV3.h5"]:
    with h5py.File(filename, 'r') as h:
        X_train.append(np.array(h['train']))
        X_test.append(np.array(h['test']))
        y_train = np.array(h['label'])
        #label 只要任意一个模型的label就可以啦，不需要写到循环中
        # print (y_train[:2])
print (np.shape(X_train))#(3,25000,2048)
# 合成一条特征向量
X_train = np.concatenate(X_train, axis=1)#25000X6144
print (np.shape(X_train))
print (np.shape(y_train))
X_test = np.concatenate(X_test, axis=1)
X_train, y_train = shuffle(X_train, y_train)

from keras.models import Model
from keras.layers import Input,Dropout,Dense

input_tensor = Input(X_train.shape[1:])#6144
x = input_tensor #6144
x = Dropout(0.5)(x)
x = Dense(1, activation='sigmoid')(x)
model = Model(input_tensor, x)#input x ,ouput 1
model.compile(optimizer='adadelta',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.fit(X_train, y_train, batch_size=128, nb_epoch=8, validation_split=0.2)
model.save('model.h5')
# model.save_weights('.h5')
# model.load_weights('my_model_weights.h5')

# 测试
y_pred = model.predict(X_test, verbose=1)
y_pred = y_pred.clip(min=0.005, max=0.995)#trick
import pandas as pd
from keras.preprocessing.image import ImageDataGenerator

df = pd.read_csv("sample_submission.csv")
image_size = (224, 224)
gen = ImageDataGenerator()
test_generator = gen.flow_from_directory("/home/naruto/PycharmProjects/data/cats_dogs/test2", image_size, shuffle=False,
                                         batch_size=16, class_mode=None)

直接从其他模型导入的迁移值用于输入
input_tensor=Input(transfer_values_train.shape[1:])
x=Dropout(0.5)(input_tensor)
# x=Dense(10,activation='sigmoid')(x)
x=BatchNormalization(momentum=0.8)(x)
x=Activation(activation='sigmoid')(x)
x=Dense(10)(x)

model=Model(input_tensor,x)
model.compile(optimizer='adadelta',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.fit(transfer_values_train, cls_train_onehot, batch_size=128, nb_epoch=8, validation_split=0.2)




# API
gen = ImageDataGenerator(preprocessing_function=preprocess_input)
train_data = gen.flow_from_directory('train', target_size=(224, 224), batch_size=1, shuffle=False)
base_model = VGG19(include_top=False,weights='imagenet',input_shape=(224, 224, 3),pooling=None)
train_X = base_model.predict_generator(train_data, steps=train_data.n)
model.summary()
model.compile(Adam(lr=1e-4), 'categorical_crossentropy', metrics=['accuracy'])
model.fit(x=trn_X, y=trn_y, batch_size=6, epochs=40, validation_data=(val_X, val_y), verbose=2)

Sequential models：这种方法用于实现一些简单的模型。你只需要向一些存在的模型中添加层就行了。
from keras.models import Sequential
models = Sequential()
from keras.layers import Dense, Activation, Conv2D, MaxPooling2D, Flatten, Dropout
model.add(Conv2D(64, (3,3), activation='relu', input_shape = (100,100,32)))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Flatten())
model.compile(loss='binary_crossentropy', optimizer='rmsprop')
from keras.optimizers import SGD
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd)
model.fit(x_train, y_train, batch_size = 32, epochs = 10, validation_data(x_val, y_val))
score = model.evaluate(x_test, y_test, batch_size = 32)


Functional API：Keras的API是非常强大的，你可以利用这些API来构造更加复杂的模型，比如多输出模型，有向无环图等等

参考：https://segmentfault.com/a/1190000012645225



model = applications.VGG16(weights='imagenet')
img = image.load_img('cat.jpeg', target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
preds = model.predict(x)
for results in decode_predictions(preds):
    for result in results:
        print('Probability %0.2f%% => [%s]' % (100*result[2], result[1]))

for layers in base_model.layers:
    layers.trainable = False
x = GlobalAveragePooling2D()(base_model.output)
model = Model(base_model.input, x)
zip([x.name for x in model.layers], range(len(model.layers)))
weights = model.layers[177].get_weights()[0]
model2 = Model(model.input, [model.layers[172].output, model.output])
for layer in model.layers[140:]:
    layer.trainable = True
model.fit(X_train, y_train, batch_size=16, epochs=5, validation_data=(X_valid, y_valid))

history = new_model.fit_generator(generator=generator_train,
                                  epochs=epochs,
                                  steps_per_epoch=steps_per_epoch,
                                  class_weight=class_weight,
                                  validation_data=generator_test,
                                  validation_steps=steps_test)

from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K
from keras.utils.visualize_util import plot

model.add(Dense(32, input_dim=784)) model.add(Activation('relu'))
 evaluate(self, x, y, batch_size=32, verbose=1, sample_weight=None)
 predict(self, x, batch_size=32, verbose=0)
 fit

 每个epoch以经过模型的样本数达到samples_per_epoch时，记一个epoch结束

