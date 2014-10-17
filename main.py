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
    i,
    appendum,
    id_=None
):
    print("mark_rect(img, {},{},{},{})".format(
        filename_template,
        i,
        appendum,
        id_,
    ))
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

    count = 0
    filename = filename_template.format(
        id_,
        "{}.{}".format(appendum, count),
    )
    while(os.path.isfile(filename)):
        count += 1
        filename = filename_template.format(
            id_,
            "{}.{}".format(appendum, count)
        )

    img_part.save(filename)

    print('Saved Image part: {} @{}'.format(
        filename,
        (upperleft, lowerright),
    ))

    return (upperleft, lowerright), img_part, id_, count


def render_image(img):
    print("rerendering..")
    plt.clf()
    plt.imshow(img)
    plt.draw()
    pl.autoscale(False)
    print("OK")


def log_rectangles(
    output_directory, origin, upperleft, lowerright, id_, count, type_
):
    import time

    with open(
        os.path.join(
            output_directory,
            'rects.yaml'
        ),
        "a"
    ) as f:
        message = (
            "- origin: {origin}\n"
            "  upperleft: {upperleft}\n"
            "  lowerright: {lowerright}\n"
            "  id: {id_}\n"
            "  type: {type_}\n"
            "  count: {count}\n"
            "  timestamp: {timestamp}\n"
        ).format(
            origin=origin,
            upperleft=upperleft,
            lowerright=lowerright,
            id_=id_,
            type_=type_,
            count=count,
            timestamp=int(time.time()),
        )

        f.write(message)
        print(message)


def main(
    pages_directory='pages',
    output_directory='output',
    start_page=None,
):
    # TODO save start_page in file
    global i

    i = start_page if start_page is not None\
        else 0

    try:
        os.mkdir(output_directory)
    except Exception as e:
        print(e.message)

    page_names = map(
        partial(os.path.join, pages_directory),
        sorted(os.listdir(pages_directory))
    )
    imgs = map(
        composition(mpimg.imread, teeprint('Loading Image: {}')),
        page_names[:2]
    )
    N = len(imgs)

    fig = plt.figure(1)
    pl.ion()
    pl.show()

    filename_template = os.path.join(output_directory, '{}.{}.png')

    def onkey(event):
        if event.key:
            if event.key in 'ea':
                global latest_id
                if event.key == 'e':
                    (upperleft, lowerright), img_part, id_, count = mark_rect(
                        imgs[i],
                        filename_template,
                        appendum='exercise',
                        i=i,
                        id_=None,
                    )
                    latest_id = id_

                elif event.key == 'a':
                    (upperleft, lowerright), img_part, id_, count = mark_rect(
                        imgs[i],
                        filename_template,
                        appendum='answer',
                        i=i,
                        id_=latest_id
                    )

                log_rectangles(
                    output_directory=output_directory,
                    origin=page_names[i],
                    upperleft=upperleft,
                    lowerright=lowerright,
                    id_=latest_id,
                    count=count,
                    type_={
                        'e': 'exercise',
                        'a': 'answer'
                    }.get(
                        event.key,
                        'unknown'
                    ),
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
