import cv2 as cv2
import math


class Target:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow("Target", 1)
        cv2.namedWindow("Threshold1",1)
        cv2.namedWindow("Threshold2",1)
        cv2.namedWindow("hsv",1)
     
    def run(self):
        font = cv2.initFont(cv2.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)
        hsv_img=cv2.createImage(cv2.GetSize(cv2.QueryFrame(self.capture)),8,3)
        threshold_img1 = cv2.CreateImage(cv2.GetSize(hsv_img),8,1)
        threshold_img1a = cv2.CreateImage(cv2.GetSize(hsv_img),8,1)
        threshold_img2 = cv2.CreateImage(cv2.GetSize(hsv_img),8,1)
        i=0
        writer=cv2.CreateVideoWriter("angle_tracking.avi",cv2.CV_FOURCC('M','J','P','G'),30,cv2.GetSize(hsv_img),1)

        while True:
            img=cv2.QueryFrame(self.capture)

            cv2.CvtColor(img,hsv_img,cv2.CV_BGR2HSV)

            cv2.InRangeS(hsv_img,(165,145,100),(250,210,160),threshold_img1)
            cv2.InRangeS(hsv_img,(0,145,100),(10,210,160),threshold_img1a)
            cv2.Add(threshold_img1,threshold_img1a,threshold_img1)
            cv2.InRangeS(hsv_img,(105,180,40),(120,260,100),threshold_img2)


            threshold_img1=cv2.GetMat(threshold_img1)
            threshold_img2=cv2.GetMat(threshold_img2)
            moments1=cv2.Moments(threshold_img1,0)
            moments2=cv2.Moments(threshold_img2,0)
            area1=cv2.GetCentralMoment(moments1,0,0)
            area2=cv2.GetCentralMoment(moments2,0,0)
             
            x1,y1,x2,y2=(1,2,3,4)
            coord_list=[x1,y1,x2,y2]
            for x in coord_list:
                x=0
             
            if (area1 >200000):
                x1=int(cv2.GetSpatialMoment(moments1,1,0)/area1)
                y1=int(cv2.GetSpatialMoment(moments1,0,1)/area1)

                cv2.Circle(img,(x1,y1),2,(0,255,0),20)
                cv2.PutText(img,str(x1)+","+str(y1),(x1,y1+20),font, 255)

            if (area2 >100000):
                x2=int(cv2.GetSpatialMoment(moments2,1,0)/area2)
                y2=int(cv2.GetSpatialMoment(moments2,0,1)/area2)

                cv2.Circle(img,(x2,y2),2,(0,255,0),20)

                cv2.PutText(img,str(x2)+","+str(y2),(x2,y2+20),font, 255)
                cv2.Line(img,(x1,y1),(x2,y2),(0,255,0),4,cv2.CV_AA)
                cv2.Line(img,(x1,y1),(cv2.GetSize(img)[0],y1),(100,100,100,100),4,cv2.CV_AA)
            x1=float(x1)
            y1=float(y1)
            x2=float(x2)
            y2=float(y2)
            angle = int(math.atan((y1-y2)/(x2-x1))*180/math.pi)
            cv2.PutText(img,str(angle),(int(x1)+50,(int(y2)+int(y1))/2),font,255)

            cv2.WriteFrame(writer,img)

          
            cv2.ShowImage("Target",img)
            cv2.ShowImage("Threshold1",threshold_img1)
            cv2.ShowImage("Threshold2",threshold_img2)
            cv2.ShowImage("hsv",hsv_img)
            c = cv2.WaitKey(7) % 0x100
            if c == 27 or c == 10:
                break
        cv2.DestroyAllWindows()
             
if __name__=="__main__":
    t = Target()
    t.run()