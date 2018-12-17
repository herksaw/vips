# -*- coding: utf-8 -*-
"""
@author: CJR
"""

'''
main function
'''
import Vips
import winsound
import sys
import os
import subprocess
from urllib.parse import unquote

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second



urlList = ['https://paultan.org/2018/07/27/new-national-electric-vehicle-project-proposal-coming/',
"https://www.geckoandfly.com/20737/best-dash-cam-app-android/",
"http://www.proudduck.com/2018/07/the-mysterious-case-of-missing-pencils/",
"https://www.soyacincau.com/2018/07/27/samsung-galaxy-note9-malaysia-price-online-store/",
"http://www.janechuck.co/2018/01/dubai-must-do-list.html#.W11SOdIzarw",
"http://www.bangsarbabe.com/2018/05/a-letter-to-our-daughter.html",
"https://www.budiey.com/wak-doyok-keluar-pas-sertai-pan/",
"https://www.mywomenstuff.com/2018/07/dont-believe-everything-you-read-about-skincare/",
"http://www.placesandfoods.com/2018/07/deliciousbangsar.html",
#"http://cheeserland.com/2018/07/kamogawa-summer-2018/",
"https://barelysupermommy.com/2018/08/13/i-need-bf-advice/",
"http://www.beautyholicsanonymous.com/2016/10/smashed-first-10k/",
#"https://www.tommyooi.com/how-to-apply-canada-travel-visa-for-malaysians/",
"http://www.imafulltimemummy.com/post/2010/06/28/Walloping-the-King-of-all-Fruits.aspx",
"http://www.nisakay.com/2018/10/ufora-skincare-baru-di-pasaran-langkah.html",
"https://kclau.com/investment/rpgt-2019/",
"https://fourfeetnine.com/2018/10/23/to-the-mother-judging-another-mom-please-stop/",
"http://www.vkeong.com/eat/top-10-penang-curry-mee-klang-valley/",
"https://www.ammboi.com/tempat-menarik-di-kemboja/",
"http://www.eatdrink.my/kl/2018/11/27/puttin-on-a-ritzy-christmas-snapshot/",
"https://blog.miragestudio7.com/8-excellent-free-3d-model-websites-for-3d-studio-max/4168/#at_pco=smlre-1.0&at_si=5c051cec88e87d26&at_ab=per-2&at_pos=2&at_tot=4",
"http://www.rebeccasaw.com/the-entertainer-app-malaysia-buy-one-get-one-free-dining-offers/",
"http://www.emilyquak.com/2018/03/product-review-celmonze-signature.html",
"http://www.chanwon.com/2018/11/what-does-blogger-do-how-i-started.html",
#"http://www.malaysianflavours.com/2018/02/top-instagram-worthy-cafes-kl-pj-visit-2018.html",
"http://tziaaa.com/2017/10/06/maputi-whitening-cream/",
"https://www.malaysianfoodie.com/2018/11/michelin-star-chef-daniele-repetti-cicchetti-zenzero.html#.XAUgymgzarw",
"http://blog.malaysia-asia.my/2018/11/fox-world-theme-park-genting-malaysia.html",
"http://www.faizalfredley.com/2018/02/13/27-perkara-perlu-tahu-jika-travel-ke-norway-tips-info/",
"https://www.sunshinekelly.com/2018/12/the-coffee-bean-tea-leaf-2018-holiday-menu-beverages.html",
"http://kyspeaks.com/2018/12/01/ky-eats-hana-tei-japanese-restaurant-lucky-garden-bangsar/",
"https://www.timothytiah.com/2018/08/22/how-having-money-can-sometimes-make-you-more-sad/",
"http://kampungboycitygal.com/2018/11/hana-tei-japanese-restaurant-bangsar-kl/",
"https://ariffshah.com/airasia-vs-malindo-air/",
"http://www.j2kfm.com/merindy-restaurant-kampung-simee-ipoh-sar-kok-liew/",
"https://ccfoodtravel.com/2018/11/swiss-michelin-star-chef-andreas-caminada-st-regis-kl/",
"http://www.smallnhot.com/2018/11/w7-cosmetics-launch-signature-by-hill.html",
"https://hommes.my/lifestyle/stylish-speakers-for-creative-home-office/#.XAUiR2gzarw",
#"https://alwaystravelicious.com/2013/10/22/santorini-park-cha-am-hua-hin/",
"http://www.shaolintiger.com/2016/12/17/vlog002-how-to-install-a-nato-watch-strap-22mm-avi-8/",
"http://www.bubblynotes.com/2018/11/smart-junior-chefnow-every-kid-can-cook.html",
"http://www.street-love.net/2017/11/how-i-learned-to-be-in-peace-with-my-depression/",
"http://redmummy.com/2018/10/25/abang-17th/",
"http://www.sabrinatajudin.com/2015/02/my-dr-ko-skin-center-experience-for-my.html",
"http://www.jessytheklchic.com/2015/11/health-malaysia-public-goverment-dental.html",
"http://www.kimberlylow.com/2017/06/13/eyebrow-embroidery-huevicky-gorgeous-eyebrows/",
"http://www.ciklilyputih.com/p/pr-newswire.html?rkey=20181203MS88593&filter=11889",
"http://www.mrjocko.com/2018/11/20th-century-fox-genting-highland-mungkin-dibatalkan.html"
]
"""
urlList = ['https://www.kompasiana.com/paulodenoven/5b4ffab1caf7db4b58030b92/kontroversi-larangan-pemberian-pr',
'https://www.alodokter.com/cermat-memilih-produk-pembersih-bayi-yang-lembut-dan-bebas-iritasi',
'https://www.malaysiakini.com/news/436377',
'https://www.moretify.com/2018/07/%E8%BF%9E%E7%BB%AD%E5%8D%81%E5%B9%B4%E5%86%A0%E5%86%9B-airasia%E9%99%90%E6%97%B6%E4%BF%83%E9%94%80%E3%80%8C%E6%9C%BA%E7%A5%A8%E5%8F%AA%E8%A6%8110sen%E3%80%8D/',
'https://www.mysumber.com/saps.html',
'https://paultan.org/2018/07/27/new-national-electric-vehicle-project-proposal-coming/',
'https://beautifulnara.com/akaun-instagram-ini-kantoikan-beberapa-artis-popular-pakai-jenama-tiruan/',
'https://www.geckoandfly.com/20737/best-dash-cam-app-android/',
#'http://www.malaysiandigest.com/frontpage/282-main-tile/749798-secretaries-general-ordered-to-probe-possible-sabotage-against-govt.html',
'https://www.soyacincau.com/2018/07/27/samsung-galaxy-note9-malaysia-price-online-store/',
'https://www.budiey.com/wak-doyok-keluar-pas-sertai-pan/',
#'https://www.tommyooi.com/how-many-days-in-europe-cities/',
'https://www.mywomenstuff.com/2018/07/dont-believe-everything-you-read-about-skincare/',
'https://www.ammboi.com/tm-dan-tnb-batal-kerjasama-sediakan-internet-kelajuan-tinggi/',
'https://kclau.com/investment/ray-dalio/',
'http://www.chanwon.com/2018/07/diediemust-try-eyeliner.html',
'http://www.beautyholicsanonymous.com/2016/10/hylamide-c25/',
#'http://www.kenhuntfood.com/2018/07/home-by-martell-penang-rendezvous-2018.html',
'http://www.nisakay.com/2018/05/pastikan-ootd-post-anda-paling-meletop.html'
]
"""

