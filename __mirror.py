# --------------------------------------------------- #
# Author: SgtAlex
# Description: Battlefield 2 Modding tool
#
# This program mirrors the objects in the map
#  (flips content vertical and horizontally)
#
# The algorithm procedure is the following:
#
#   reads filename from commandline
#   if file exists, then
#       creates file: filename_mirror
#       for line in file
#           if (line contains ".absolutePosition"), then
#               mirror (line)
#           elif (line contains ".rotation"), then
#               line.X += 180
#           endif
#           write line into filename_mirror
#       endfor
#
#
#   func mirror(string line)
#       line.X = -line.X
#       line.Z = -line.Z
#
#
# It can process several files in a time:
#   python __mirror.py StaticObjects.con AmbientObjects.con Editor\Splines.con Editor\GamePlayObjects.con
#
# --------------------------------------------------- #

import os, sys

# --
# -
#
class Position:
    def __init__(self, line):
        self.base = line.strip().split(' ')[0]
        coords = line.strip().split(' ')[1]

        self.x = float(coords.split('/')[0])
        self.y = float(coords.split('/')[1])
        self.z = float(coords.split('/')[2])

        self.mirror()

    def __str__(self):
        return '%s %s/%s/%s\n' % (self.base, self.x, self.y, self.z)

    def mirror(self):
        self.x = -self.x
        self.z = -self.z

# --
# -
#
class Rotation(Position):
    def __init__(self, line):
        super().__init__(line)

    def mirror(self):
        self.x = self.x + 180


# --
# -
#
def parseFile(filename):
    output = ''
    hasEmptyRotation = False

    # read source file and mirror its objects
    fd = open(filename)
    for line in fd:
        if ('.absolutePosition' in line):
            obj = Position(line)
            output += str(obj)
            hasEmptyRotation = True
        elif ('.rotation' in line):
            obj = Rotation(line)
            output += str(obj)
            hasEmptyRotation = False
        elif (hasEmptyRotation):         # 0/0/0 rotations are skipped by editor
            obj = 'Object.rotation 180/0/0\n'
            output += str(obj)
            output += line
            hasEmptyRotation = False
        elif ('.AddControlPoint' in line):  # Splines.con
            obj = Position(line)
            output += str(obj)
        else:
            output += line
    fd.close()

    # write parsed content into new file
    outputFile = filename.replace('.con', '_mirrored.con')
    fd = open(outputFile, 'w')
    fd.write(output)
    fd.close()


# --
# -
#
def main(argv):
    argv.pop(0)     # remove script name from args

    for file in argv:
        parseFile(file)


# --
# -
#
if __name__ == "__main__":

    if (len(sys.argv) < 2):
        print ('Usage: __mirror.py filename_1 filename_2 ... filename_N')
        sys.exit(-1)
    else:
        main(sys.argv)
