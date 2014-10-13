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

pl.ion()
pl.plot(range(10), range(10))

def composition(f, *g):
    if g:
        def _composition(*x):
            return f(composition(*g)(*x))

        return _composition
    else:
        return f


def main(
    directory_pages='output'
):
    page_names = map(
        partial(os.path.join, directory_pages),
        os.listdir(directory_pages)
    )
    img = mpimg.imread(page_names[0])
    plt.imshow(img)
    plt.show()
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
    img_part = img[
        upperleft[1]:lowerright[1],
        upperleft[0]:lowerright[0],
    ]

    Image.fromarray(
        np.uint8(255*img_part)
    ).save('test.png')

    pl.close()


if __name__ == '__main__':
    main()
