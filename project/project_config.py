import pickle as pckl
import numpy as np
import codecs

DESCRIPTOR_VEC_SHAPE = [300,]
GALLERY_IMG_NUM = 16


def obj2pickled(obj):
    return codecs.encode(pckl.dumps(obj), "base64").decode()


def deafult_user_pref_vec():
    return obj2pickled(np.zeros(DESCRIPTOR_VEC_SHAPE))