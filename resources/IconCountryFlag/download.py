import requests

arr = [
    "https://valar-sms.com/static/media/CN.e9b8b9a7.svg",
    "https://valar-sms.com/static/media/FI.0fec362e.svg",
    "https://valar-sms.com/static/media/DO.52e5ffa9.svg",
    "https://valar-sms.com/static/media/IL.4c50fabf.svg",
    "https://valar-sms.com/static/media/MV.8523a608.svg",
    "https://valar-sms.com/static/media/GH.d80d3a38.svg",
    "https://valar-sms.com/static/media/PR.5d0cd34a.svg",
    "https://valar-sms.com/static/media/BB.b48a77a7.svg",
    "https://valar-sms.com/static/media/BO.71f40e98.svg",
    "https://valar-sms.com/static/media/MZ.b6551397.svg",
    "https://valar-sms.com/static/media/SZ.7e07633c.svg",
    "https://valar-sms.com/static/media/TZ.15fc3a0e.svg",
    "https://valar-sms.com/static/media/VE.ae450ebc.svg",
    "https://valar-sms.com/static/media/CF.35d287ac.svg",
    "https://valar-sms.com/static/media/DZ.586a49b6.svg",
    "https://valar-sms.com/static/media/YE.9920a427.svg",
    "https://valar-sms.com/static/media/PH.065ff3fc.svg",
    "https://valar-sms.com/static/media/TG.8cd53002.svg",
    "https://valar-sms.com/static/media/HT.2756e1ea.svg",
    "https://valar-sms.com/static/media/IR.3e952031.svg",
    "https://valar-sms.com/static/media/SY.f5f0fa9d.svg",
    "https://valar-sms.com/static/media/MN.f31fa7e7.svg",
    "https://valar-sms.com/static/media/BE.549c0b45.svg",
    "https://valar-sms.com/static/media/BM.307e5dac.svg",
    "https://valar-sms.com/static/media/KE.56f17b15.svg",
    "https://valar-sms.com/static/media/NP.1f767153.svg",
    "https://valar-sms.com/static/media/ML.97236722.svg",
    "https://valar-sms.com/static/media/GT.56d82081.svg",
    "https://valar-sms.com/static/media/RU.059fe2c2.svg",
    "https://valar-sms.com/static/media/LK.348a89d8.svg",
    "https://valar-sms.com/static/media/NG.f07538c4.svg",
    "https://valar-sms.com/static/media/UG.90d250ad.svg",
    "https://valar-sms.com/static/media/PL.093e1c48.svg",
    "https://valar-sms.com/static/media/VN.54aee0f5.svg",
    "https://valar-sms.com/static/media/OM.3ec57fe0.svg",
    "https://valar-sms.com/static/media/TN.95b4bb25.svg",
    "https://valar-sms.com/static/media/JO.cc84fd0e.svg",
    "https://valar-sms.com/static/media/BH.62547ef7.svg",
    "https://valar-sms.com/static/media/UY.1aa23617.svg",
    "https://valar-sms.com/static/media/LT.4852482a.svg",
    "https://valar-sms.com/static/media/PG.3661f805.svg",
    "https://valar-sms.com/static/media/JM.030bbb1c.svg",
    "https://valar-sms.com/static/media/HN.2ad12e32.svg",
    "https://valar-sms.com/static/media/EE.67f12303.svg",
    "https://valar-sms.com/static/media/AE.953d102d.svg",
    "https://valar-sms.com/static/media/ZW.21158d0f.svg",
    "https://valar-sms.com/static/media/PA.a46901a7.svg",
    "https://valar-sms.com/static/media/NI.88a422be.svg",
    "https://valar-sms.com/static/media/CG.7d199acd.svg",
    "https://valar-sms.com/static/media/KG.c6da8f13.svg",
    "https://valar-sms.com/static/media/LC.ccf80c75.svg",
    "https://valar-sms.com/static/media/KH.3383e0ed.svg",
    "https://valar-sms.com/static/media/ID.7f88510e.svg",
    "https://valar-sms.com/static/media/BG.59cab6a3.svg",
    "https://valar-sms.com/static/media/CK.e09d5325.svg",
    "https://valar-sms.com/static/media/SV.d93deb05.svg",
    "https://valar-sms.com/static/media/TR.5ea73590.svg",
    "https://valar-sms.com/static/media/IQ.5c5eaf7d.svg",
    "https://valar-sms.com/static/media/DE.22d50712.svg",
    "https://valar-sms.com/static/media/LY.deefebe6.svg",
    "https://valar-sms.com/static/media/LS.2fc136a8.svg",
    "https://valar-sms.com/static/media/MD.b465393e.svg",
    "https://valar-sms.com/static/media/SN.daa49c16.svg",
    "https://valar-sms.com/static/media/BR.738779c2.svg",
    "https://valar-sms.com/static/media/NZ.d398b19d.svg",
    "https://valar-sms.com/static/media/PT.e6dd16cc.svg",
    "https://valar-sms.com/static/media/SK.3d1c655f.svg",
    "https://valar-sms.com/static/media/GY.35d8d606.svg",
    "https://valar-sms.com/static/media/MY.f8b9607e.svg",
    "https://valar-sms.com/static/media/LA.b12b616c.svg",
    "https://valar-sms.com/static/media/BD.8bd2ff19.svg",
    "https://valar-sms.com/static/media/AR.fde4d817.svg",
    "https://valar-sms.com/static/media/AZ.bcc3dc33.svg",
    "https://valar-sms.com/static/media/BW.8269463f.svg",
    "https://valar-sms.com/static/media/IE.f2b6e66c.svg",
    "https://valar-sms.com/static/media/RO.d13f0184.svg",
    "https://valar-sms.com/static/media/GE.78b2493d.svg",
    "https://valar-sms.com/static/media/LU.43cf27ed.svg",
    "https://valar-sms.com/static/media/SE.25bd123c.svg",
    "https://valar-sms.com/static/media/GD.65bb393e.svg",
    "https://valar-sms.com/static/media/LR.fd7dc6f0.svg",
    "https://valar-sms.com/static/media/EG.5349d5ed.svg",
    "https://valar-sms.com/static/media/CR.daf38afa.svg",
    "https://valar-sms.com/static/media/ET.3c7ae7ae.svg",
    "https://valar-sms.com/static/media/NE.3850bb33.svg",
    "https://valar-sms.com/static/media/TH.632add3a.svg",
    "https://valar-sms.com/static/media/GB.c6e0745b.svg",
    "https://valar-sms.com/static/media/PE.23fb27d8.svg",
    "https://valar-sms.com/static/media/SD.bafd4f3a.svg",
    "https://valar-sms.com/static/media/GA.264db985.svg",
    "https://valar-sms.com/static/media/TJ.37ced611.svg",
    "https://valar-sms.com/static/media/KW.d81d5376.svg",
    "https://valar-sms.com/static/media/ES.2833f86d.svg",
    "https://valar-sms.com/static/media/MO.9159de64.svg",
    "https://valar-sms.com/static/media/GN.9b2cc31b.svg",
    "https://valar-sms.com/static/media/CO.40fd6674.svg",
    "https://valar-sms.com/static/media/IT.446c2f87.svg",
    "https://valar-sms.com/static/media/TL.40d24c12.svg",
    "https://valar-sms.com/static/media/MC.276852c7.svg",
    "https://valar-sms.com/static/media/UA.1c98dd3d.svg",
    "https://valar-sms.com/static/media/KZ.b54cfd78.svg",
    "https://valar-sms.com/static/media/NL.9f24a3db.svg",
    "https://valar-sms.com/static/media/AM.26c66dad.svg",
    "https://valar-sms.com/static/media/US.d6e2427c.svg",
    "https://valar-sms.com/static/media/ZA.c2a25ca1.svg",
    "https://valar-sms.com/static/media/GM.6f2c9085.svg",
    "https://valar-sms.com/static/media/AU.ded60aa3.svg",
    "https://valar-sms.com/static/media/MG.52eb27b3.svg",
    "https://valar-sms.com/static/media/BY.853e5ddb.svg",
    "https://valar-sms.com/static/media/AL.1011693a.svg",
    "https://valar-sms.com/static/media/MX.f2ac965f.svg",
    "https://valar-sms.com/static/media/AF.81a923e2.svg",
    "https://valar-sms.com/static/media/MA.40d145dd.svg",
    "https://valar-sms.com/static/media/QA.321bd702.svg",
    "https://valar-sms.com/static/media/MW.84a544ec.svg",
    "https://valar-sms.com/static/media/HU.06362bba.svg",
    "https://valar-sms.com/static/media/UZ.8ac27841.svg",
    "https://valar-sms.com/static/media/AT.d62eb517.svg",
    "https://valar-sms.com/static/media/SA.7c3534d2.svg",
    "https://valar-sms.com/static/media/BJ.03a813fb.svg",
    "https://valar-sms.com/static/media/CD.05be5862.svg",
    "https://valar-sms.com/static/media/IN.9e3f788c.svg",
    "https://valar-sms.com/static/media/MT.1274ee1e.svg",
    "https://valar-sms.com/static/media/CM.d85c8865.svg",
    "https://valar-sms.com/static/media/TD.0b54e502.svg",
    "https://valar-sms.com/static/media/CZ.99030ef5.svg",
    "https://valar-sms.com/static/media/EC.74700feb.svg",
    "https://valar-sms.com/static/media/SO.1b8788e4.svg",
    "https://valar-sms.com/static/media/TT.4552b6af.svg",
    "https://valar-sms.com/static/media/NA.c8f8d2cb.svg",
    "https://valar-sms.com/static/media/PY.39bdfdc6.svg",
    "https://valar-sms.com/static/media/MU.c8b6fe6f.svg",
    "https://valar-sms.com/static/media/AO.909e2576.svg",
    "https://valar-sms.com/static/media/PK.8feefde0.svg",
    "https://valar-sms.com/static/media/BF.c3386e04.svg",
    "https://valar-sms.com/static/media/MM.13abbec8.svg",
    "https://valar-sms.com/static/media/CU.11fcf53a.svg",
    "https://valar-sms.com/static/media/BI.2236469c.svg",
    "https://valar-sms.com/static/media/LV.54112eaa.svg",
    "https://valar-sms.com/static/media/ZM.0489c39b.svg",
    "https://valar-sms.com/static/media/NO.6fd53332.svg",
    "https://valar-sms.com/static/media/TM.56b496f2.svg",
    "https://valar-sms.com/static/media/CL.bf94e187.svg",
    "https://valar-sms.com/static/media/FR.1404f10a.svg",
    "https://valar-sms.com/static/media/ANY.09cbd92b.svg",
    "https://valar-sms.com/static/media/HK.61f78ccf.svg",
    "https://valar-sms.com/static/media/RE.7d4b746c.svg",
    "https://valar-sms.com/static/media/TW.75c55976.svg",
    "https://valar-sms.com/static/media/SS.79597ae9.svg",
    "https://valar-sms.com/static/media/BA.9936ebec.svg",
    "https://valar-sms.com/static/media/GQ.a42ed491.svg",
    "https://valar-sms.com/static/media/MR.69512b1f.svg",
    "https://valar-sms.com/static/media/GW.0ee0b409.svg",
    "https://valar-sms.com/static/media/RW.c7f8c117.svg",
    "https://valar-sms.com/static/media/CI.2d8c926f.svg",

]
arr_name = [
"China",
"Finland",
"Dominican Republic",
"Israel",
"Maldives",
"Ghana",
"Puerto Rico",
"Barbados",
"Bolivia",
"Mozambique",
"Swaziland",
"Tanzania",
"Venezuela",
"Central African Republic",
"Algeria",
"Yemen",
"Philippines",
"Togo",
"Haiti",
"Iran",
"Syria",
"Mongolia",
"Belgium",
"Bermuda",
"Kenya",
"Nepal",
"Mali",
"Guatemala",
"Russia",
"Sri Lanka",
"Nigeria",
"Uganda",
"Poland",
"Vietnam",
"Oman",
"Tunisia",
"Jordan",
"Bahrain",
"Uruguay",
"Lithuania",
"Papua New Guinea",
"Jamaica",
"Honduras",
"Estonia",
"United Arab Emirates",
"Zimbabwe",
"Panama",
"Nicaragua",
"Congo - Brazzaville",
"Kyrgyzstan",
"St. Lucia",
"Cambodia",
"Indonesia",
"Bulgaria",
"Cook Islands",
"El Salvador",
"Turkey",
"Iraq",
"Germany",
"Libya",
"Lesotho",
"Moldova",
"Senegal",
"Brazil",
"New Zealand",
"Portugal",
"Slovakia",
"Guyana",
"Malaysia",
"Laos",
"Bangladesh",
"Argentina",
"Azerbaijan",
"Botswana",
"Ireland",
"Romania",
"Georgia",
"Luxembourg",
"Sweden",
"Grenada",
"Liberia",
"Egypt",
"Costa Rica",
"Ethiopia",
"Niger",
"Thailand",
"United Kingdom",
"Peru",
"Sudan",
"Gabon",
"Tajikistan",
"Kuwait",
"Spain",
"Macau (China)",
"Guinea",
"Colombia",
"Italy",
"Timor-Leste",
"Monaco",
"Ukraine",
"Kazakhstan",
"Netherlands",
"Armenia",
"United States",
"South Africa",
"Gambia",
"Australia",
"Madagascar",
"Belarus",
"Albania",
"Mexico",
"Afghanistan",
"Morocco",
"Qatar",
"Malawi",
"Hungary",
"Uzbekistan",
"Austria",
"Saudi Arabia",
"Benin",
"Congo - Kinshasa",
"India",
"Malta",
"Cameroon",
"Chad",
"Czech Republic",
"Ecuador",
"Somalia",
"Trinidad & Tobago",
"Namibia",
"Paraguay",
"Mauritius",
"Angola",
"Pakistan",
"Burkina Faso",
"Myanmar (Burma)",
"Cuba",
"Burundi",
"Latvia",
"Zambia",
"Norway",
"Turkmenistan",
"Chile",
"France",
"Any country",
"Hong Kong (China)",
"Réunion",
"Taiwan",
"South Sudan",
"Bosnia & Herzegovina",
"Equatorial Guinea",
"Mauritania",
"Guinea-Bissau",
"Rwanda",
"Côte d’Ivoire"
]

arrdt = []
#print(len(arr_name))
#print(len(arr))
# build_dict

arr_short_name = []
for index in range(len(arr)):
    # arrdt.append({f"{arr_name[index]}": f"{arr[index].split('/')[5]}"})
    arrdt.append([f"{arr_name[index]}", f"{arr[index].split('/')[5]}"])
    # #print(f'"{arr_name[index]}": "{arr[index]}"')
    arr_short_name.append(arr[index].split('/')[5])
# #print(arrdt)
#print(arr_short_name)


# downloand
# for img in arr:
#     name = img.split('/')[5]
#     #print(name)
#     with open(name, 'wb') as handle:
#         response = requests.get(img, stream=True)
#
#         if not response.ok:
#             #print(response)
#
#         for block in response.iter_content(1024):
#             if not block:
#                 break
#
#             handle.write(block)