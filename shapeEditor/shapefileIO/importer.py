import os, os.path, tempfile, zipfile
import shutil, traceback

from osgeo import ogr
from shapeEditor.shared.models import Shapefile
from shapeEditor.shared import utils
from shapeEditor.shared.models import Attribute
from django.contrib.gis.geos.geometry import GEOSGeometry
from osgeo import osr
from shapeEditor.shared.models import Feature


def import_data(shapefile, character_encoding):

    fd, fname = tempfile.mkstemp(suffix=".zip")
    os.close(fd)

    f = open(fname, 'w+b')
    for chunk in shapefile.chunks():
    	f.write(chunk)
    f.close

    if not zipfile.is_zipfile(fname):
    	os.remove(fname)
    	return "Not a valid zip archive."

    zip = zipfile.ZipFile(fname)
    required_suffixes = [".shp",".dbf",".prj"]

    has_suffix = {}
    for suffix in required_suffixes:
     	has_suffix[suffix] = False

    for info in zip.infolist():
     	extension = os.path.splitext(info.filename)[1].lower()
     	if extension in required_suffixes:
     		has_suffix[extension] = True

    for suffix in required_suffixes:
     	if not has_suffix[suffix]:
     		zip.close()
     		os.remove(fname)
     		return "Archive missing required "+suffix+" file."

    shapefile_name = None
    dst_dir = tempfile.mkdtemp()
    for info in zip.infolist():
        if info.filename.endswith(".shp"):
            shapefile_name = info.filename
        dst_file = os.path.join(dst_dir, info.filename)
        f = open(dst_file, "wb")
        f.write(zip.read(info.filename))
        f.close()
    zip.close()


    try:
        datasource = ogr.Open(os.path.join(dst_dir, shapefileName))
        layer = datasource.GetLayer(0)
        shapefileOK = True

    except:
        traceback.print_exc()
        shapefileOK = False

    if not shapefileOK:
        os.remove(fname)
        shutil.rmtree(dst_dir)
        return "Not a valid shapefile."


    src_spatial_ref = layer.GetSpatialRef()
    geometry_type = layer.GetLayerDefn().GetGeomType()
    geometry_name = utils.ogr_type_to_geometry_name(geometry_type)
    shapefile = Shapefile(filename=shapefile_name, srs_wkt=src_spatial_ref.ExportToWkt(), geom_type=geometry_name, encoding=character_encoding)
    shapefile.save()


    #defining the shapefile's attributes

    attributes = []
    layer_def = layer.GetLayerDefn()
    for i in range(layer_def.GetFieldCount()):
        field_def = layer_def.GetFieldDefn(i)
        attr = Attribute(shapefile=shapefile,
                         name=field_def.GetName(),
                         type=field_def.GetType(),
                         width=field_def.GetWidth(),
                         precision=field_def.GetPrecision())

    attr.save()
    attributes.append(attr)


    #store the shapefile's features

    dst_spatial_ref = osr.SpatialReference()
    dst_spatial_ref.ImportFromEPSG(4326)
    coord_transform = osr.CoordinateTransformation(src_spatial_ref,dst_spatial_ref)
    for i in range(layer.GetFeatureCount()):
        src_feature = layer.GetFeature(i)
        src_geometry = src_feature.GetGeometryRef()
        src_geometry.Transform(coord_transform)
        geometry = GEOSGeometry(src_geometry.ExportToWkt())



    geometry = utils.wrap_geos_geometry(geometry)
    geometry_field = utils.calc_geometry_field(geometry_name)

    args = {}
    args['shapefile'] = shapefile
    args[geometry_field] = geometry
    feature = Feature(**args)
    feature.save()


    for attr in attributes:
        success,result = utils.getOGRFeatureAttribute(attr, srcFeature,character_encoding)
        if not success:
            os.remove(fname)
            shutil.rmtree(dst_dir)
            shapefile.delete()
            return result
        attr_value = AttributeValue(feature=feature,attribute=attr,value=result)

        attr_value.save()

    os.remove(fname)
    shutil.rmtree(dst_dir)
    return None
