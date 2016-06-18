from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from shapeEditor.shared.models import Shapefile
from editor.form import ImportShapefileForm
from shapeEditor.shapefileIO import importer

def list_shapefiles(request):
    shapefiles = Shapefile.objects.all().order_by("filename")
    return render(request, "list_shapefiles.html",{'shapefiles' : shapefiles})


def import_shapefile(request):

    if request.method == "GET":
        form = ImportShapefileForm()
        return render(request,"import_shapefile.html",{'form' :form,
                                                       'err_msg' :None }
                                                       )


    elif request.method == "POST":
        form = ImportShapefileForm(request.POST,request.FILES)
        if form.is_valid():
            shapefile = request.FILES['shapefile']
            encoding = request.POST['character_encoding']

            err_msg = importer.import_data(shapefile,encoding)

            if err_msg == None:
                return HttpResponseRedirect("/shape-editor")
        else:
            err_msg = None

        return render(request, "import_shapefile.html",
                  {'form' : form,
                   'err_msg' : err_msg})