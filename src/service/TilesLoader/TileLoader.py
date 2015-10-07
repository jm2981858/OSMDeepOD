import httplib2
from StringIO import StringIO
from PIL import Image
from src.base.Tile import Tile
from src.base.Bbox19 import Bbox19


class TileLoader:
    # http://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial/
    # ?mapArea=47.366177501999516,8.54279671719532,47.36781249586627,8.547088251618977
    # &key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq

    def __init__(self):
        self.PRELINK = "http://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial/?mapArea="
        self.POSTLINK = "&key=Asc0mfX_vbDVHkleWyc85z1mRLrSfjqHeGJamZsRF-mgzR4_GAlU31hkwMOGN4Mq"

    def download(self, bbox):
        url = self.PRELINK + bbox.getBingFormat() + self.POSTLINK
        resp, content = httplib2.Http().request(url)
        image = Image.open(StringIO(content))
        return Tile(image,bbox)

    def download19(self,bbox):
        result = []
        bboxes19 = Bbox19.toBbox19(bbox)
        for y in range(len(bboxes19)):
            result.append([])
            for x in range(len(bboxes19[y])):
                box = bboxes19[y][x]
                tile = self.download(box)
                result[y].append(tile)
        return result
