import httplib, urllib, base64, json

#def eye_aspect(cords):


def main():
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
    body = "{'url':'https://i.imgur.com/YfiguD0.jpg'}"

    try:
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        print(response)

        data = response.read()
        parsed = json.loads(data)
        xf = json.dumps(parsed, sort_keys=True, indent=2)
        #prin(xf)
        landmarks = parsed[0]["faceLandmarks"]

        eRT = landmarks["eyeRightTop"]
        eRB = landmarks["eyeRightBottom"]
        eLT = landmarks["eyeLeftTop"]
        eLB = landmarks["eyeLeftBottom"]
        print(eRB,eRT,eLB,eLT)
        aspectR =  (eRB['y']-eRT['y'])
        aspectL =  (eLB['y']-eLT['y'])
        print(aspectL,aspectR)          # check 1 on 4 before

        #print ("Response:")

        #print(parsed)
        #print(type(parsed))
        conn.close()

    except Exception as e:
        print("Check Image Url")
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__ == "__main__":
    main()
