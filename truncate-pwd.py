import os

MAX_PATH_SEGMENTS = 3

def main():
    cwd = os.getcwd()
    has_home = cwd.find(os.environ['HOME']) is not -1
    clean_cwd = cwd.replace(os.environ['HOME'], '~', 1)
    segments = clean_cwd.split('/')
    if has_home and len(segments) <= MAX_PATH_SEGMENTS + 1 or not has_home and len(segments) <= MAX_PATH_SEGMENTS:
        print clean_cwd
    else:
        print '~/../' + '/'.join( segments[-MAX_PATH_SEGMENTS:])

if __name__ == '__main__':
    main()