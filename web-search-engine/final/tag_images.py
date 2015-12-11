from clarifai.client import ClarifaiApi

class imageTag(object):
  def __init__(self):
    self.input = open('items.json','r')
    self.result = open('tagged_info.json','wb')

  def image_tag(self):
    clarifai_api = ClarifaiApi()
    url_list = []
    
    while True:
      text = self.input.readline()
      if not text:
        break
      str = text[15:-3] 
      url_list.append(str)

    result = clarifai_api.tag_urls(url_list)
    #self.recordTagInfo(result)
    print result
    self.input.close()

  def recordTagInfo(self,result):
    for info in result:
      self.result.write(info)
    self.result.close()

abc = imageTag()
abc.image_tag()


