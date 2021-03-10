import sys
from Collection import Ebay
from Initialization import driverStarter

driver = driverStarter.startDriver()
url_ebay_Electronics_Search = 'https://www.ebay.com/sch/i.html?_sacat=0&_udlo=&_udhi=&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=22747&_sop=12&_dmd=1&_fosrp=1&LH_ItemCondition=3&_nkw=electronics&_pgn=1'
driverStarter.effectiveGet(driver, url_ebay_Electronics_Search)
content = driver.page_source
# Encode & Decode the source data and decode again for string type only
readable_content = content.encode(sys.stdout.encoding, errors='replace').decode('utf-8', errors='ignore')
Ebay.getTheProducts_singleURL(readable_content, '')
