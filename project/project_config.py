import pickle as pckl
import numpy as np

DESCRIPTOR_VEC_SHAPE = [300,]
GALLERY_IMG_NUM = 16


def deafult_user_pref_vec():
    return pckl.dumps(np.zeros(DESCRIPTOR_VEC_SHAPE))