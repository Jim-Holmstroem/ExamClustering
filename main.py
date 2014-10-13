from __future__ import print_function, division

from functools import partial

import os

from PIL import Image

import numpy as np
import matplotlib
matplotlib.use('GTKCairo')
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


i = 0  # NOTE do not judge me  (ugly but easy)
latest_id = None


def composition(f, *g):
    if g:
        def _composition(*x):
            return f(composition(*g)(*x))

        return _composition
    else:
        return f


def teeprint(template="{}"):
    def _teeprint(message):
        print(template.format(message))
        return message
    return _teeprint


def mark_rect(
    img,
    filename_template,
    original_filename,
    i,
    appendum,
    id_=None
):
    print("Starting on part for: {}".format(original_filename))

    upperleft, lowerright = map(
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
        np.uint8(255*img_part_raw)
    )

    id_ = hash(img_part_raw) if id_ is None\
        else id_

    def find_proper_filename(filename):
        return os.path.splitext(os.path.basename(filename))[0]

    filename = filename_template.format(
        find_proper_filename(original_filename),
        id_,
        appendum,
    )
    img_part.save(filename)

    print('Saved Image part: {} @{} from {}'.format(
        filename,
        (upperleft, lowerright),
        original_filename,
    ))

    return (upperleft, lowerright), img_part, id_


def render_image(img):
    print("rerendering..")
    plt.clf()
    plt.imshow(img)
    plt.draw()
    pl.autoscale(False)
    print("OK")


def main(
    pages_directory='pages',
    output_directory='output',
    start_page=0,
):
# TODO save start_page in file
    global i
    i = start_page

    try:
        os.mkdir(output_directory)
    except Exception as e:
        pass

    page_names = map(
        partial(os.path.join, pages_directory),
        sorted(os.listdir(pages_directory))
    )
    imgs = map(
        composition(mpimg.imread, teeprint('Loading Image: {}')),
        page_names[:3]
    )
    N = len(imgs)

    fig = plt.figure(1)
    pl.ion()
    pl.show()

    filename_template = os.path.join(output_directory, '{}_{}.{}.png')

    def onkey(event):
        if event.key in 'ea':
            global latest_id
            if event.key == 'e':
                (upperleft, lowerright), img_part, id_ = mark_rect(
                    imgs[i],
                    filename_template,
                    page_names[i],
                    appendum='exercise',
                    i=i,
                    id_=None,
                )
                latest_id = id_

            elif event.key == 'a':
                (upperleft, lowerright), img_part, id_ = mark_rect(
                    imgs[i],
                    filename_template,
                    page_names[i],
                    appendum='answer',
                    i=i,
                    id_=latest_id
                )

        elif event.key in ['pageup', 'pagedown']:
            global i
            i += {
                'pageup': 1,
                'pagedown': -1,
            }[event.key]

            i %= N
            if i == -1:
                i = N - 1

            print(i)
            render_image(imgs[i])

    fig.canvas.mpl_connect(
        'key_press_event',
        onkey
    )

    render_image(imgs[i])


if __name__ == '__main__':
    main()
