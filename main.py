from __future__ import print_function, division

from functools import partial
from threading import RLock
import os

from PIL import Image

import numpy as np
import matplotlib
matplotlib.use('GTKCairo')
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def composition(f, *g):
    if g:
        def _composition(*x):
            return f(composition(*g)(*x))

        return _composition
    else:
        return f


i = 0  # NOTE do not judge me


def teeprint(template="{}"):
    def _teeprint(message):
        print(template.format(message))
        return message
    return _teeprint

def mark_rect(filename_template, original_filename, i):
    filename = 'test.png'
    print("Starting on part: {}".format(filename))
    upperleft,lowerright = map(
        partial(map, int),
        pl.ginput(2)
    )

    pl.plot(
        *zip(*[
            upperleft,
            (upperleft[0], lowerright[1]),
            lowerright,
            (lowerright[0], upperleft[1]),
            upperleft,
        ])
    )
    img_part_raw = img[
        upperleft[1]:lowerright[1],
        upperleft[0]:lowerright[0],
    ]

    img_part = Image.fromarray(
        np.uint8(255*img_part)
    )
    img_part.save(filename)
    print('Saved Image part: {} @{} from {}'.format(
        filename,
    ))
    return (upperleft, lowerright), img_part

def render_image(img):
    print("rerendering..")
    plt.clf()
    plt.imshow(img)
    plt.draw()
    print("OK")



def main(
    directory_pages='output'
):
    global i
    i = 0

    page_names = map(
        partial(os.path.join, directory_pages),
        sorted(os.listdir(directory_pages))
    )
    imgs = map(
        composition(mpimg.imread, teeprint('Loading Image: {}')),
        page_names[:3]
    )
    N = len(imgs)

    img = imgs[0]
    fig = plt.figure(1)
    plt.show()

    lock = RLock()
    def onkey(event):
        try:
            with lock:
                if event.key == 'x':
                    mark_rect('nothing', 'else', 13)
                else:
                    global i
                    if event.key == 'pageup':
                        i += 1
                    if event.key == 'pagedown':
                        i -= 1
                    i %= N
                    if i == -1: i = N - 1
                    print(i)
                    if event.key == 'pageup' or event.key == 'pagedown':
                        render_image(imgs[i])
        except Exception as e:
            print('Error', e.message)

    fig.canvas.mpl_connect(
        'key_press_event',
        onkey
    )

    render_image(img[i])

    pl.close()


if __name__ == '__main__':
    main()
