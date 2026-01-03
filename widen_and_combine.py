import argparse


def to_s(s: str) -> int:
    parts = s.split(':')
    ret = 0
    mult = 1
    while parts:
        ret += mult * int(parts.pop())
        mult *= 60
    return ret


assert to_s('5') == 5
assert to_s('01:05') == 65
assert to_s('01:02:05') == 3725


def _t(seconds: int) -> str:
    hours = seconds // 60 // 60
    minutes = seconds % (60 * 60) // 60
    seconds = seconds % 60

    if hours:
        return f'{hours:02}:{minutes:02}:{seconds:02}'
    else:
        return f'{minutes:02}:{seconds:02}'


def _printit(fname: str, start: int, end: int) -> None:
    if end - start > 30:
        return
    print(f'{fname}\t{_t(start)}\t{_t(end)}')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('out')
    args = parser.parse_args()

    prev = None
    with open(args.out) as f:
        for line in f:
            fname, start, end = line.rsplit(maxsplit=2)

            start_s, end_s = to_s(start) - 3, to_s(end) + 3

            if prev is None:
                prev = fname, start_s, end_s
            elif prev[0] != fname or start_s >= prev[-1]:
                _printit(*prev)
                prev = fname, start_s, end_s
            else:
                prev = fname, prev[1], max(prev[2], end_s)

    if prev is not None:
        _printit(*prev)


if __name__ == '__main__':
    raise SystemExit(main())
