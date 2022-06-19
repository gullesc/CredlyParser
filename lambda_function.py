
import requests
import json
from bs4 import BeautifulSoup


class badge:
  def __init__(self, certTitle, certIssuer, certURL):
    self.certTitle = certTitle
    self.certIssuer = certIssuer
    self.certURL = certURL


def lambda_handler(event, context):   
  url = "https://www.credly.com/users/" + event['person'] +"/badges"
  grab_page = requests.get(url)
  parse_page = BeautifulSoup(grab_page.text, "html.parser")
  badgeArray = parse_page.find_all("li", class_="data-table-row data-table-row-grid")
  resultArray = []

  for x in badgeArray:
      title = x.find("a")
      certificateTitle = title.get('title')
      img = x.find("img")
      certificateImageURL = img.get("src")
      issuer = x.find("div", class_="cr-standard-grid-item-content__subtitle")
      certificateIssuer = issuer.get_text(strip=True)
      jsonResult = {
                  'certTitle': certificateTitle.encode("ascii", "ignore").decode('utf-8'),
                  'certIssuer': certificateIssuer,
                  'certUrl': certificateImageURL
              }
      
      resultArray.append(jsonResult)

  #print(json.dumps(resultArray).replace("\\", ""))  
 

  return {
        'statusCode': 200,
        'body': json.dumps(resultArray).replace("\\", "")
    }
