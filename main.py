import argparse

def main(args):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Filter")
    args = parser.parse_args()
    print(args)
    main(args)