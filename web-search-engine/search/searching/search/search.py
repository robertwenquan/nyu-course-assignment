from django.shortcuts import render
from django.http import HttpResponse
from BeautifulSoup import BeautifulSoup

import json
import socket
import jinja2


def view(request):
  """ the search engine query view """

  pagecontent = """
  <HTML>
    <HEAD>
      <TITLE>SEARCH ENGINE BY ROBERT and CAICAI</TITLE>
    </HEAD>

    <BR>
    <BR>
    <BR>
    <BR>
    <BR>

    <BODY>
      <DIV ALIGN="CENTER">
      <IMG SRC="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png" width="200" height="65">
      <BR>
      <FORM action="/search" method="get">
        <DIV ALIGN="CENTER">
        <input style="padding: 0px; margin: 0px; height:30px; width: 60%; outline: none; background: url(data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw%3D%3D) transparent;" maxlength="256" name="q" title="Search" type="text" value="">
        <br>
        <br>
        <input type="submit" style="padding: 0px; margin: 0px; height:60px; width: 100px" value="Submit">
        </DIV>
      </FORM>
      </DIV>
    </BODY>
  </HTML>
  """
  return HttpResponse(pagecontent)


def get_response(query):
  """ get server query response """

  clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  clientsocket.setblocking(1)
  clientsocket.connect(('localhost', 1124))
  clientsocket.send(query)

  data = clientsocket.recv(1024)
  while not '"END OF RESULT"' in data.strip():
    data += clientsocket.recv(1024)

  return data

def result(request):
  """ show the search result listing """

  query = request.GET.get('q', '')

  data = get_response(query)

  templateLoader = jinja2.FileSystemLoader(searchpath="/")
  templateEnv = jinja2.Environment(loader=templateLoader)

  TEMPLATE_FILE = "/home/robert_wen/robert/nyu-course-assignment/web-search-engine/search/searching/search/template.jinja"
  template = templateEnv.get_template(TEMPLATE_FILE)

  templateVars = { "title" : "Search Results",
                   "description" : "Search results for " + query,
                   "items" : data
                 }

  #outputText = template.render(templateVars)

  soup = BeautifulSoup(data)
  outputText = soup.prettify()

  return HttpResponse(outputText)

