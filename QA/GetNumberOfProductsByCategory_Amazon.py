from StoreUploading import availableProduct
from Initialization import driverStarter

'''
# Initialize
driver = driverStarter.startDriver()
# Ebay
Ebay_NotPersonalSite = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=a&_sacat=0'
Ebay_incorrectUrl = 'https://www.ebay.com/itm/My-Pillow-Pets-Trolls-World-Tour-Poppy-16-Plush-DreamWorks-World-Tour-NEW/203131168693?hash=item2f4b8fa7b5%3Ag%3Am74AAOSw7blffRys&amp;LH_ItemCondition=1000'
Ebay_freeShippingUrl = 'https://www.ebay.com/p/13033697075?iid=154105371641'
Ebay_notFreeShippingUrl_1 = 'https://www.ebay.com/p/1910229201?_trkparms=aid%3D333200%26algo%3DCOMP.MBE%26ao%3D1%26asc%3D20170706093515%26meid%3D458d871f4aa44fc8a3f62c40154f7de7%26pid%3D100831%26rk%3D2%26rkt%3D3%26itm%3D114178601582%26pmt%3D0%26noa%3D1%26pg%3D2322090%26algv%3DProductBundlingV6%26brand%3DAmerican+Girl&_trksid=p2322090.c100831.m5025&iid=114178601582'
Ebay_notFreeShippingUrl_2 = 'https://www.ebay.com/p/25034587357'
urls_Ebay = [Ebay_incorrectUrl, Ebay_freeShippingUrl, Ebay_notFreeShippingUrl_1, Ebay_notFreeShippingUrl_2]
# Amazon
Amazon_correctUrl = 'https://www.amazon.com/WolVol-Electric-Flash-Light-Train/dp/B00FKFLQKI'
Amazon_incorretUrl = 'https://www.amazon.com//gp/slredirect/picassoRedirect.html/ref=pa_sp_btf_toys-and-games_sr_pg132_1?ie=UTF8&amp;adId=A01600801GVDVB5VJ8IQO&amp;url=%2FWolVol-Electric-Flash-Light-Train%2Fdp%2FB00FKFLQKI%2Fref%3Dsr_1_3175_sspa%3Fdchild%3D1%26keywords%3Dsteam%2Btoys%26qid%3D1601976460%26s%3Dtoys-and-games%26sr%3D1-3175-spons%26psc%3D1&amp;qualifier=1601976459&amp;id=4001836270984246&amp;widgetName=sp_btf'
name = 'WolVol Bump &amp; Go Electric Flash Light Train Toy with Music'
img = 'https://m.media-amazon.com/images/I/71gV1n8hMIL._AC_UL320_.jpg'
urls_Amazon = [Amazon_correctUrl, Amazon_incorretUrl]
# Test - Ebay
for url in urls_Ebay:
    driverStarter.effectiveGet(driver, url)
    isPersonal = availableProduct.checkIfPersonalSite_Ebay(driver)
    if isPersonal:
        # Checking the shipping details and options
        shipping = availableProduct.checkShippingEbay(driver) # A browser must be open before with the appropriate site
        print(shipping)
    else: print("Not personal site")
# Test - Amazon
for url in urls_Amazon:
    driverStarter.effectiveGet(driver, url)
    isCorrect_Amazon = availableProduct.checkIfPersonalSite_Amazon(driver)
    if isCorrect_Amazon == False:
        newHref = availableProduct.getTheCorrectSite_Amazon(driver, name, img)
        print(newHref)
'''
availableProduct.checkGapProducts() # AMAZON STORE PROBLEM!
