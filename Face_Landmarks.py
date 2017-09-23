import httplib, urllib, base64, json

#def eye_aspect(cords):

from picamera import PiCamera
from datetime import datetime
import time
from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings

camera = PiCamera()

block_blob_service = BlockBlobService(account_name='irisdriving', account_key='xNhodNyQZdly5H/LcEVZxEUvS4e4yiXEDg+45Ybw114KxPswAz3vIHnfhfzkvwlLz2muqXl3DZI6cbXqptbb2Q==')

def imageCall():
    filename = "pircam-" +  datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")
    camera.capture(filename)
    print("picture taken")
    block_blob_service.create_blob_from_path(
    'pipictures',
    filename,
    filename,
    content_settings=ContentSettings(content_type='image/jpeg'))
    time.sleep(1)
    return "https://irisdriving.blob.core.windows.net/pipictures/pircam-" + filename


def main(img):
    subscription_key = '42f58775935b46e4a363bef2be2187dd'

    uri_base = 'westcentralus.api.cognitive.microsoft.com'

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
        }

    params = urllib.urlencode({
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'true',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
            })

            # The URL of a JPEG image to analyze.
    bag = ['jpg','JPG','png','PNG']
    body = "{'url':img}"


    try:
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')

        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        print(response)

        data = response.read()
        parsed = json.loads(data)
        xf = json.dumps(parsed, sort_keys=True, indent=2)
        #prin(xf)

        attr = parsed[0]["faceAttributes"]['emotion']
        glass_flag = parsed[0]["faceAttributes"]['glasses']        # check NoGlasses
        occ =  parsed[0]["faceAttributes"]['occlusion']['eyeOccluded']
        landmarks = parsed[0]["faceLandmarks"]

        if not occ :
            eRT = landmarks["eyeRightTop"]
            eRB = landmarks["eyeRightBottom"]
            eLT = landmarks["eyeLeftTop"]
            eLB = landmarks["eyeLeftBottom"]
            #print(eRB,eRT,eLB,eLT)

            aspectR =  (eRB['y']-eRT['y'])
            aspectL =  (eLB['y']-eLT['y'])
            print("Aspect Ratios Left and Right (T/B)")
            print(aspectL,aspectR)          # check 1 on 4 before
            print("Emotions")
            for at in attr.keys():
                print(str(at),attr[at])
            #print(occ)
            #print ("Response:")

            #print(parsed)
            #print(type(parsed))
            conn.close()
            return (aspectL,aspectR)
        else:
            print("You've probably got your glasses on , Please make sure you remove them and then submit your face samples.")
            return (-1,-1)
    except Exception as e:
        print("Check Image Url . ")
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def mainPic():
    li = []
    print("Take picture looking directly into the camera")
    time.sleep(3)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("Smile")
    li.append(imageCall())

    print("Take picture looking directly at the camera with your eyes closed")
    time.sleep(3)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("Smile")
    li.append(imageCall())

    print("Take picture looking directly at the camera with your eyes normal")
    time.sleep(3)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("Smile")
    li.append(imageCall())

    return li

def infi(refx,refy):
    while True:
        link = imageCall()
        x,y = main(link)
        print(x,y)
        if(x<refx or y<refy):
            print("GONE")
        time.sleep(1)


if __name__ == "__main__":
    li =  mainPic()
    print(li)
    x,y =  0 ,0
    for item in li:
        tmp  = main(item)
        if tmp == (-1,-1):
            print("FATAL")
            exit()
        x+=tmp[0]
        y+=tmp[1]
    refx=x//3
    refy=y//3
    print(refx,refy)
    infi(refx,refy)
