import pickle as pckl
import numpy as np
import codecs

DESCRIPTOR_VEC_SHAPE = [300,]
GALLERY_IMG_NUM = 20


def empty_embed_vec():
    return np.zeros(DESCRIPTOR_VEC_SHAPE)

def obj2pickled(obj):
    return codecs.encode(pckl.dumps(obj), "base64").decode()

def pickled2obj(pickled):
    return pckl.loads(codecs.decode(pickled.encode(), "base64"))

def find_similar(pref_vec,images, k_similar=20):
    sim = []
    for img in images:
        img_vec = pickled2obj(img.txt_vec)
        similarity = np.arccos(np.dot(img_vec, pref_vec) / (np.linalg.norm(img_vec) * np.linalg.norm(pref_vec)))
        sim.append((img.id, similarity))

    sim.sort(key=lambda tup: tup[1])
    indices = map(lambda rec: rec[0], sim[:k_similar])
    return indices