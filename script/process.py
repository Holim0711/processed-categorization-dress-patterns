""" Process images

The original images contain red or black bordered boxes.
And I couldn't have found the real original images of the original images.
So, I just removed the outside of the boxes.
"""
import sys
import csv
import cv2
import numpy as np
from skimage.io import imread, imsave
from tqdm import tqdm


def reader():
    with open("dress_patterns.csv") as file:
        reader = csv.reader(file)
        header = reader.__next__()
        for row in reader:
            yield row


def unique_uids():
    url_uid = dict()
    uids = list()

    for uid, _, _, url in reader():
        if url not in url_uid:
            url_uid[url] = uid
            uids.append(uid)
        else:
            uid = url_uid[url]
            if uid in uids:
                uids.remove(uid)
    return uids


def autosplit(image):
    if len(image.shape) == 2:
        image = np.stack([image]*3, axis=-1)
        bg_color_lb = np.array([0, 0, 0])
        bg_color_ub = np.array([5, 5, 5])
    elif len(image.shape) == 3:
        bg_color_lb = np.array([254, 0, 0])
        bg_color_ub = np.array([255, 0, 0])
        if image.shape[2] != 3:
            image = image[:, :, :3]
    else:
        raise Exception("{} {}".format(uid, img.shape))

    mask = ~cv2.inRange(image, bg_color_lb, bg_color_ub)
    ret, _, stat, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)

    split_list = []
    for idx in range(1, ret):
        top = stat[idx, cv2.CC_STAT_TOP]
        left = stat[idx, cv2.CC_STAT_LEFT]
        w = stat[idx, cv2.CC_STAT_WIDTH]
        h = stat[idx, cv2.CC_STAT_HEIGHT]

        if h == image.shape[0] and w == image.shape[1]:
            continue
        if h < 32 or w < 32:
            continue

        split_list.append(image[top:top + h, left:left + w])

    split_list.sort(key=lambda x: x.shape[0] * x.shape[1], reverse=True)
    return split_list


if __name__ == "__main__":
    for uid in tqdm(unique_uids()):
        try:
            img = imread("image/%s.png" % uid)
            box = autosplit(img)
            if box:
                imsave("bboxed/%s.jpg" % uid, box[0])
        except Exception as e:
            print(file=sys.stderr)
            print("Error on", uid, file=sys.stderr)
            print(e, file=sys.stderr)
            exit()
