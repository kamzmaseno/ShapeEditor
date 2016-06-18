from osgeo import ogr
from django.contrib.gis.geos.collections import MultiPolygon, MultiLineString
from shapeEditor.shared.models import AttributeValue

def ogr_type_to_geometry_mname(ogr_type):
    return {ogr.wkbUnknown : 'Unknown',
            ogr.wkbPoint : 'Point',
            ogr.wkbLineString : 'LineString',
            ogr.wkbPolygon : 'Polygon',
            ogr.wkbMultiPoint : 'MultiPoint',
            ogr.wkbMultiLineString : 'MultiLineString',
            ogr.wkbMultiPolygon : 'MultiPolygon',
            ogr.wkbGeometryCollection : 'GeometryCollection',
            ogr.wkbNone : 'None',
            ogr.wkbLinearRing : 'LinearRing'}.get(ogr_type)


def wrap_geos_Geometry(geometry):
    if geometry.geom_type == "Polygon":
        return MultiPolygon(geometry)
    elif geometry.geom_type == "LineString":
        return MultiLineString(geometry)
    else:
        return geometry

def calc_geometry_field(geometry_type):
    if geometry_type == "Polygon":
        return "geom_multipolygon"
    elif geometry_type == "LineString":
        return "geom_multilinestring"
    else:
        return "geom_" + geometry_type.lower()

def getOGRFeatureAttribute(attr, feature, encoding):
    attr_name = str(attr.name)
    if not feature.IsFieldSet(attr_name):
        return (True, None)

    needs_encoding = False
    if attr.type == ogr.OFTInteger:
        value = str(feature.GetFieldAsInteger(attr_name))

    elif attr.type == ogr.OFTIntegerList:
        value = repr(feature.GetFieldAsIntegerList(attr_name))
    elif attr.type == ogr.OFTReal:
        value = feature.GetFieldAsDouble(attr_name)
        value = "%*.*f" % (attr.width, attr.precision, value)
    elif attr.type == ogr.OFTRealList:
        values = feature.GetFieldAsDoubleList(attr_name)
        str_values = []
        for value in values:
            str_values.append("%*.*f" % (attr.width,attr.precision,value))
        value = repr(str_Values)
    

    elif attr.type == ogr.OFTString:
        value = feature.GetFieldAsString(attr_name)
        needs_encoding = True
    elif attr.type == ogr.OFTStringList:
        value = repr(feature.GetFieldAsStringList(attr_name))
        needs_encoding = True
    elif attr.type == ogr.OFTDate:
        parts = feature.GetFieldAsDateTime(attr_name)
        year,month,day,hour,minute,second,tzone = parts
        value = "%d,%d,%d,%d" % (year,month,day,tzone)
    elif attr.type == ogr.OFTTime:
        parts = feature.GetFieldAsDateTime(attr_name)
        year,month,day,hour,minute,second,tzone = parts
        value = "%d,%d,%d,%d" % (hour,minute,second,tzone)
    elif attr.type == ogr.OFTDateTime:
        parts = feature.GetFieldAsDateTime(attr_name)
        year,month,day,hour,minute,second,tzone = parts
        value = "%d,%d,%d,%d,%d,%d,%d,%d" % (year,month,day,hour,minute,second,tzone)
    else:
        return (False, "Unsupported attribute type: " + str(attr.type))
    if needs_encoding:
        try:
            value = value.decode(encoding)
        except UnicodeDecodeError:

            return (False, "Unable to decode value in " + repr(attr_name) + " attribute.&nbsp; " +
                    "Are you sure you're using the right " + "character encoding?")
    return (True, value)




































