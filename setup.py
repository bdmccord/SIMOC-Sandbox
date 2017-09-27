import os, sys,shutil

if sys.version_info[0] != 3:
    print("This update requires Python version 3\nRun again with python3")
    sys.exit(1)

def main():
    try:
        import mesa
    except ImportError:
        print ("Mesa has not been installed on your computer. To install run:\npip install mesa")

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



if __name__ == "__main__":
    main()
