import xml.etree.ElementTree as ET
import os
from pyanvileditor import world
import qrcode
import qrcode.image.svg
import json
import argparse

def createQR(content, filename="qr.svg"):
    img = qrcode.make(content, image_factory=qrcode.image.svg.SvgImage)
    img.save(filename)
    return filename

def getQRArray(filename="qr.svg"):
    tree = ET.parse(filename)
    root = tree.getroot()
    width = int(root.attrib["width"].replace("m",""))
    height = int(root.attrib["height"].replace("m",""))
    matrix = []
    for i in range(width+1):
        matrix.append([0]*height)

    for child in root:
        x = int(child.attrib["x"].replace("m",""))
        y = int(child.attrib["y"].replace("m",""))
        matrix[x][y] = 1

    return matrix

def placeQR(matrix,savefolder,xoffset,yoffset,height,light,dark):
    with world.World(savefolder) as mcworld:
        nx = 0
        for x in matrix:
            ny = 0
            for y in x:
                blockpos = (nx+xoffset, height, ny+yoffset)
                block = mcworld.get_block(blockpos)
                if y == 1:
                    block.set_state(world.BlockState(dark, {}))
                else:
                    block.set_state(world.BlockState(light, {}))
                ny += 1
            nx += 1


parser = argparse.ArgumentParser(description="Add QR-Code to Minecraft-world")
parser.add_argument("-c", "--content", help="Content of the QR-Code", required=True)
parser.add_argument("-s", "--savegame", help="Path to the MC-Savegame", required=True)
parser.add_argument("-x", "--xoffset", help="Offset (starting point) for the x-coordinate", type=int, default=0)
parser.add_argument("-y", "--yoffset", help="Offset (starting point) for the y-coordinate", type=int, default=0)
parser.add_argument("-z", "--height", help="Level (height) of the QR-Code", type=int, default=100)
parser.add_argument("-l", "--light", help="Block-ID for the light / white blocks", type=str, default="minecraft:iron_block")
parser.add_argument("-d", "--dark", help="Block-ID for the dark / black blocks", type=str, default="minecraft:obsidian")
args = parser.parse_args()

createQR(args.content)
placeQR(getQRArray(),args.savegame,args.xoffset,args.yoffset,args.height,args.light,args.dark)
print("Pasted QR-Code into world")
