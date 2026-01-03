import argparse
import os.path
import subprocess


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('src')
    parser.add_argument('dest')
    args = parser.parse_args()

    os.makedirs(args.dest, exist_ok=True)

    with open(args.src) as f:
        for i, line in enumerate(f):
            fname, start, end = line.strip().split('\t')

            basename = os.path.basename(fname)
            noext, _ = os.path.splitext(basename)

            subprocess.check_call((
                'ffmpeg',
                '-ss', start,
                '-to', end,
                '-i', fname,
                '-preset', 'slow',
                f'{args.dest}/{noext}_{i:04}.mov',
            ))


if __name__ == '__main__':
    raise SystemExit(main())
