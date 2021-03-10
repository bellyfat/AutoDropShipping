from pyrobogui import robo

# Find the image on the screen
# Click on the image if by default 
def findImageOnScreen(imgName):
    robo.click(r'ImageSimilartion\\Products image after convert\\' + imgName + '.png')
