from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def view(request):
  pagecontent = """
  <HTML>
    <HEAD>
      <TITLE>SEARCH ENGINE BY ROBERT and CAICAI</TITLE>
    </HEAD>

    <BODY>
      <DIV ALIGN="CENTER">
      <IMG SRC="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png" width="200" height="65">
      <FORM action="/search" method="get">
        <DIV ALIGN="CENTER">
        <input style="padding: 0px; margin: 0px; height:30px; width: 60%; outline: none; background: url(data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw%3D%3D) transparent;" maxlength="256" name="q title="Search" type="text" value="">
        </DIV>
      </FORM>
      </DIV>
    </BODY>
  </HTML>
  """
  return HttpResponse(pagecontent)

def result(request):
  return HttpResponse('sdfsdfd')

