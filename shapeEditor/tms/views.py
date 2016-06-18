from django.shortcuts import render
from django.http import HttpResponse
import traceback,mimetypes
from django.http import Http404
from shapeEditor.shared.models import Shapefile

def root(request):
    try:
    	baseURL = request.build_absolute_uri()
    	xml = []
    	xml.append('<?xml version="1.0" encoding="utf-8" ?>')
    	xml.append('<Services>')
    	xml.append(' <TileMapService ' + 'title="ShapeEditor Tile Map Service" ' +'version="1.0" href="' + baseURL + '/1.0"/>')
    	xml.append('</Services>')
    	return HttpResponse("\n".join(xml), content_type="text/xml")

    except:
    	traceback.print_exc()
    	return HttpResponse("Error")
def service(request, version):
    try:
        if version != "1.0":
            raise Http404

        baseURL = request.build_absolute_uri()
        xml = []
        xml.append('<?xml version="1.0" encoding="utf-8" ?>')
        xml.append('<TileMapService version="1.0" services="' +
			        baseURL + '">')
        xml.append(' <Title>ShapeEditor Tile Map Service' +
                   '</Title>')
        xml.append('<Abstract></Abstract>')
        xml.append(' <TileMaps>')
        for shapefile in Shapefile.objects.all():
            id = str(shapefile.id)
            xml.append('<TileMap title="' +shapefile.filename + '"')
            xml.append('srs="EPSG:4326"')
            xml.append('href="'+baseURL+'/'+id+'"/>')
        xml.append(' </TileMaps>')
        xml.append('</TileMapService>')
        return HttpResponse("\n".join(xml), content_type="text/xml")
    except:
        traceback.print_exc()
        return HttpResponse("Error")

def tileMap(request, version, shapefile_id):
    if version != "1.0":
        raise Http404

    try:
        shapefile = shapefile.objects.get(id=shapefile_id)
    except shapefile.DoesNotExist:
        raise Http404

    try:
        baseURL = request.build_absolute_uri()
        xml = []
        xml.append('<?xml version="1.0" encoding="utf-8" ?>')
        xml.append('<TileMap version="1.0" ' + 'tilemapservice="' + baseURL + '">')
        xml.append(' <Title>' + shapefile.filename + '</Title>')
        xml.append(' <Abstract></Abstract>')
        xml.append(' <SRS>EPSG:4326</SRS>')
        xml.append(' <BoundingBox minx="-180" miny="-90" ' + 'maxx="180" maxy="90"/>')
        xml.append(' <Origin x="-180" y="-90"/>')
        xml.append(' <TileFormat width="' + str(TILE_WIDTH) + '" height="' + str(TILE_HEIGHT) + '" ' + 'content_type="image/png" extension="png"/>')
        xml.append(' <TileSets profile="global-geodetic">')
        for zoomLevel in range(0, MAX_ZOOM_LEVEL+1):
            unitsPerPixel = _unitsPerPixel(zoomLevel)
            xml.append('<TileSet href="' + baseURL + '/' + str(zoomLevel) + '" units-per-pixel="'+str(unitsPerPixel) + '" order="' + str(zoomLevel) + '"/>')


        xml.append(' </TileSets>')
        xml.append('</TileMap>')
        return HttpResponse("\n".join(xml), content_type="text/xml")
    except:
        traceback.print_exc()
        return HttpResponse("Error")
def tile(request, version, shapefile_id, zoom, x, y):
    return HttpResponse("Tile")
