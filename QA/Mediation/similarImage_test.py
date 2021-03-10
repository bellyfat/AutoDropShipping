import sys, time, Constances, SQLHandler
from Entities import GapProduct
from Collection import Ebay
from ImageSimilartion import ImageSimilartion

amazonImg = 'https://images-na.ssl-images-amazon.com/images/I/41WzHq0SkRL._AC_.jpg'
ebayImg_same_1 = 'https://i.ebayimg.com/images/g/zFEAAOSwvBFfd4f9/s-l500.jpg'
ebayImg_same_2 = 'https://i.ebayimg.com/images/g/Z8gAAOSwxLVbH-Gi/s-l500.jpg'
ebayImg_diffrent_but_similar = 'https://i.ebayimg.com/images/g/Z~MAAOSwhhJfL0Ff/s-l500.jpg'
ebayImg_diffrent_1 = 'https://i.ebayimg.com/images/g/HjYAAOSwTWNe2PPL/s-l500.jpg'
ebayImg_diffrent_2 = 'https://i.ebayimg.com/images/g/N0YAAOSwOhtfaetm/s-l500.jpg'
ebayImg_diffrent_3 = 'https://i.ebayimg.com/images/g/kJwAAOSwyKBfdFRl/s-l1600.jpg'
ebayImg_diffrent_4 = 'https://i.ebayimg.com/images/g/8fUAAOSwJwFdurLb/s-l500.jpg'
ebayImg_diffrent_5 = 'https://i.ebayimg.com/images/g/I4cAAOSwQhte16Xp/s-l500.jpg'
ebayImg_diffrent_6 = 'https://i.ebayimg.com/images/g/feEAAOSw~SNfBjyY/s-l500.jpg'

start = time.time()

ImageSimilartion.URL_to_PNG(amazonImg, 'AmazonImage')

ImageSimilartion.URL_to_PNG(ebayImg_same_1, 'EbayImage')
isImageSimilarAnswer = ImageSimilartion.isImageSimilar('AmazonImage', 'EbayImage')
print("Same 1 - " + str(isImageSimilarAnswer))
ImageSimilartion.deleteImage('EbayImage')

ImageSimilartion.URL_to_PNG(ebayImg_same_2, 'EbayImage')
isImageSimilarAnswer = ImageSimilartion.isImageSimilar('AmazonImage', 'EbayImage')
print("Same 2 - " + str(isImageSimilarAnswer))
ImageSimilartion.deleteImage('EbayImage')

ImageSimilartion.URL_to_PNG(ebayImg_diffrent_but_similar, 'EbayImage')
isImageSimilarAnswer = ImageSimilartion.isImageSimilar('AmazonImage', 'EbayImage')
print("diffrent_but_similar - " + str(isImageSimilarAnswer))
ImageSimilartion.deleteImage('EbayImage')

ImageSimilartion.URL_to_PNG(ebayImg_diffrent_1, 'EbayImage')
isImageSimilarAnswer = ImageSimilartion.isImageSimilar('AmazonImage', 'EbayImage')
print("diffrent - " + str(isImageSimilarAnswer))
ImageSimilartion.deleteImage('EbayImage')

ImageSimilartion.URL_to_PNG(ebayImg_diffrent_2, 'EbayImage')
isImageSimilarAnswer = ImageSimilartion.isImageSimilar('AmazonImage', 'EbayImage')
print("diffrent - " + str(isImageSimilarAnswer))
ImageSimilartion.deleteImage('EbayImage')

ImageSimilartion.URL_to_PNG(ebayImg_diffrent_3, 'EbayImage')
isImageSimilarAnswer = ImageSimilartion.isImageSimilar('AmazonImage', 'EbayImage')
print("diffrent - " + str(isImageSimilarAnswer))
ImageSimilartion.deleteImage('EbayImage')

ImageSimilartion.URL_to_PNG(ebayImg_diffrent_4, 'EbayImage')
isImageSimilarAnswer = ImageSimilartion.isImageSimilar('AmazonImage', 'EbayImage')
print("diffrent - " + str(isImageSimilarAnswer))
ImageSimilartion.deleteImage('EbayImage')

ImageSimilartion.URL_to_PNG(ebayImg_diffrent_5, 'EbayImage')
isImageSimilarAnswer = ImageSimilartion.isImageSimilar('AmazonImage', 'EbayImage')
print("diffrent - " + str(isImageSimilarAnswer))
ImageSimilartion.deleteImage('EbayImage')

ImageSimilartion.URL_to_PNG(ebayImg_diffrent_6, 'EbayImage')
isImageSimilarAnswer = ImageSimilartion.isImageSimilar('AmazonImage', 'EbayImage')
print("diffrent - " + str(isImageSimilarAnswer))
ImageSimilartion.deleteImage('EbayImage')

ImageSimilartion.deleteImage('AmazonImage')

end = time.time()
print("Avg time for process: " + str((end- start) / 9))
