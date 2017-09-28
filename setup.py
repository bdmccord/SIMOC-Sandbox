import os, sys,shutil

def main():
    os.system('pip install -r requirements.txt')
    import mesa
    path = os.path.join(mesa.__file__[:-12],"visualization","templates")
    paths = [os.path.join(path,'css'),
             os.path.join(path,'js'),
             os.path.join(path,'js'),
             path]

    src_files = os.listdir('updates/')

    for src,dest in zip(src_files,paths):
        print ('Copying ' + src + '...')
        shutil.copy('updates/' + src, dest)
    print ('Finished.')

if sys.version_info[0] != 3:
    print("This update requires Python version 3\nRun again with python3")
    sys.exit(1)

if __name__ == "__main__":
    main()
