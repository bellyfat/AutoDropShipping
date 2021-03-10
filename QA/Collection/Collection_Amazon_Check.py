import sys
from Collection import Amazon
from Initialization import driverStarter

driver = driverStarter.startDriver()
url_amazon_vehicles = 'https://www.amazon.com/b/ref=s9_acss_bw_cg_TGCGDK_3d1_w?node=276729011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-15&pf_rd_r=FECH07WR2FC8EZYQK48Q&pf_rd_t=101&pf_rd_p=e7b0592f-ffeb-48c4-9453-25c721806001&pf_rd_i=165793011'
driverStarter.effectiveGet(driver, url_amazon_vehicles)
content = driver.page_source
# Encode & Decode the source data and decode again for string type only
readable_content = content.encode(sys.stdout.encoding, errors='replace').decode('utf-8', errors='ignore')
Amazon.getTheProducts_singleURL(readable_content, 'ToyCars')