url_list = [
    "https://www.schukat.com/schukat/schukat_cms_en.nsf/index/CMSDF15D356B046D53BC1256D550038A9E0?OpenDocument&wg=U1232&refDoc=CMS322921A477B31844C125707B0034EB15",
    "https://www.digikey.com/products/en/integrated-circuits-ics/embedded-fpgas-field-programmable-gate-array-with-microcontrollers/767",
    "https://www.nxp.com/products/processors-and-microcontrollers/arm-based-processors-and-mcus/lpc-cortex-m-mcus/lpc800-series-cortex-m0-plus-mcus:MC_71785",
    "https://global.epson.com/products_and_drivers/semicon/products/micro_controller/16bit/#ac01",
    "http://www.firmcodes.com/microcontrollers/8051-3/features-of-8051-microcontroller/",
    "https://www.engineersgarage.com/8051-microcontroller",
    "https://www.robotshop.com/en/microcontrollers.html",
    "https://www.electroncomponents.com/Integrated-Circuits/Microcontroller",
    "https://www.jameco.com/shop/keyword=Buy-Transistors",
    "https://www.allelectronics.com/category/793/transistors/1.html",
    "https://www.rohm.com/new-products-listing/?nodecode=2020&period=180",
    "https://www.futureelectronics.com/c/semiconductors/discretes--transistors--general-purpose-transistors/products"
]

def main(url):
    # vips = Vips.Vips(unquote("https://www.geckoandfly.com/23620/jpeg-compression-tool-batch-lossy-lossless-optimization/", encoding="utf-8"))
    vips = Vips.Vips(unquote(url, encoding="utf-8"))
    vips.setRound(1)
    vips.service()
    # sys.exit(0)
    #winsound.Beep(frequency, duration)

index = 11

main(url_list[index])

# for i in range(0, len(urlList)):
#     main(urlList[i])