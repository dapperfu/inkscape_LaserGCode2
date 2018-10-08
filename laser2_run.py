import sys

addpaths=[
    "/mnt/ubuntu1604_2/home/jed/.config/inkscape/extensions/InkscapeLaserGCode",
    "/usr/share/inkscape/extensions",
    "/opt/caffe/distribute/python",
    "/mnt/ubuntu1604_2/home/jed/.config/inkscape/extensions",
    "/usr/lib/python2.7",
    "/usr/lib/python2.7/plat-x86_64-linux-gnu",
    "/usr/lib/python2.7/lib-tk",
    "/usr/lib/python2.7/lib-old",
    "/usr/lib/python2.7/lib-dynload",
    "/mnt/ubuntu1604_2/home/jed/.local/lib/python2.7/site-packages",
    "/usr/local/lib/python2.7/dist-packages",
    "/usr/lib/python2.7/dist-packages",
    "/usr/lib/python2.7/dist-packages/gtk-2.0",
}
for addpath in addpaths:
    if addpath not in sys.path:
        sys.path.append(addpath)


