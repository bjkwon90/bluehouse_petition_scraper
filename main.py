import argparse
from scraper import Scraper

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--s', type=int, required=True)
    parser.add_argument('--e', type=int)
    parser.add_argument('--o', type=str)
    parser.add_argument('--pkl', action='store_true')
    args = parser.parse_args()

    if args.e != None:
        idx = [i for i in range(args.s, args.e + 1)]
    else:
        idx = args.s

    scp = Scraper(idx)
    scp.req()
    scp.write(args.o, pkl=args.pkl)