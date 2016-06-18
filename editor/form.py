from django import forms

CHARACTER_ENCODINGS = [("ascii","ASCII"),
                       ("latin1", "Latin-1"),
                       ("utf8", "UTF-8")]


class ImportShapefileForm(forms.Form):
	shapefile = forms.FileField(label="select a Zipped Shapefile")
	character_encoding = forms.ChoiceField(choices=CHARACTER_ENCODINGS, initial="utf8")