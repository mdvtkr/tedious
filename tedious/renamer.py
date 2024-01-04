from pathlib import Path
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('two argument expected: old, new')
    else:
        old = sys.argv[1]
        new = sys.argv[2]
        for fpath in Path('./').iterdir():
            if fpath.is_dir():
                continue

            if old in str(fpath.name):
                new_name = fpath.name.replace(old, new)
                print(fpath.name + ' -> ' + new_name)
                fpath.rename(new_name)
                

