import sys, time, Constances, SQLHandler, cv2
from scipy.linalg import norm
from Entities import GapProduct, Amazon
from Collection import Ebay
from Mediation import byCrossReferencing
from Initialization import driverStarter
from PIL import Image
from ImageSimilartion import ImageSimilartion

print("True")
# 0.6666666666666666 True
print(byCrossReferencing.isNameSimilar('Roku Premiere | HD/4K/HDR Streaming Media Player, Simple Remote and Premium HDMI Cable',
                                    'Roku Premiere Version HD/4K/HDR Streaming Media Player W/Remote & HDMI Cable'))
# 0.6666666666666666 True
print(byCrossReferencing.isNameSimilar('Roku Premiere | HD/4K/HDR Streaming Media Player, Simple Remote and Premium HDMI Cable',
                                    'ROKU HD/4K/HDR Streaming - Simple Remote - Premium HDMI Cable - NEW & FREESHIP'))
# 0.5333333333333333 True
print(byCrossReferencing.isNameSimilar('Roku Premiere | HD/4K/HDR Streaming Media Player with Simple Remote and Premium HDMI Cable (Renewed), Black',
                                    'Roku Premiere Version HD/4K/HDR Streaming Media Player W/Remote & HDMI Cable'))
# 0.5333333333333333 True
print(byCrossReferencing.isNameSimilar('Roku Premiere | HD/4K/HDR Streaming Media Player with Simple Remote and Premium HDMI Cable (Renewed), Black',
                                    'ROKU HD/4K/HDR Streaming - Simple Remote - Premium HDMI Cable - NEW & FREESHIP'))
# True - 0.7857142857142857
amazonName = 'Hape Beaded Raindrops | Mini Wooden Musical Shake & Rattle Rainmaker Toy, Blue, Model Number: E0328B'
ebayName = 'Hape Beaded Raindrops | Mini Wooden Musical Shake & Rattle Rainmaker Toy Blue...'
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
# True - 0.7142857142857143
amazonName = "GETIANLAI Wooden Educational Preschool Toddler Toys Shape Color Sorting Block Puzzles for Boys & Girls"
ebayName = "GETIANLAI Wooden Educational Preschool Toddler Toys Shape Color Sorting Block..."
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
# True - 0.7142857142857143
amazonName = "GETIANLAI Wooden Educational Preschool Toddler Toys Shape Color Sorting Block Puzzles for Boys & Girls"
ebayName = "GETIANLAI Wooden Educational Preschool Toddler Toys Shape Color Sorting Block Pu"
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
# True - 0.7142857142857143
amazonName = "Fisher-Price Laugh & Learn Smart Stages Puppy"
ebayName = "Laugh & Learn Smart Stages Puppy"
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
# True - 0.5263157894736842
amazonName = '18 Inch Doll Furniture Fits 18" American Girl Dolls - Floral Doll Table and Chairs Set for My Life Dolls'
ebayName = '18" Doll Furniture Wooden Table and Chair Set Fits American Girl Dolls Age 3'
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
# True - 0.42857142857142855
amazonName = 'Skyrocket Blume Doll - Add Water & See Who Grows'
ebayName = 'Blume Doll Toys Add Water See Toy Grows Surprises Fashion Sticker Series 1 3'
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
# True - 0.0
amazonName = 'Jamohom Wooden Puzzles for Toddlers, 2 Pack Chunky Wooden Peg Board Alphabet Puzzles with Colorful Fruit Animal Vegetables Pattern, Educational Learning Toy for Kids Age 1-4.'
ebayName = '2 Sets Wooden Number Puzzle and Alphabet Puzzle Set Early Educational Board Toys'
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
print("False")
# 0.0 False
print(byCrossReferencing.isNameSimilar('NEOWOWS Kids Crafts and Arts Supplies Set Painting Kit Decorate Your Own Dinosaur Figurines DIY Dinosaur Arts Crafts 3D Painting Dinosaurs Toys for Kids Boys Girls Age 4 5 6 7 8 Years Old',
                                    'TOYS FOR KIDS GIRLS BOYS Toddler Gift Educational Toys For 3 4 5 6 7 Years Old'))
# 0.0 False
print(byCrossReferencing.isNameSimilar('NEOWOWS Kids Crafts and Arts Supplies Set Painting Kit Decorate Your Own Dinosaur Figurines DIY Dinosaur Arts Crafts 3D Painting Dinosaurs Toys for Kids Boys Girls Age 4 5 6 7 8 Years Old',
                                    'Educational Developing Activity Toys Kids Age 3 4 5 6 7 8 Years old Boys Girls'))
# 0.0 False
print(byCrossReferencing.isNameSimilar('NEOWOWS Kids Crafts and Arts Supplies Set Painting Kit Decorate Your Own Dinosaur Figurines DIY Dinosaur Arts Crafts 3D Painting Dinosaurs Toys for Kids Boys Girls Age 4 5 6 7 8 Years Old',
                                    'Kids Creative Learning Educational Toys for Age 3 4 5 6 7 8 Years Old Boys Girls'))
# 0.0 False
print(byCrossReferencing.isNameSimilar('KellyToy Llama 16" Plush Animal Tan Got Llama Love For You Stuffed Animal New',
                                    'Douglas Llamacorn Llama Unicorn Plush Stuffed Animal'))
# False - 0.0
amazonName = "GETIANLAI Wooden Educational Preschool Toddler Toys Shape Color Sorting Block Puzzles for Boys & Girls"
ebayName = "Wooden Educational Preschool Toddler Toys For 1 2 3 4 5 Year Old Boys Girls US"
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
# False - 0.0
amazonName = "GETIANLAI Wooden Educational Preschool Toddler Toys Shape Color Sorting Block Puzzles for Boys & Girls"
ebayName = "Wooden Sorting & Stacking Toys for Toddlers Educational Shape Color Recognition"
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
# False - 0.0
amazonName = "GETIANLAI Wooden Educational Preschool Toddler Toys Shape Color Sorting Block Puzzles for Boys & Girls"
ebayName = "Wooden Educational Toys For Toddlers Preschool Shape Color Sorting Stacking Geom"
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
# False - 0.0
amazonName = "Baby Alive Classic Doll Pram"
ebayName = "Baby Doll Accessories Baby Doll Swing, Baby Doll High Chair, Doll Carrier (4PC)"
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
# False - 0.0
amazonName = 'Dress Up America Pretend Play Costumes - Role-Play and Dress-Up for Kids'
ebayName = '23Pcs Education For Kids Fun Learning Toys For Children Kids Pretend Role Play K'
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
# False - 0.0
amazonName = 'Disney Baby Classic Piglet Stuffed Animal Plush Toy, 9 inches '
ebayName = '14" Pink Stuffed Dinosaur Plush Toy, Plush Dinosaur Stuffed Animal, Dinosaur Toy'
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
# False - 0.0
amazonName = 'Litti Pritti Baby Doll Stroller for Toddlers - Baby Stroller for Dolls with Basket'
ebayName = 'Baby Doll Accessories Baby Doll Swing, Baby Doll High Chair, Doll Carrier (4PC)'
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
# False - 0.0
amazonName = 'Disney Baby Toy Story Buzz Lightyear On The Go Activity Toy'
ebayName = 'Disney Baby Minnie Mouse On The Go Activity Toy Christmas Teether Chime'
print(byCrossReferencing.isNameSimilar(amazonName, ebayName))
