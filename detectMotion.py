import datetime
import numpy as np
import subprocess
import os
import cv2
import time
import requests


def motionDetection():
    token = os.environ['LINE_TOKEN']  #Line token
    motion_th = 1000          #Threshold for motion detection

    s_token = os.environ['SLACK_TOKEN'] #Slack token 

    while True:
        # retrieve time
        time2 = datetime.datetime.now()
        strtime = time2.strftime('%Y%m%d_%H:%M:%S')
        FileName = strtime + ".jpg"

        # image1 capture
        print("e1 start %s" %(strtime))
        cmd1 = 'fswebcam -r 640x480 --no-banner e1.jpg'
        ps1 = subprocess.run(cmd1.split(), stdout = subprocess.PIPE)

        # image2 capture
        print("e2 start %s" %(strtime))
        cmd2 = 'fswebcam -r 640x480 --no-banner e2.jpg'
        ps2 = subprocess.run(cmd2.split(), stdout = subprocess.PIPE)

        # motion detection
        img1 = cv2.imread('e1.jpg')
        img2 = cv2.imread('e2.jpg')

        # set background differences
        fgbg = cv2.createBackgroundSubtractorMOG2()   # create background object

        fgmask = fgbg.apply(img1)
        fgmask = fgbg.apply(img2)

        motion = cv2.countNonZero(fgmask)
        print('detected motion: %d' %(motion))

        if motion > motion_th:
            cv2.imwrite(FileName, img2)
            print('----Captured!----')

            payload = {'message': 'Motion detected'}   # send message
            url = 'https://notify-api.line.me/api/notify'
            headers = {'Authorization': 'Bearer ' + token}

            files = {'imageFile': open(FileName,'rb')}
            res = requests.post(url, data = payload, headers = headers, files = files,) # post to LINE Notify
            print('LINE',res)

            # slack 
            channel = os.environ['SLACK_CHANNEL']
            title = datetime.datetime(*time.localtime(os.path.getctime(FileName))[:6])
            files2 = {'file': open('e2.jpg', 'rb')}
            param = {
                'token': s_token,
                'channels': channel,
                'filename': 'my_picture.jpg',
                'initial_comment': 'posted picture.', 'title': title
            }
            # post to slack channel
            res2 = requests.post(url='https://slack.com/api/files.upload', params = param, files = files2,)
            print('slack',res2)

            # detected image
            cv2.imwrite('./diff.jpg', fgmask)

            time.sleep(10)
        else:
            pass
        
        # display
        #cv2.imshow('frame',fgmask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
