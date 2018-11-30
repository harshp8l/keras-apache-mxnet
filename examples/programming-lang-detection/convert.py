import keras
import mxnet

model = keras.models.load_model('./save_tmp.h5')
keras.models.save_mxnet_model(model=model, prefix='progLang_model')
