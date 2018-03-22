import numpy as np
import tqdm
from skimage.io import imread
from skimage.transform import resize
import matplotlib.pyplot as plt

import stl10_input as STL10

#STL-10
DATA_PATH = './train_X.bin'
LABEL_PATH = './train_y.bin'

x_inp = STL10.read_all_images(DATA_PATH)
label = STL10.read_labels(LABEL_PATH)

x_processed = np.load('./processed_train_X.npy')

for index, img in tqdm.tqdm(enumerate(x_inp)):
    test_img = resize(img,(229,229), mode = 'constant')
    processed_vector = x_processed[index]
    plt.imshow(test_img)
    plt.show()
