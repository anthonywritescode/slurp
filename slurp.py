from __future__ import annotations
import numpy
import argparse
import cv2


def _t(fid: int) -> str:
    seconds = fid // 30
    hours = seconds // 60 // 60
    minutes = seconds % (60 * 60) // 60
    seconds = seconds % 60

    if hours:
        return f'{hours:02}:{minutes:02}:{seconds:02}'
    else:
        return f'{minutes:02}:{seconds:02}'


def _has_water(frame: numpy.ndarray) -> bool:
    crop = frame[100:300, 1477:1700]
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    m = None
    for lo, hi in (
        ((100, 125, 210), (120, 165, 245)),
        ((103, 110, 35), (125, 170, 65)),
        ((103, 140, 130), (117, 170, 195)),
        ((107, 125, 75), (128, 200, 130)),
        ((108, 125, 115), (119, 180, 135)),
        ((116, 115, 110), (125, 140, 175)),
        ((125, 115, 80), (131, 150, 145)),
    ):
        thres = cv2.inRange(hsv, lo, hi)
        if m is None:
            m = thres
        else:
            m = cv2.bitwise_or(m, thres)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, kernel)

    return numpy.count_nonzero(m) >= 1800


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args()

    for fname in args.filenames:
        start = None
        vid = cv2.VideoCapture(fname)
        fid = 0
        while True:
            for _ in range(5):
                vid.grab()
                fid += 1
            ret, frame = vid.read()
            fid += 1
            if not ret:
                break

            if start is None and _has_water(frame):
                start = fid
            elif start is not None and not _has_water(frame):
                print(f'{fname} {_t(start)} {_t(fid)}')
                start = None

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
