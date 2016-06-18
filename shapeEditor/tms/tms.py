import math

MAX_ZOOM_LEVEL = 10
TILE_WIDTH = 256
TILE_HEIGHT = 256

def _unitsPerPixel(zoomLevel):
	return 0.703125 / math.pow(2, zoomLevel)