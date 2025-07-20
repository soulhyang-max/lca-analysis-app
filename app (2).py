import dash
from dash import html, dcc, Input, Output, State, dash_table, callback_context, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import json
import os
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from datetime import datetime

USER_FILE = 'users.json'

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def init_users_file():
    """사용자 데이터 파일이 없으면 초기화"""
    if not os.path.exists(USER_FILE):
        save_users({})
        print(f"사용자 데이터 파일이 생성되었습니다: {USER_FILE}")

class User(UserMixin):
    def __init__(self, id, password_hash):
        self.id = id
        self.password_hash = password_hash
    def get_id(self):
        return self.id

def get_user(user_id):
    users = load_users()
    if user_id in users:
        return User(user_id, users[user_id]['password_hash'])
    return None

impact_db = [
  {
    "DB명": "transport, freight, lorry 16-32 metric ton, EURO6",
    "국가": "RoW",
    "acidification": 0.0004665406527552214,
    "climate change: biogenic": 0.1885494916325229,
    "climate change: fossil": 4.984257528078234e-05,
    "climate change: land use and land use change": 0.1884004414490243,
    "climate change": 9.920760821777495e-05,
    "ecotoxicity: freshwater, inorganics": 1.458160978420497,
    "ecotoxicity: freshwater, organics": 1.407383731993104,
    "ecotoxicity: freshwater": 0.05077724642739304,
    "energy resources: non-renewable": 2.673338483470699,
    "eutrophication: freshwater": 1.54201802372325e-05,
    "eutrophication: marine": 0.000113765206651151,
    "eutrophication: terrestrial": 0.001168781744277254,
    "human toxicity: carcinogenic, inorganics": 8.575753540800703e-11,
    "human toxicity: carcinogenic, organics": 4.237483466122098e-11,
    "human toxicity: carcinogenic": 4.3382700746786e-11,
    "human toxicity: non-carcinogenic, inorganics": 1.930764804227794e-09,
    "human toxicity: non-carcinogenic, organics": 1.833915647669942e-09,
    "human toxicity: non-carcinogenic": 9.684915655785279e-11,
    "ionising radiation: human health": 0.002285335631214934,
    "land use": 1.60622166754322,
    "material resources: metals/minerals": 6.278082963837777e-07,
    "ozone depletion": 2.968749982283703e-09,
    "particulate matter formation": 1.404913238135801e-08,
    "photochemical oxidant formation: human health": 0.0006225210004292991,
    "water use": 0.01274256163584312
  },
  {
    "DB명": "transport, freight, lorry 16-32 metric ton, EURO6",
    "국가": "RER",
    "acidification": 0.0004038703457986204,
    "climate change: biogenic": 0.1849044943815216,
    "climate change: fossil": 5.395457750879004e-05,
    "climate change: land use and land use change": 0.1847593183336692,
    "climate change": 9.12214703436423e-05,
    "ecotoxicity: freshwater, inorganics": 1.297421139330328,
    "ecotoxicity: freshwater, organics": 1.250279474751473,
    "ecotoxicity: freshwater": 0.04714166457885514,
    "energy resources: non-renewable": 2.643776406601877,
    "eutrophication: freshwater": 1.313133949129807e-05,
    "eutrophication: marine": 0.000101894370027364,
    "eutrophication: terrestrial": 0.001035337346297446,
    "human toxicity: carcinogenic, inorganics": 8.45156975327677e-11,
    "human toxicity: carcinogenic, organics": 4.134666791514878e-11,
    "human toxicity: carcinogenic": 4.316902961761902e-11,
    "human toxicity: non-carcinogenic, inorganics": 1.876435142552835e-09,
    "human toxicity: non-carcinogenic, organics": 1.776633292513129e-09,
    "human toxicity: non-carcinogenic": 9.980185003970683e-11,
    "ionising radiation: human health": 0.003551970172243695,
    "land use": 1.586554779024902,
    "material resources: metals/minerals": 6.181358351466749e-07,
    "ozone depletion": 4.022195831609177e-09,
    "particulate matter formation": 1.376775009360797e-08,
    "photochemical oxidant formation: human health": 0.0006269576718477913,
    "water use": 0.01312348222468712
  },
  {
    "DB명": "transport, freight, lorry 3.5-7.5 metric ton, EURO6",
    "국가": "RoW",
    "acidification": 0.0014654751902129,
    "climate change: biogenic": 0.5832636197066242,
    "climate change: fossil": 0.0001800656773564031,
    "climate change: land use and land use change": 0.5827109150920549,
    "climate change": 0.0003726389372128307,
    "ecotoxicity: freshwater, inorganics": 4.661921549697693,
    "ecotoxicity: freshwater, organics": 4.507648785418774,
    "ecotoxicity: freshwater": 0.1542727642789179,
    "energy resources: non-renewable": 8.033766484324296,
    "eutrophication: freshwater": 5.545511778316408e-05,
    "eutrophication: marine": 0.000328130554332174,
    "eutrophication: terrestrial": 0.003370096392963264,
    "human toxicity: carcinogenic, inorganics": 2.902237332053968e-10,
    "human toxicity: carcinogenic, organics": 1.509634039425819e-10,
    "human toxicity: carcinogenic": 1.392603292628147e-10,
    "human toxicity: non-carcinogenic, inorganics": 5.7705895074462e-09,
    "human toxicity: non-carcinogenic, organics": 5.492290499786334e-09,
    "human toxicity: non-carcinogenic": 2.782990076598626e-10,
    "ionising radiation: human health": 0.007965839648235296,
    "land use": 3.341328618064852,
    "material resources: metals/minerals": 2.531119526265904e-06,
    "ozone depletion": 8.793354945116029e-09,
    "particulate matter formation": 3.229991597551551e-08,
    "photochemical oxidant formation: human health": 0.001784803476765617,
    "water use": 0.04218659771213926
  },
  {
    "DB명": "transport, freight, lorry 3.5-7.5 metric ton, EURO6",
    "국가": "RER",
    "acidification": 0.001181818225645573,
    "climate change: biogenic": 0.5568030104900816,
    "climate change: fossil": 0.0002041487601030225,
    "climate change: land use and land use change": 0.5562734206521974,
    "climate change": 0.0003254410777812778,
    "ecotoxicity: freshwater, inorganics": 4.13874249053569,
    "ecotoxicity: freshwater, organics": 3.998170144471372,
    "ecotoxicity: freshwater": 0.1405723460643125,
    "energy resources: non-renewable": 7.880504935416289,
    "eutrophication: freshwater": 4.706549078077587e-05,
    "eutrophication: marine": 0.0002749811658697282,
    "eutrophication: terrestrial": 0.002780417539853232,
    "human toxicity: carcinogenic, inorganics": 2.83013174544733e-10,
    "human toxicity: carcinogenic, organics": 1.459428690074652e-10,
    "human toxicity: carcinogenic": 1.370703055372678e-10,
    "human toxicity: non-carcinogenic, inorganics": 5.477478752340758e-09,
    "human toxicity: non-carcinogenic, organics": 5.194641657184233e-09,
    "human toxicity: non-carcinogenic": 2.828370951565302e-10,
    "ionising radiation: human health": 0.01558348408221075,
    "land use": 3.249297330995121,
    "material resources: metals/minerals": 2.49212904461216e-06,
    "ozone depletion": 1.209968753921939e-08,
    "particulate matter formation": 2.955418984550446e-08,
    "photochemical oxidant formation: human health": 0.001746367566825933,
    "water use": 0.04481477054965119
  },
  {
    "DB명": "transport, freight, lorry >32 metric ton, EURO6",
    "국가": "RoW",
    "acidification": 0.0005864031260656991,
    "climate change: biogenic": 0.2419772990466468,
    "climate change: fossil": 6.433831564264865e-05,
    "climate change: land use and land use change": 0.2417904393736559,
    "climate change": 0.0001225213573482701,
    "ecotoxicity: freshwater, inorganics": 1.884211208859366,
    "ecotoxicity: freshwater, organics": 1.820880717235901,
    "ecotoxicity: freshwater": 0.06333049162346537,
    "energy resources: non-renewable": 3.371052491524187,
    "eutrophication: freshwater": 1.941397838876394e-05,
    "eutrophication: marine": 0.0001392961262372976,
    "eutrophication: terrestrial": 0.001430164605662284,
    "human toxicity: carcinogenic, inorganics": 9.968123716826577e-11,
    "human toxicity: carcinogenic, organics": 5.152095136853231e-11,
    "human toxicity: carcinogenic": 4.816028579973351e-11,
    "human toxicity: non-carcinogenic, inorganics": 2.294900642629378e-09,
    "human toxicity: non-carcinogenic, organics": 2.179457614179735e-09,
    "human toxicity: non-carcinogenic": 1.154430284496475e-10,
    "ionising radiation: human health": 0.002891433147837563,
    "land use": 1.726458423825162,
    "material resources: metals/minerals": 7.848660497313991e-07,
    "ozone depletion": 3.7024959426745e-09,
    "particulate matter formation": 1.548739649926998e-08,
    "photochemical oxidant formation: human health": 0.0007605242682282794,
    "water use": 0.01526158884681789
  },
  {
    "DB명": "transport, freight, lorry >32 metric ton, EURO6",
    "국가": "RER",
    "acidification": 0.0004822246499028764,
    "climate change: biogenic": 0.2337122788437657,
    "climate change: fossil": 7.16607063900633e-05,
    "climate change: land use and land use change": 0.2335332912167705,
    "climate change": 0.0001073269206050781,
    "ecotoxicity: freshwater, inorganics": 1.667796321713106,
    "ecotoxicity: freshwater, organics": 1.6098913537184,
    "ecotoxicity: freshwater": 0.05790496799470424,
    "energy resources: non-renewable": 3.317978966857269,
    "eutrophication: freshwater": 1.616226653886088e-05,
    "eutrophication: marine": 0.0001199181989772127,
    "eutrophication: terrestrial": 0.00121421399407123,
    "human toxicity: carcinogenic, inorganics": 9.727689298552154e-11,
    "human toxicity: carcinogenic, organics": 4.97619396741231e-11,
    "human toxicity: carcinogenic": 4.751495331139843e-11,
    "human toxicity: non-carcinogenic, inorganics": 2.19470831379665e-09,
    "human toxicity: non-carcinogenic, organics": 2.076470947049777e-09,
    "human toxicity: non-carcinogenic": 1.182373667468747e-10,
    "ionising radiation: human health": 0.005328611814607079,
    "land use": 1.692504753308598,
    "material resources: metals/minerals": 7.699722847816843e-07,
    "ozone depletion": 5.096054613406992e-09,
    "particulate matter formation": 1.463379683334167e-08,
    "photochemical oxidant formation: human health": 0.0007543967469791458,
    "water use": 0.0159993975299813
  },
  {
    "DB명": "transport, freight, lorry 7.5-16 metric ton, EURO6",
    "국가": "RoW",
    "acidification": 0.0005864031260656991,
    "climate change: biogenic": 0.2419772990466468,
    "climate change: fossil": 6.433831564264865e-05,
    "climate change: land use and land use change": 0.2417904393736559,
    "climate change": 0.0001225213573482701,
    "ecotoxicity: freshwater, inorganics": 1.884211208859366,
    "ecotoxicity: freshwater, organics": 1.820880717235901,
    "ecotoxicity: freshwater": 0.06333049162346537,
    "energy resources: non-renewable": 3.371052491524187,
    "eutrophication: freshwater": 1.941397838876394e-05,
    "eutrophication: marine": 0.0001392961262372976,
    "eutrophication: terrestrial": 0.001430164605662284,
    "human toxicity: carcinogenic, inorganics": 9.968123716826577e-11,
    "human toxicity: carcinogenic, organics": 5.152095136853231e-11,
    "human toxicity: carcinogenic": 4.816028579973351e-11,
    "human toxicity: non-carcinogenic, inorganics": 2.294900642629378e-09,
    "human toxicity: non-carcinogenic, organics": 2.179457614179735e-09,
    "human toxicity: non-carcinogenic": 1.154430284496475e-10,
    "ionising radiation: human health": 0.002891433147837563,
    "land use": 1.726458423825162,
    "material resources: metals/minerals": 7.848660497313991e-07,
    "ozone depletion": 3.7024959426745e-09,
    "particulate matter formation": 1.548739649926998e-08,
    "photochemical oxidant formation: human health": 0.0007605242682282794,
    "water use": 0.01526158884681789
  },
  {
    "DB명": "transport, freight, lorry 7.5-16 metric ton, EURO6",
    "국가": "RER",
    "acidification": 0.0004822246499028764,
    "climate change: biogenic": 0.2337122788437657,
    "climate change: fossil": 7.16607063900633e-05,
    "climate change: land use and land use change": 0.2335332912167705,
    "climate change": 0.0001073269206050781,
    "ecotoxicity: freshwater, inorganics": 1.667796321713106,
    "ecotoxicity: freshwater, organics": 1.6098913537184,
    "ecotoxicity: freshwater": 0.05790496799470424,
    "energy resources: non-renewable": 3.317978966857269,
    "eutrophication: freshwater": 1.616226653886088e-05,
    "eutrophication: marine": 0.0001199181989772127,
    "eutrophication: terrestrial": 0.00121421399407123,
    "human toxicity: carcinogenic, inorganics": 9.727689298552154e-11,
    "human toxicity: carcinogenic, organics": 4.97619396741231e-11,
    "human toxicity: carcinogenic": 4.751495331139843e-11,
    "human toxicity: non-carcinogenic, inorganics": 2.19470831379665e-09,
    "human toxicity: non-carcinogenic, organics": 2.076470947049777e-09,
    "human toxicity: non-carcinogenic": 1.182373667468747e-10,
    "ionising radiation: human health": 0.005328611814607079,
    "land use": 1.692504753308598,
    "material resources: metals/minerals": 7.699722847816843e-07,
    "ozone depletion": 5.096054613406992e-09,
    "particulate matter formation": 1.463379683334167e-08,
    "photochemical oxidant formation: human health": 0.0007543967469791458,
    "water use": 0.0159993975299813
  },
  {
    "DB명": "polyethylene production, high density, granulate",
    "국가": "RoW",
    "acidification": 0.00949400748439431,
    "climate change: biogenic": 2.319841799669729,
    "climate change: fossil": 0.00333584003715966,
    "climate change: land use and land use change": 2.315526561786595,
    "climate change": 0.0009793978459743515,
    "ecotoxicity: freshwater, inorganics": 5.923059096439043,
    "ecotoxicity: freshwater, organics": 5.683652676192211,
    "ecotoxicity: freshwater": 0.239406420246832,
    "energy resources: non-renewable": 74.43150120860705,
    "eutrophication: freshwater": 0.0004252027903414324,
    "eutrophication: marine": 0.001759914932188462,
    "eutrophication: terrestrial": 0.01868736756630648,
    "human toxicity: carcinogenic, inorganics": 5.710567446493816e-10,
    "human toxicity: carcinogenic, organics": 4.100809658634467e-10,
    "human toxicity: carcinogenic": 1.60975778785935e-10,
    "human toxicity: non-carcinogenic, inorganics": 1.469776192777208e-08,
    "human toxicity: non-carcinogenic, organics": 1.342389703434892e-08,
    "human toxicity: non-carcinogenic": 1.27386489342315e-09,
    "ionising radiation: human health": 0.05045623996022707,
    "land use": 2.461554565003346,
    "material resources: metals/minerals": 9.148277310449493e-06,
    "ozone depletion": 1.116332113691052e-08,
    "particulate matter formation": 9.240752289283923e-08,
    "photochemical oxidant formation: human health": 0.008235166310629835,
    "water use": 0.8593832580819728
  },
  {
    "DB명": "polyethylene production, high density, granulate",
    "국가": "RER",
    "acidification": 0.006798662297169727,
    "climate change: biogenic": 1.902452277669814,
    "climate change: fossil": 0.002646415894692653,
    "climate change: land use and land use change": 1.899224781384523,
    "climate change": 0.0005810803905991912,
    "ecotoxicity: freshwater, inorganics": 2.329763422883976,
    "ecotoxicity: freshwater, organics": 2.115817675941261,
    "ecotoxicity: freshwater": 0.2139457469427152,
    "energy resources: non-renewable": 71.66140161815167,
    "eutrophication: freshwater": 0.0002561060809799675,
    "eutrophication: marine": 0.001244439682640138,
    "eutrophication: terrestrial": 0.01312753987626972,
    "human toxicity: carcinogenic, inorganics": 4.563795392364182e-10,
    "human toxicity: carcinogenic, organics": 3.20413782290535e-10,
    "human toxicity: carcinogenic": 1.359657569458833e-10,
    "human toxicity: non-carcinogenic, inorganics": 1.020982894849495e-08,
    "human toxicity: non-carcinogenic, organics": 9.02920515010368e-09,
    "human toxicity: non-carcinogenic": 1.180623798391279e-09,
    "ionising radiation: human health": 0.1284678267723885,
    "land use": 1.734966913842621,
    "material resources: metals/minerals": 8.663070420361225e-06,
    "ozone depletion": 1.276582937497122e-08,
    "particulate matter formation": 7.036248143653954e-08,
    "photochemical oxidant formation: human health": 0.006775907997083089,
    "water use": 0.8505148105766858
  },
  {
    "DB명": "aluminium production, primary, ingot",
    "국가": "CA",
    "acidification": 0.07274530842500421,
    "climate change: biogenic": 7.531954855102165,
    "climate change: fossil": 0.009292538220617437,
    "climate change: land use and land use change": 7.41235336501448,
    "climate change": 0.110308951867068,
    "ecotoxicity: freshwater, inorganics": 29.5399861793615,
    "ecotoxicity: freshwater, organics": 23.63695026205819,
    "ecotoxicity: freshwater": 5.903035917303241,
    "energy resources: non-renewable": 67.80769940202516,
    "eutrophication: freshwater": 0.002109110415922267,
    "eutrophication: marine": 0.007806449722818277,
    "eutrophication: terrestrial": 0.08202186943458226,
    "human toxicity: carcinogenic, inorganics": 6.562643153672702e-08,
    "human toxicity: carcinogenic, organics": 1.468461006857164e-08,
    "human toxicity: carcinogenic": 5.09418214681554e-08,
    "human toxicity: non-carcinogenic, inorganics": 2.59514388203509e-07,
    "human toxicity: non-carcinogenic, organics": 2.577386639564009e-07,
    "human toxicity: non-carcinogenic": 1.775724247108028e-09,
    "ionising radiation: human health": 0.09736468819345638,
    "land use": -39.03220486521756,
    "material resources: metals/minerals": 1.39497047169255e-05,
    "ozone depletion": 1.514375906940261e-07,
    "particulate matter formation": 1.08868562585728e-06,
    "photochemical oxidant formation: human health": 0.03154068397176298,
    "water use": 13.03913186075013
  },
  {
    "DB명": "aluminium production, primary, ingot",
    "국가": "CN",
    "acidification": 0.152554308777789,
    "climate change: biogenic": 23.45972623934835,
    "climate change: fossil": 0.005362904244666704,
    "climate change: land use and land use change": 23.45158165702678,
    "climate change": 0.002781678076909631,
    "ecotoxicity: freshwater, inorganics": 71.77069366490076,
    "ecotoxicity: freshwater, organics": 65.94981346960803,
    "ecotoxicity: freshwater": 5.820880195292715,
    "energy resources: non-renewable": 201.6447697747971,
    "eutrophication: freshwater": 0.00503809873712295,
    "eutrophication: marine": 0.0264880458439425,
    "eutrophication: terrestrial": 0.2801804076991723,
    "human toxicity: carcinogenic, inorganics": 2.34292788250928e-08,
    "human toxicity: carcinogenic, organics": 1.685979109484417e-08,
    "human toxicity: carcinogenic": 6.569487730248628e-09,
    "human toxicity: non-carcinogenic, inorganics": 4.01804913870341e-07,
    "human toxicity: non-carcinogenic, organics": 3.960107719184352e-07,
    "human toxicity: non-carcinogenic": 5.794141951905902e-09,
    "ionising radiation: human health": 0.1204167963080752,
    "land use": 45.34248184746616,
    "material resources: metals/minerals": 1.467103057246489e-05,
    "ozone depletion": 1.651519907724918e-07,
    "particulate matter formation": 2.190133658984605e-06,
    "photochemical oxidant formation: human health": 0.08210818520209107,
    "water use": 2.46949383470672
  },
  {
    "DB명": "aluminium production, primary, ingot",
    "국가": "IAI Area, Africa",
    "acidification": 0.1668283099115653,
    "climate change: biogenic": 14.89068168519825,
    "climate change: fossil": 0.05222177318051805,
    "climate change: land use and land use change": 14.49566963880149,
    "climate change": 0.3427902732162345,
    "ecotoxicity: freshwater, inorganics": 34.06448835607939,
    "ecotoxicity: freshwater, organics": 28.28671278184996,
    "ecotoxicity: freshwater": 5.777775574229461,
    "energy resources: non-renewable": 154.2874989232529,
    "eutrophication: freshwater": 0.007433525353435458,
    "eutrophication: marine": 0.0216059103416835,
    "eutrophication: terrestrial": 0.2257922320132275,
    "human toxicity: carcinogenic, inorganics": 2.250521095784486e-08,
    "human toxicity: carcinogenic, organics": 1.67828592544015e-08,
    "human toxicity: carcinogenic": 5.722351703443351e-09,
    "human toxicity: non-carcinogenic, inorganics": 4.107828803180869e-07,
    "human toxicity: non-carcinogenic, organics": 4.085154291601732e-07,
    "human toxicity: non-carcinogenic": 2.267451157913818e-09,
    "ionising radiation: human health": 0.1062327988381448,
    "land use": 22.89984274783768,
    "material resources: metals/minerals": 1.426750568550063e-05,
    "ozone depletion": 1.56672363723765e-07,
    "particulate matter formation": 1.067457370253812e-06,
    "photochemical oxidant formation: human health": 0.0686242960427617,
    "water use": 12.2573711580391
  },
  {
    "DB명": "aluminium production, primary, ingot",
    "국가": "IAI Area, Asia, without China and GCC",
    "acidification": 0.1856897814144623,
    "climate change: biogenic": 28.76639570707204,
    "climate change: fossil": 0.0175805993253771,
    "climate change: land use and land use change": 28.68962949346153,
    "climate change": 0.05918561428513328,
    "ecotoxicity: freshwater, inorganics": 69.46577126234288,
    "ecotoxicity: freshwater, organics": 63.40811115934761,
    "ecotoxicity: freshwater": 6.057660102995135,
    "energy resources: non-renewable": 301.2581179301421,
    "eutrophication: freshwater": 0.01702915177199283,
    "eutrophication: marine": 0.03114260813822619,
    "eutrophication: terrestrial": 0.3158780966297546,
    "human toxicity: carcinogenic, inorganics": 2.457536912326248e-08,
    "human toxicity: carcinogenic, organics": 1.875473919780522e-08,
    "human toxicity: carcinogenic": 5.820629925457272e-09,
    "human toxicity: non-carcinogenic, inorganics": 5.23369392885418e-07,
    "human toxicity: non-carcinogenic, organics": 5.2030209683425e-07,
    "human toxicity: non-carcinogenic": 3.06729605116885e-09,
    "ionising radiation: human health": 0.1316515486426217,
    "land use": 46.74423099516451,
    "material resources: metals/minerals": 1.63739570503291e-05,
    "ozone depletion": 1.697790440866463e-07,
    "particulate matter formation": 1.394838948141921e-06,
    "photochemical oxidant formation: human health": 0.0916225895054273,
    "water use": 4.275152879912463
  },
  {
    "DB명": "aluminium production, primary, ingot",
    "국가": "IAI Area, EU27 & EFTA",
    "acidification": 0.04500047002693963,
    "climate change: biogenic": 7.209838002062297,
    "climate change: fossil": 0.03071537943140184,
    "climate change: land use and land use change": 7.012753619475435,
    "climate change": 0.1663690031554594,
    "ecotoxicity: freshwater, inorganics": 28.12055616594674,
    "ecotoxicity: freshwater, organics": 23.35519712553974,
    "ecotoxicity: freshwater": 4.765359040406999,
    "energy resources: non-renewable": 109.0333275055194,
    "eutrophication: freshwater": 0.004048042215268272,
    "eutrophication: marine": 0.006295313759958244,
    "eutrophication: terrestrial": 0.05722494449981276,
    "human toxicity: carcinogenic, inorganics": 2.255758471894239e-08,
    "human toxicity: carcinogenic, organics": 9.912688653556317e-09,
    "human toxicity: carcinogenic": 1.264489606538606e-08,
    "human toxicity: non-carcinogenic, inorganics": 2.094500268009302e-07,
    "human toxicity: non-carcinogenic, organics": 2.078621822736765e-07,
    "human toxicity: non-carcinogenic": 1.587844527253796e-09,
    "ionising radiation: human health": 1.89475927009532,
    "land use": 7.5173405791649,
    "material resources: metals/minerals": 1.381208104127097e-05,
    "ozone depletion": 2.111092104276512e-07,
    "particulate matter formation": 5.311078337503402e-07,
    "photochemical oxidant formation: human health": 0.02486093147595597,
    "water use": 13.88397488159878
  },
  {
    "DB명": "aluminium production, primary, ingot",
    "국가": "IAI Area, Gulf Cooperation Council",
    "acidification": 0.07163327640051889,
    "climate change: biogenic": 16.82197143040647,
    "climate change: fossil": 0.004639322996635662,
    "climate change: land use and land use change": 16.81470423497709,
    "climate change": 0.002627872432750107,
    "ecotoxicity: freshwater, inorganics": 31.62263228655986,
    "ecotoxicity: freshwater, organics": 25.75710182808128,
    "ecotoxicity: freshwater": 5.865530458478608,
    "energy resources: non-renewable": 227.4770879265284,
    "eutrophication: freshwater": 0.002186070521863026,
    "eutrophication: marine": 0.01071425731606057,
    "eutrophication: terrestrial": 0.1134924027792365,
    "human toxicity: carcinogenic, inorganics": 2.071021093509679e-08,
    "human toxicity: carcinogenic, organics": 1.491668688120707e-08,
    "human toxicity: carcinogenic": 5.793524053889709e-09,
    "human toxicity: non-carcinogenic, inorganics": 2.734357795956653e-07,
    "human toxicity: non-carcinogenic, organics": 2.696608332941752e-07,
    "human toxicity: non-carcinogenic": 3.774946301489604e-09,
    "ionising radiation: human health": 0.1021106998715751,
    "land use": 17.28041996868982,
    "material resources: metals/minerals": 2.020778294134242e-05,
    "ozone depletion": 4.465873116674401e-07,
    "particulate matter formation": 8.080546784987164e-07,
    "photochemical oxidant formation: human health": 0.05252853336637274,
    "water use": 1.625552496848945
  },
  {
    "DB명": "aluminium production, primary, ingot",
    "국가": "IAI Area, Russia & RER w/o EU27 & EFTA",
    "acidification": 0.07113912877222803,
    "climate change: biogenic": 9.162538451271352,
    "climate change: fossil": 0.0301522880017663,
    "climate change: land use and land use change": 8.946837897709509,
    "climate change": 0.185548265560079,
    "ecotoxicity: freshwater, inorganics": 36.45134394017978,
    "ecotoxicity: freshwater, organics": 28.9005189398837,
    "ecotoxicity: freshwater": 7.55082500029611,
    "energy resources: non-renewable": 87.80248833023157,
    "eutrophication: freshwater": 0.003252848533798053,
    "eutrophication: marine": 0.009362567440098989,
    "eutrophication: terrestrial": 0.09545582447007042,
    "human toxicity: carcinogenic, inorganics": 2.657842799348112e-08,
    "human toxicity: carcinogenic, organics": 1.554413988335604e-08,
    "human toxicity: carcinogenic": 1.103428811012507e-08,
    "human toxicity: non-carcinogenic, inorganics": 2.813361915567022e-07,
    "human toxicity: non-carcinogenic, organics": 2.792113669102894e-07,
    "human toxicity: non-carcinogenic": 2.124824646413492e-09,
    "ionising radiation: human health": 0.8694779052786257,
    "land use": 12.99476172753121,
    "material resources: metals/minerals": 1.466118351983391e-05,
    "ozone depletion": 1.642215882539971e-07,
    "particulate matter formation": 9.822265196963632e-07,
    "photochemical oxidant formation: human health": 0.03462549314529683,
    "water use": 7.39898635794165
  },
  {
    "DB명": "aluminium production, primary, ingot",
    "국가": "IAI Area, South America",
    "acidification": 0.06685286851051553,
    "climate change: biogenic": 11.16477604298506,
    "climate change: fossil": 0.4668022344864314,
    "climate change: land use and land use change": 10.33654370927779,
    "climate change": 0.3614300992208376,
    "ecotoxicity: freshwater, inorganics": 32.18423295565285,
    "ecotoxicity: freshwater, organics": 25.70908491048947,
    "ecotoxicity: freshwater": 6.475148045163374,
    "energy resources: non-renewable": 112.4365966214519,
    "eutrophication: freshwater": 0.002144376274886037,
    "eutrophication: marine": 0.008860542897445233,
    "eutrophication: terrestrial": 0.09178377299690457,
    "human toxicity: carcinogenic, inorganics": 2.261569244053088e-08,
    "human toxicity: carcinogenic, organics": 1.480702003098145e-08,
    "human toxicity: carcinogenic": 7.808672409549422e-09,
    "human toxicity: non-carcinogenic, inorganics": 2.65860929202485e-07,
    "human toxicity: non-carcinogenic, organics": 2.626929015545532e-07,
    "human toxicity: non-carcinogenic": 3.168027647932214e-09,
    "ionising radiation: human health": 0.1019536820902814,
    "land use": 15.18845237590232,
    "material resources: metals/minerals": 1.569200341185139e-05,
    "ozone depletion": 2.466607216551348e-07,
    "particulate matter formation": 9.586135273429514e-07,
    "photochemical oxidant formation: human health": 0.03723539461729936,
    "water use": 16.98604685816212
  },
  {
    "DB명": "aluminium production, primary, ingot",
    "국가": "RoW",
    "acidification": 0.2131287630157153,
    "climate change: biogenic": 21.7601748187725,
    "climate change: fossil": 0.005621589745292675,
    "climate change: land use and land use change": 21.75066956179978,
    "climate change": 0.003883667227425767,
    "ecotoxicity: freshwater, inorganics": 63.84868894806888,
    "ecotoxicity: freshwater, organics": 57.94316467383771,
    "ecotoxicity: freshwater": 5.905524274231193,
    "energy resources: non-renewable": 218.5732947288747,
    "eutrophication: freshwater": 0.01172769531394853,
    "eutrophication: marine": 0.02789105651637363,
    "eutrophication: terrestrial": 0.2822326189309778,
    "human toxicity: carcinogenic, inorganics": 2.296890757788624e-08,
    "human toxicity: carcinogenic, organics": 1.67263532255599e-08,
    "human toxicity: carcinogenic": 6.242554352326328e-09,
    "human toxicity: non-carcinogenic, inorganics": 3.870642539431181e-07,
    "human toxicity: non-carcinogenic, organics": 3.837539694000125e-07,
    "human toxicity: non-carcinogenic": 3.310284543105822e-09,
    "ionising radiation: human health": 1.162519599819061,
    "land use": 36.37556477245249,
    "material resources: metals/minerals": 1.528109481675105e-05,
    "ozone depletion": 1.676300805701456e-07,
    "particulate matter formation": 1.179865478408671e-06,
    "photochemical oxidant formation: human health": 0.08556866847518561,
    "water use": 2.221904947248021
  },
  {
    "DB명": "aluminium production, primary, ingot",
    "국가": "UN-OCEANIA",
    "acidification": 0.1367725510152475,
    "climate change: biogenic": 20.27065603442973,
    "climate change: fossil": 0.01895487614542686,
    "climate change: land use and land use change": 20.14602892865204,
    "climate change": 0.1056722296322639,
    "ecotoxicity: freshwater, inorganics": 71.11160988379417,
    "ecotoxicity: freshwater, organics": 65.34116410125692,
    "ecotoxicity: freshwater": 5.770445782537252,
    "energy resources: non-renewable": 189.3771740019663,
    "eutrophication: freshwater": 0.02989406621320967,
    "eutrophication: marine": 0.02296478104600976,
    "eutrophication: terrestrial": 0.1876350023737772,
    "human toxicity: carcinogenic, inorganics": 2.249992654859584e-08,
    "human toxicity: carcinogenic, organics": 1.712497874728282e-08,
    "human toxicity: carcinogenic": 5.374947801313021e-09,
    "human toxicity: non-carcinogenic, inorganics": 4.017716574455321e-07,
    "human toxicity: non-carcinogenic, organics": 3.997057945234609e-07,
    "human toxicity: non-carcinogenic": 2.065862922070719e-09,
    "ionising radiation: human health": 0.1148581698398097,
    "land use": 16.24134286459061,
    "material resources: metals/minerals": 1.443109247741315e-05,
    "ozone depletion": 1.517946911612031e-07,
    "particulate matter formation": 8.630468273072206e-07,
    "photochemical oxidant formation: human health": 0.0585585738917486,
    "water use": 5.138262393073969
  },
  {
    "DB명": "textile production, nonwoven polyester, needle-punched",
    "국가": "RoW",
    "acidification": 0.02814244724467353,
    "climate change: biogenic": 5.504900059124122,
    "climate change: fossil": 0.01785778283319467,
    "climate change: land use and land use change": 5.481263123148413,
    "climate change": 0.005779153142512804,
    "ecotoxicity: freshwater, inorganics": 26.78565415684695,
    "ecotoxicity: freshwater, organics": 24.75262648240592,
    "ecotoxicity: freshwater": 2.033027674441061,
    "energy resources: non-renewable": 102.9708882632134,
    "eutrophication: freshwater": 0.001491653800889585,
    "eutrophication: marine": 0.005433351836650348,
    "eutrophication: terrestrial": 0.06944430405575032,
    "human toxicity: carcinogenic, inorganics": 3.347169324305157e-09,
    "human toxicity: carcinogenic, organics": 1.799169113692585e-09,
    "human toxicity: carcinogenic": 1.548000210612571e-09,
    "human toxicity: non-carcinogenic, inorganics": 5.869232086748439e-08,
    "human toxicity: non-carcinogenic, organics": 5.28227363968471e-08,
    "human toxicity: non-carcinogenic": 5.869584470637308e-09,
    "ionising radiation: human health": 0.3335569358223986,
    "land use": 25.5818856009411,
    "material resources: metals/minerals": 4.347742728603094e-05,
    "ozone depletion": 1.584259935413488e-05,
    "particulate matter formation": 3.516418296341304e-07,
    "photochemical oxidant formation: human health": 0.0259000813281171,
    "water use": 2.450199904596805
  },
  {
    "DB명": "polyester fibre production, finished",
    "국가": "RoW",
    "acidification": 0.01826230221400528,
    "climate change: biogenic": 4.275012087831722,
    "climate change: fossil": 0.007139959343636908,
    "climate change: land use and land use change": 4.263716498467941,
    "climate change": 0.004155630020143294,
    "ecotoxicity: freshwater, inorganics": 18.34231434200919,
    "ecotoxicity: freshwater, organics": 16.75921321534582,
    "ecotoxicity: freshwater": 1.583101126663371,
    "energy resources: non-renewable": 87.95724040820083,
    "eutrophication: freshwater": 0.001139801166710037,
    "eutrophication: marine": 0.003809648449853346,
    "eutrophication: terrestrial": 0.03701724388462149,
    "human toxicity: carcinogenic, inorganics": 1.623646139311896e-09,
    "human toxicity: carcinogenic, organics": 1.075402404591433e-09,
    "human toxicity: carcinogenic": 5.482437347204637e-10,
    "human toxicity: non-carcinogenic, inorganics": 4.244717307333613e-08,
    "human toxicity: non-carcinogenic, organics": 3.727098271946414e-08,
    "human toxicity: non-carcinogenic": 5.176190353872026e-09,
    "ionising radiation: human health": 0.2557663388674392,
    "land use": 9.018454464783193,
    "material resources: metals/minerals": 2.622307637014384e-05,
    "ozone depletion": 1.529481966300286e-05,
    "particulate matter formation": 1.989217986321935e-07,
    "photochemical oxidant formation: human health": 0.02043012093680842,
    "water use": 2.028320597357287
  },
  {
    "DB명": "polyethylene production, low density, granulate",
    "국가": "RoW",
    "acidification": 0.01067564295732578,
    "climate change: biogenic": 2.50676825391379,
    "climate change: fossil": 0.004011815577610536,
    "climate change: land use and land use change": 2.501096832366965,
    "climate change": 0.001659605969214708,
    "ecotoxicity: freshwater, inorganics": 6.635096039269144,
    "ecotoxicity: freshwater, organics": 6.343743545511278,
    "ecotoxicity: freshwater": 0.2913524937578642,
    "energy resources: non-renewable": 76.54932860096491,
    "eutrophication: freshwater": 0.0005588645761402161,
    "eutrophication: marine": 0.002040844981870758,
    "eutrophication: terrestrial": 0.02139373094225725,
    "human toxicity: carcinogenic, inorganics": 5.564690578671809e-10,
    "human toxicity: carcinogenic, organics": 3.906119948515446e-10,
    "human toxicity: carcinogenic": 1.658570630156364e-10,
    "human toxicity: non-carcinogenic, inorganics": 1.71472046941732e-08,
    "human toxicity: non-carcinogenic, organics": 1.578373221501751e-08,
    "human toxicity: non-carcinogenic": 1.36347247915571e-09,
    "ionising radiation: human health": 0.08404052397838571,
    "land use": 2.977466261983676,
    "material resources: metals/minerals": 9.252973824386622e-06,
    "ozone depletion": 1.038420589649407e-08,
    "particulate matter formation": 1.023936733971553e-07,
    "photochemical oxidant formation: human health": 0.01083143519517877,
    "water use": 1.138914447765908
  },
  {
    "DB명": "polyethylene production, low density, granulate",
    "국가": "RER",
    "acidification": 0.007221533076845002,
    "climate change: biogenic": 1.918311433350991,
    "climate change: fossil": 0.003516287635079392,
    "climate change: land use and land use change": 1.913835019627547,
    "climate change": 0.000960126088364821,
    "ecotoxicity: freshwater, inorganics": 2.572830317746567,
    "ecotoxicity: freshwater, organics": 2.31201396961881,
    "ecotoxicity: freshwater": 0.2608163481277585,
    "energy resources: non-renewable": 73.30242919340652,
    "eutrophication: freshwater": 0.0003915326247385986,
    "eutrophication: marine": 0.001348185270776277,
    "eutrophication: terrestrial": 0.01376583698436941,
    "human toxicity: carcinogenic, inorganics": 4.130154604506418e-10,
    "human toxicity: carcinogenic, organics": 2.788739867222818e-10,
    "human toxicity: carcinogenic": 1.341414737283597e-10,
    "human toxicity: non-carcinogenic, inorganics": 1.141246562260072e-08,
    "human toxicity: non-carcinogenic, organics": 1.01836289862036e-08,
    "human toxicity: non-carcinogenic": 1.228836636397106e-09,
    "ionising radiation: human health": 0.2308907319019235,
    "land use": 2.155549485857873,
    "material resources: metals/minerals": 8.80035278874485e-06,
    "ozone depletion": 1.104004331796178e-08,
    "particulate matter formation": 6.904625664702536e-08,
    "photochemical oxidant formation: human health": 0.008798455340865246,
    "water use": 1.141473299975068
  },
  {
    "DB명": "acrylic acid production",
    "국가": "RER",
    "acidification": 0.004609103404363894,
    "climate change: biogenic": 1.931622254693634,
    "climate change: fossil": 0.001957810744449999,
    "climate change: land use and land use change": 1.929166582043466,
    "climate change": 0.0004978619057187129,
    "ecotoxicity: freshwater, inorganics": 2.090730626101454,
    "ecotoxicity: freshwater, organics": 1.502518206020707,
    "ecotoxicity: freshwater": 0.588212420080749,
    "energy resources: non-renewable": 46.00626074804178,
    "eutrophication: freshwater": 0.0002148351555428486,
    "eutrophication: marine": 0.0007823929977316197,
    "eutrophication: terrestrial": 0.008292983885189852,
    "human toxicity: carcinogenic, inorganics": 2.977591004878595e-10,
    "human toxicity: carcinogenic, organics": 2.15470700859149e-10,
    "human toxicity: carcinogenic": 8.228839962871039e-11,
    "human toxicity: non-carcinogenic, inorganics": 8.982055087846505e-09,
    "human toxicity: non-carcinogenic, organics": 8.077613012079946e-09,
    "human toxicity: non-carcinogenic": 9.044420757665602e-10,
    "ionising radiation: human health": 0.1084258311702076,
    "land use": 1.504653020492235,
    "material resources: metals/minerals": 8.410277347940112e-06,
    "ozone depletion": 5.198717595287971e-09,
    "particulate matter formation": 4.595611690829414e-08,
    "photochemical oxidant formation: human health": 0.003802121046676237,
    "water use": 0.4852289673573231
  },
  {
    "DB명": "market for electricity, high voltage",
    "국가": "KR",
    "acidification": 0.002244768124836137,
    "climate change: biogenic": 0.6934377394283747,
    "climate change: fossil": 0.000675147888403226,
    "climate change: land use and land use change": 0.6923963204682079,
    "climate change": 0.0003662710717635833,
    "ecotoxicity: freshwater, inorganics": 1.357335640253134,
    "ecotoxicity: freshwater, organics": 1.34043833119982,
    "ecotoxicity: freshwater": 0.01689730905331286,
    "energy resources: non-renewable": 11.51894026087301,
    "eutrophication: freshwater": 0.000485558132883358,
    "eutrophication: marine": 0.0007439615242034082,
    "eutrophication: terrestrial": 0.007296536259746033,
    "human toxicity: carcinogenic, inorganics": 1.913203541803247e-10,
    "human toxicity: carcinogenic, organics": 9.519289737837866e-11,
    "human toxicity: carcinogenic": 9.6127456801946e-11,
    "human toxicity: non-carcinogenic, inorganics": 4.918644289939532e-09,
    "human toxicity: non-carcinogenic, organics": 4.844997904336491e-09,
    "human toxicity: non-carcinogenic": 7.364638560304961e-11,
    "ionising radiation: human health": 0.2131758554513167,
    "land use": 1.465688838081694,
    "material resources: metals/minerals": 3.023883466100206e-07,
    "ozone depletion": 8.284666228425721e-09,
    "particulate matter formation": 7.681844924184631e-09,
    "photochemical oxidant formation: human health": 0.002027089180831424,
    "water use": 0.1442360415940051
  },
  {
    "DB명": "market for electricity, low voltage",
    "국가": "KR",
    "acidification": 0.002526622704752922,
    "climate change: biogenic": 0.6972658679996785,
    "climate change: fossil": 0.0006952185934046667,
    "climate change: land use and land use change": 0.6961905476755239,
    "climate change": 0.0003801017307499951,
    "ecotoxicity: freshwater, inorganics": 1.836318725005255,
    "ecotoxicity: freshwater, organics": 1.700961476867264,
    "ecotoxicity: freshwater": 0.1353572481379872,
    "energy resources: non-renewable": 11.53248652115303,
    "eutrophication: freshwater": 0.0005043561315997108,
    "eutrophication: marine": 0.0007573378252238169,
    "eutrophication: terrestrial": 0.007486387223878489,
    "human toxicity: carcinogenic, inorganics": 2.59325108472665e-10,
    "human toxicity: carcinogenic, organics": 1.395417901399197e-10,
    "human toxicity: carcinogenic": 1.197833183327455e-10,
    "human toxicity: non-carcinogenic, inorganics": 8.69970563834228e-09,
    "human toxicity: non-carcinogenic, organics": 8.454299620413364e-09,
    "human toxicity: non-carcinogenic": 2.454060179289155e-10,
    "ionising radiation: human health": 0.2119873514236743,
    "land use": 1.953722610877758,
    "material resources: metals/minerals": 4.061672751456263e-06,
    "ozone depletion": 9.016139755645753e-09,
    "particulate matter formation": 9.145242749917749e-09,
    "photochemical oxidant formation: human health": 0.002088431954138908,
    "water use": 0.1514953305327877
  },
  {
    "DB명": "market for electricity, medium voltage",
    "국가": "KR",
    "acidification": 0.002290940718494875,
    "climate change: biogenic": 0.6982364284204597,
    "climate change: fossil": 0.000680383316637915,
    "climate change: land use and land use change": 0.6971854866141471,
    "climate change": 0.0003705584896746791,
    "ecotoxicity: freshwater, inorganics": 1.518488410266983,
    "ecotoxicity: freshwater, organics": 1.38467438431168,
    "ecotoxicity: freshwater": 0.1338140259553028,
    "energy resources: non-renewable": 11.58594214018137,
    "eutrophication: freshwater": 0.0004904382542527294,
    "eutrophication: marine": 0.0007498097447350837,
    "eutrophication: terrestrial": 0.007360444457016417,
    "human toxicity: carcinogenic, inorganics": 2.071805222643616e-10,
    "human toxicity: carcinogenic, organics": 1.010661983891545e-10,
    "human toxicity: carcinogenic": 1.061143238752073e-10,
    "human toxicity: non-carcinogenic, inorganics": 5.363984363375611e-09,
    "human toxicity: non-carcinogenic, organics": 5.269411978278333e-09,
    "human toxicity: non-carcinogenic": 9.457238509727705e-11,
    "ionising radiation: human health": 0.214186718604455,
    "land use": 1.48906334049838,
    "material resources: metals/minerals": 7.038524186560069e-07,
    "ozone depletion": 8.723579594913982e-09,
    "particulate matter formation": 7.864715752868226e-09,
    "photochemical oxidant formation: human health": 0.002048050639163668,
    "water use": 0.1455512808908281
  },
  {
    "DB명": "market for natural gas, liquefied",
    "국가": "GLO",
    "acidification": 0.0026799757986518,
    "climate change: biogenic": 0.6422668137809451,
    "climate change: fossil": 0.0002366429869226088,
    "climate change: land use and land use change": 0.641833981244906,
    "climate change": 0.0001961895491164682,
    "ecotoxicity: freshwater, inorganics": 0.9075747363661636,
    "ecotoxicity: freshwater, organics": 0.8383982651628795,
    "ecotoxicity: freshwater": 0.06917647120328452,
    "energy resources: non-renewable": 42.97126471372196,
    "eutrophication: freshwater": 3.25654522474467e-05,
    "eutrophication: marine": 0.0007226685023302352,
    "eutrophication: terrestrial": 0.007906311491513635,
    "human toxicity: carcinogenic, inorganics": 3.064258099740601e-10,
    "human toxicity: carcinogenic, organics": 1.469588891220416e-10,
    "human toxicity: carcinogenic": 1.594669208520186e-10,
    "human toxicity: non-carcinogenic, inorganics": 2.426595127691025e-09,
    "human toxicity: non-carcinogenic, organics": 2.040426414766669e-09,
    "human toxicity: non-carcinogenic": 3.861687129243546e-10,
    "ionising radiation: human health": 0.004247265162833278,
    "land use": 0.4084550245400763,
    "material resources: metals/minerals": 4.51438561354382e-07,
    "ozone depletion": 8.56831559563567e-08,
    "particulate matter formation": 8.882372323164838e-09,
    "photochemical oxidant formation: human health": 0.005072476247115901,
    "water use": 0.03961990425192723
  },
  {
    "DB명": "market for liquefied petroleum gas",
    "국가": "RoW",
    "acidification": 0.005834859508290099,
    "climate change: biogenic": 0.9846939489051307,
    "climate change: fossil": 0.0003126572656427796,
    "climate change: land use and land use change": 0.9841101679610125,
    "climate change": 0.0002711236784754525,
    "ecotoxicity: freshwater, inorganics": 28.99553765835892,
    "ecotoxicity: freshwater, organics": 28.04454428913568,
    "ecotoxicity: freshwater": 0.9509933692232092,
    "energy resources: non-renewable": 57.26754745721954,
    "eutrophication: freshwater": 4.275242038089833e-05,
    "eutrophication: marine": 0.001055601873969488,
    "eutrophication: terrestrial": 0.009862628230207459,
    "human toxicity: carcinogenic, inorganics": 3.596403242258424e-10,
    "human toxicity: carcinogenic, organics": 1.989665878994024e-10,
    "human toxicity: carcinogenic": 1.606737363264403e-10,
    "human toxicity: non-carcinogenic, inorganics": 6.869330888431206e-09,
    "human toxicity: non-carcinogenic, organics": 6.191630649269595e-09,
    "human toxicity: non-carcinogenic": 6.777002391616192e-10,
    "ionising radiation: human health": 0.01225781595863316,
    "land use": 3.47727336351941,
    "material resources: metals/minerals": 6.540021127230025e-07,
    "ozone depletion": 5.863888500636856e-08,
    "particulate matter formation": 4.868278997189408e-08,
    "photochemical oxidant formation: human health": 0.008545600213770937,
    "water use": 0.0812400573350386
  },
  {
    "DB명": "steam production, in chemical industry",
    "국가": "RoW",
    "acidification": 0.001218326815286872,
    "climate change: biogenic": 0.348997605010887,
    "climate change: fossil": 5.923151528231126e-05,
    "climate change: land use and land use change": 0.3488740564619348,
    "climate change": 6.431703366982195e-05,
    "ecotoxicity: freshwater, inorganics": 0.9779751389144945,
    "ecotoxicity: freshwater, organics": 0.9469180407600621,
    "ecotoxicity: freshwater": 0.03105709815443149,
    "energy resources: non-renewable": 4.295883335279258,
    "eutrophication: freshwater": 4.03193406447723e-05,
    "eutrophication: marine": 0.0001856677423800428,
    "eutrophication: terrestrial": 0.001929456515666007,
    "human toxicity: carcinogenic, inorganics": 7.314012688447922e-11,
    "human toxicity: carcinogenic, organics": 2.639239299583354e-11,
    "human toxicity: carcinogenic": 4.674773388864572e-11,
    "human toxicity: non-carcinogenic, inorganics": 1.394415961420798e-09,
    "human toxicity: non-carcinogenic, organics": 1.335479466143914e-09,
    "human toxicity: non-carcinogenic": 5.89364952768824e-11,
    "ionising radiation: human health": 0.002956868557371451,
    "land use": 0.2816917127828304,
    "material resources: metals/minerals": 9.505283378479182e-08,
    "ozone depletion": 4.422546054145843e-09,
    "particulate matter formation": 1.512757072167171e-08,
    "photochemical oxidant formation: human health": 0.0008261148043339584,
    "water use": 0.01250197652609036
  },
  {
    "DB명": "market for tap water",
    "국가": "RoW",
    "acidification": 6.548803729397869e-06,
    "climate change: biogenic": 0.001240890749523278,
    "climate change: fossil": 1.955303630712735e-06,
    "climate change: land use and land use change": 0.001237299126831443,
    "climate change": 1.636319061122303e-06,
    "ecotoxicity: freshwater, inorganics": 0.005425358868837599,
    "ecotoxicity: freshwater, organics": 0.005034746901010667,
    "ecotoxicity: freshwater": 0.0003906119678269244,
    "energy resources: non-renewable": 0.01499824474985496,
    "eutrophication: freshwater": 4.47460954411389e-07,
    "eutrophication: marine": 1.333060318910682e-06,
    "eutrophication: terrestrial": 1.362496615518188e-05,
    "human toxicity: carcinogenic, inorganics": 2.932190776644533e-12,
    "human toxicity: carcinogenic, organics": 1.978226267631667e-12,
    "human toxicity: carcinogenic": 9.539645090128647e-13,
    "human toxicity: non-carcinogenic, inorganics": 4.160963174460445e-11,
    "human toxicity: non-carcinogenic, organics": 4.112615360906181e-11,
    "human toxicity: non-carcinogenic": 4.834781355426373e-13,
    "ionising radiation: human health": 0.0001085427734108322,
    "land use": 0.003083871512604728,
    "material resources: metals/minerals": 5.985751330544954e-09,
    "ozone depletion": 2.406149969792277e-10,
    "particulate matter formation": 8.320388923330052e-11,
    "photochemical oxidant formation: human health": 4.383411628727941e-06,
    "water use": 0.0003241104083011059
  },
  {
    "DB명": "tap water production, underground water without treatment",
    "국가": "RoW",
    "acidification": 1.474049708003459e-06,
    "climate change: biogenic": 0.0002984641946046991,
    "climate change: fossil": 5.117787837206939e-07,
    "climate change: land use and land use change": 0.0002974367730220624,
    "climate change": 5.156427989159919e-07,
    "ecotoxicity: freshwater, inorganics": 0.000763964196211695,
    "ecotoxicity: freshwater, organics": 0.0007052636251365275,
    "ecotoxicity: freshwater": 5.870057107516742e-05,
    "energy resources: non-renewable": 0.003634479222501986,
    "eutrophication: freshwater": 1.034088592089799e-07,
    "eutrophication: marine": 2.988378231904879e-07,
    "eutrophication: terrestrial": 3.066355611596331e-06,
    "human toxicity: carcinogenic, inorganics": 8.089281041693811e-14,
    "human toxicity: carcinogenic, organics": 5.044473095624842e-14,
    "human toxicity: carcinogenic": 3.044807946068967e-14,
    "human toxicity: non-carcinogenic, inorganics": 2.566619912148196e-12,
    "human toxicity: non-carcinogenic, organics": 2.49015316674972e-12,
    "human toxicity: non-carcinogenic": 7.646674539847314e-14,
    "ionising radiation: human health": 3.139973422545573e-05,
    "land use": 0.0007277347352600049,
    "material resources: metals/minerals": 3.992418539013938e-10,
    "ozone depletion": 1.811013690812112e-12,
    "particulate matter formation": 1.53528676052208e-11,
    "photochemical oxidant formation: human health": 9.052199854061844e-07,
    "water use": 6.376230784243411e-05
  },
  {
    "DB명": "transport, freight, sea, bulk carrier for dry goods",
    "국가": "GLO",
    "acidification": 0.0001881023552701557,
    "climate change: biogenic": 0.007084442146282268,
    "climate change: fossil": 1.491140299946688e-06,
    "climate change: land use and land use change": 0.007076212882064766,
    "climate change": 6.738123917555795e-06,
    "ecotoxicity: freshwater, inorganics": 0.04285021806012439,
    "ecotoxicity: freshwater, organics": 0.04086268097818143,
    "ecotoxicity: freshwater": 0.00198753708194291,
    "energy resources: non-renewable": 0.08714971425699718,
    "eutrophication: freshwater": 2.804393412873863e-07,
    "eutrophication: marine": 4.312389686730543e-05,
    "eutrophication: terrestrial": 0.0004779381784388519,
    "human toxicity: carcinogenic, inorganics": 3.459397393892416e-12,
    "human toxicity: carcinogenic, organics": 2.177106934628205e-12,
    "human toxicity: carcinogenic": 1.28229045926421e-12,
    "human toxicity: non-carcinogenic, inorganics": 2.681521009409985e-11,
    "human toxicity: non-carcinogenic, organics": 2.537732263717733e-11,
    "human toxicity: non-carcinogenic": 1.437887456922546e-12,
    "ionising radiation: human health": 4.927714417437317e-05,
    "land use": 0.006820817439116442,
    "material resources: metals/minerals": 8.411315564112028e-09,
    "ozone depletion": 1.070149589135456e-10,
    "particulate matter formation": 2.072313316823518e-10,
    "photochemical oxidant formation: human health": 0.0001323744992788875,
    "water use": 0.0002868057629415415
  },
  {
    "DB명": "transport, freight, sea, container ship",
    "국가": "GLO",
    "acidification": 0.0003026048890479922,
    "climate change: biogenic": 0.01016351302910071,
    "climate change: fossil": 1.82223513906984e-06,
    "climate change: land use and land use change": 0.01015385339647313,
    "climate change": 7.837397488514437e-06,
    "ecotoxicity: freshwater, inorganics": 0.06142342716445788,
    "ecotoxicity: freshwater, organics": 0.05872338599250172,
    "ecotoxicity: freshwater": 0.002700041171956223,
    "energy resources: non-renewable": 0.125236661119668,
    "eutrophication: freshwater": 3.381542793440568e-07,
    "eutrophication: marine": 7.558721019237289e-05,
    "eutrophication: terrestrial": 0.0008361894873699992,
    "human toxicity: carcinogenic, inorganics": 4.397548953171948e-12,
    "human toxicity: carcinogenic, organics": 2.829214118800389e-12,
    "human toxicity: carcinogenic": 1.56833483437156e-12,
    "human toxicity: non-carcinogenic, inorganics": 3.612587245674277e-11,
    "human toxicity: non-carcinogenic, organics": 3.413960121089943e-11,
    "human toxicity: non-carcinogenic": 1.986271245843335e-12,
    "ionising radiation: human health": 5.974174610261922e-05,
    "land use": 0.009200837264791024,
    "material resources: metals/minerals": 9.92416164024781e-09,
    "ozone depletion": 1.536341959643097e-10,
    "particulate matter formation": 2.979427122463178e-10,
    "photochemical oxidant formation: human health": 0.0002258552647685388,
    "water use": 0.0003528614277838889
  },
  {
    "DB명": "Rayon fabric, Cross linked polyacrylic acid sodium salt, Copper wire",
    "국가": "-",
    "acidification": 0.11960057891328366,
    "climate change: biogenic": 3.423908765489374,
    "climate change: fossil": 0.016993822468087845,
    "climate change: land use and land use change": 3.402001533320062,
    "climate change": 0.0049134097012248565,
    "ecotoxicity: freshwater, inorganics": 97.49629619465188,
    "ecotoxicity: freshwater, organics": 96.19836084372433,
    "ecotoxicity: freshwater": 1.2979353509277476,
    "energy resources: non-renewable": 50.008304988592805,
    "eutrophication: freshwater": 0.00558885072934536,
    "eutrophication: marine": 0.005945331915963585,
    "eutrophication: terrestrial": 0.07482566905579388,
    "human toxicity: carcinogenic, inorganics": 1.7900614686844752e-08,
    "human toxicity: carcinogenic, organics": 1.7284585935839884e-08,
    "human toxicity: carcinogenic": 6.160287510048775e-10,
    "human toxicity: non-carcinogenic, inorganics": 1.5562522086452152e-06,
    "human toxicity: non-carcinogenic, organics": 1.4807127378461652e-06,
    "human toxicity: non-carcinogenic": 7.553947079905002e-08,
    "ionising radiation: human health": 0.28290073386328823,
    "land use": 88.11155901912116,
    "material resources: metals/minerals": 0.0014449958678558715,
    "ozone depletion": 2.779974418114351e-07,
    "particulate matter formation": 4.01987718868156e-07,
    "photochemical oxidant formation: human health": 0.024201916637210875,
    "water use": 2.5592101568218935
  },
  {
    "DB명": "fibre production, viscose",
    "국가": "GLO",
    "acidification": 0.03498790304702176,
    "climate change: biogenic": 3.253854319835082,
    "climate change: fossil": 0.02771152125493032,
    "climate change: land use and land use change": 3.221055550215913,
    "climate change": 0.00508724836423805,
    "ecotoxicity: freshwater, inorganics": 31.57510517741169,
    "ecotoxicity: freshwater, organics": 30.13899671915643,
    "ecotoxicity: freshwater": 1.43610845825526,
    "energy resources: non-renewable": 38.23905840572085,
    "eutrophication: freshwater": 0.001185617940066284,
    "eutrophication: marine": 0.003807624353025353,
    "eutrophication: terrestrial": 0.03931768304953312,
    "human toxicity: carcinogenic, inorganics": 1.5443566991389e-09,
    "human toxicity: carcinogenic, organics": 9.074277102825942e-10,
    "human toxicity: carcinogenic": 6.369289888563061e-10,
    "human toxicity: non-carcinogenic, inorganics": 4.929204323340738e-08,
    "human toxicity: non-carcinogenic, organics": 4.762387580401881e-08,
    "human toxicity: non-carcinogenic": 1.66816742938856e-09,
    "ionising radiation: human health": 0.2444869382655149,
    "land use": 115.039289031324,
    "material resources: metals/minerals": 3.664276716482193e-05,
    "ozone depletion": 5.448863110714334e-07,
    "particulate matter formation": 3.885540050645246e-07,
    "photochemical oxidant formation: human health": 0.01290093586394297,
    "water use": 2.756970682739676
  },
  {
    "DB명": "electrorefining of copper, anode",
    "국가": "GLO",
    "acidification": 0.76523886065726,
    "climate change: biogenic": 8.39994405604269,
    "climate change: fossil": 0.0215506277769425,
    "climate change: land use and land use change": 8.361238745925345,
    "climate change": 0.01715468234040273,
    "ecotoxicity: freshwater, inorganics": 617.4735628328046,
    "ecotoxicity: freshwater, organics": 614.6122369937756,
    "ecotoxicity: freshwater": 2.861325839030615,
    "energy resources: non-renewable": 104.8348381607304,
    "eutrophication: freshwater": 0.03740824971362597,
    "eutrophication: marine": 0.02884216482491367,
    "eutrophication: terrestrial": 0.3990752828263451,
    "human toxicity: carcinogenic, inorganics": 1.292152227686405e-07,
    "human toxicity: carcinogenic, organics": 1.271190855315771e-07,
    "human toxicity: carcinogenic": 2.09613723706346e-09,
    "human toxicity: non-carcinogenic, inorganics": 1.159464409636417e-05,
    "human toxicity: non-carcinogenic, organics": 1.103055767943345e-05,
    "human toxicity: non-carcinogenic": 5.640864169307188e-07,
    "ionising radiation: human health": 0.9326364505766089,
    "land use": 241.9800248037117,
    "material resources: metals/minerals": 0.01079899854270452,
    "ozone depletion": 9.506786682187079e-08,
    "particulate matter formation": 1.489670175197735e-06,
    "photochemical oxidant formation: human health": 0.1251382499449192,
    "water use": 7.883200031061689
  },
  {
    "DB명": "chromium steel 18/8+glass fibre production",
    "국가": "RER",
    "acidification": 0.028767008843632168,
    "climate change: biogenic": 5.1212164195269905,
    "climate change: fossil": 0.007681399277767852,
    "climate change: land use and land use change": 5.1081125717463145,
    "climate change": 0.005422448502908585,
    "ecotoxicity: freshwater, inorganics": 20.757998522218745,
    "ecotoxicity: freshwater, organics": 19.599354595282044,
    "ecotoxicity: freshwater": 1.1586439269367075,
    "energy resources: non-renewable": 58.09191047078812,
    "eutrophication: freshwater": 0.0017783529385770216,
    "eutrophication: marine": 0.005246412836772593,
    "eutrophication: terrestrial": 0.05548712526596009,
    "human toxicity: carcinogenic, inorganics": 3.279731400963105e-08,
    "human toxicity: carcinogenic, organics": 2.8008087928944957e-08,
    "human toxicity: carcinogenic": 4.7892260806860945e-09,
    "human toxicity: non-carcinogenic, inorganics": 1.193466621557927e-07,
    "human toxicity: non-carcinogenic, organics": 1.1730306787004466e-07,
    "human toxicity: non-carcinogenic": 2.043594285748044e-09,
    "ionising radiation: human health": 0.34734967330578487,
    "land use": 26.96635814947767,
    "material resources: metals/minerals": 0.00012773217976730356,
    "ozone depletion": 5.457176809069046e-08,
    "particulate matter formation": 4.125197561600841e-07,
    "photochemical oxidant formation: human health": 0.019233382639782942,
    "water use": 1.6627730520376984
  },
  {
    "DB명": "steel production, chromium steel 18/8, hot rolled",
    "국가": "RER",
    "acidification": 0.02889318947718707,
    "climate change: biogenic": 5.151144731345814,
    "climate change: fossil": 0.007720589671137274,
    "climate change: land use and land use change": 5.137967305296828,
    "climate change": 0.00545683637784894,
    "ecotoxicity: freshwater, inorganics": 20.89163618963335,
    "ecotoxicity: freshwater, organics": 19.72491380412108,
    "ecotoxicity: freshwater": 1.166722385512273,
    "energy resources: non-renewable": 58.33810389197529,
    "eutrophication: freshwater": 0.001789189349895654,
    "eutrophication: marine": 0.005266095622704055,
    "eutrophication: terrestrial": 0.05569579096132352,
    "human toxicity: carcinogenic, inorganics": 3.31062479385841e-08,
    "human toxicity: carcinogenic, organics": 2.827109247420932e-08,
    "human toxicity: carcinogenic": 4.835155464374784e-09,
    "human toxicity: non-carcinogenic, inorganics": 1.191958245896515e-07,
    "human toxicity: non-carcinogenic, organics": 1.17143910386177e-07,
    "human toxicity: non-carcinogenic": 2.051914203474527e-09,
    "ionising radiation: human health": 0.3468890881132596,
    "land use": 27.18247405715255,
    "material resources: metals/minerals": 0.0001260724726360088,
    "ozone depletion": 5.456489512954308e-08,
    "particulate matter formation": 4.156593578788712e-07,
    "photochemical oxidant formation: human health": 0.01931835302821705,
    "water use": 1.672521942594404
  },
  {
    "DB명": "glass fibre production",
    "국가": "RER",
    "acidification": 0.01627512612169681,
    "climate change: biogenic": 2.158313549463509,
    "climate change: fossil": 0.003801550334195096,
    "climate change: land use and land use change": 2.1524939502455,
    "climate change": 0.002018048883813477,
    "ecotoxicity: freshwater, inorganics": 7.527869448173218,
    "ecotoxicity: freshwater, organics": 7.168992920217506,
    "ecotoxicity: freshwater": 0.3588765279557209,
    "energy resources: non-renewable": 33.71876177325862,
    "eutrophication: freshwater": 0.0007055482180324293,
    "eutrophication: marine": 0.003297817029557798,
    "eutrophication: terrestrial": 0.03482922142498045,
    "human toxicity: carcinogenic, inorganics": 2.212855043278933e-09,
    "human toxicity: carcinogenic, organics": 1.970637947773176e-09,
    "human toxicity: carcinogenic": 2.422170955057556e-10,
    "human toxicity: non-carcinogenic, inorganics": 1.342795812037702e-07,
    "human toxicity: non-carcinogenic, organics": 1.330596587729438e-07,
    "human toxicity: non-carcinogenic": 1.219922430826236e-09,
    "ionising radiation: human health": 0.3929476073657873,
    "land use": 5.570883289664645,
    "material resources: metals/minerals": 0.0002920431857654827,
    "ozone depletion": 5.525219124428202e-08,
    "particulate matter formation": 1.016991860001584e-07,
    "photochemical oxidant formation: human health": 0.01082131418480644,
    "water use": 0.6976328869238415
  },
  {
    "DB명": "Copper, cathode",
    "국가": "RoW",
    "acidification": 0.6997461233961606,
    "climate change: biogenic": 7.680969246657977,
    "climate change: fossil": 0.025184671637298085,
    "climate change: land use and land use change": 7.639255983958733,
    "climate change": 0.01652859106195677,
    "ecotoxicity: freshwater, inorganics": 582.1547304254038,
    "ecotoxicity: freshwater, organics": 580.2257747491055,
    "ecotoxicity: freshwater": 1.928955676300732,
    "energy resources: non-renewable": 96.69928311156941,
    "eutrophication: freshwater": 0.03333526880759813,
    "eutrophication: marine": 0.02717821780519694,
    "eutrophication: terrestrial": 0.38818952491662934,
    "human toxicity: carcinogenic, inorganics": 1.3202011133774906e-07,
    "human toxicity: carcinogenic, organics": 1.30038076172391e-07,
    "human toxicity: carcinogenic": 1.9820351653581318e-09,
    "human toxicity: non-carcinogenic, inorganics": 1.2188302852990613e-05,
    "human toxicity: non-carcinogenic, organics": 7.527802373024917e-06,
    "human toxicity: non-carcinogenic": 5.818228898032682e-07,
    "ionising radiation: human health": 0.8550480524693187,
    "land use": 254.73483759159356,
    "material resources: metals/minerals": 0.011541578048780267,
    "ozone depletion": 8.600623787466369e-08,
    "particulate matter formation": 1.3428178810457366e-06,
    "photochemical oxidant formation: human health": 0.11694947607090814,
    "water use": 3.618375634618254
  },
  {
    "DB명": "Rayon fabric, Cross linked polyacrylic acid sodium salt",
    "국가": "-",
    "acidification": 0.024168056598951836,
    "climate change: biogenic": 2.782922351428539,
    "climate change: fossil": 0.018538966826540066,
    "climate change: land use and land use change": 2.7609307122366853,
    "climate change": 0.0034526723653133546,
    "ecotoxicity: freshwater, inorganics": 21.07382109064366,
    "ecotoxicity: freshwater, organics": 19.939703002149187,
    "ecotoxicity: freshwater": 1.1341180884944753,
    "energy resources: non-renewable": 41.00545923997214,
    "eutrophication: freshwater": 0.0008398596880442385,
    "eutrophication: marine": 0.002730144692235804,
    "eutrophication: terrestrial": 0.028267790196479355,
    "human toxicity: carcinogenic, inorganics": 1.1003630338659266e-09,
    "human toxicity: carcinogenic, organics": 6.609772685701343e-10,
    "human toxicity: carcinogenic": 4.3938576529579257e-10,
    "human toxicity: non-carcinogenic, inorganics": 3.493506115416652e-08,
    "human toxicity: non-carcinogenic, organics": 3.353890549456113e-08,
    "human toxicity: non-carcinogenic": 1.396155659605382e-09,
    "ionising radiation: human health": 0.19602681793019996,
    "land use": 74.60229538363049,
    "material resources: metals/minerals": 2.658735983278183e-05,
    "ozone depletion": 3.526688120251351e-07,
    "particulate matter formation": 2.6653283941983974e-07,
    "photochemical oxidant formation: human health": 0.009660262093409613,
    "water use": 1.947857195069249
  },
  {
    "DB명": "kraft paper production",
    "국가": "RoW",
    "acidification": 0.006104896162041702,
    "climate change: biogenic": 0.9429393189756768,
    "climate change: fossil": 0.03006644543096794,
    "climate change: land use and land use change": 0.9094789865325822,
    "climate change": 0.003393887012126772,
    "ecotoxicity: freshwater, inorganics": 5.844475343889573,
    "ecotoxicity: freshwater, organics": 4.936286780212249,
    "ecotoxicity: freshwater": 0.9081885636773188,
    "energy resources: non-renewable": 10.86175011230605,
    "eutrophication: freshwater": 0.001777179509355004,
    "eutrophication: marine": 0.002366206665328505,
    "eutrophication: terrestrial": 0.01853194601575411,
    "human toxicity: carcinogenic, inorganics": 6.005942354912088e-10,
    "human toxicity: carcinogenic, organics": 3.132903274388561e-10,
    "human toxicity: carcinogenic": 2.873039080523534e-10,
    "human toxicity: non-carcinogenic, inorganics": 1.097971801059375e-08,
    "human toxicity: non-carcinogenic, organics": 1.043709351652727e-08,
    "human toxicity: non-carcinogenic": 5.426244940664753e-10,
    "ionising radiation: human health": 0.05451247919996306,
    "land use": 238.6936116057079,
    "material resources: metals/minerals": 3.712310720102384e-06,
    "ozone depletion": 1.725586597536216e-08,
    "particulate matter formation": 6.314335354895219e-08,
    "photochemical oxidant formation: human health": 0.005401449755129148,
    "water use": 0.5568652336447707
  },
  {
    "DB명": "nylon 6-6 production",
    "국가": "RoW",
    "acidification": 0.03550699861014575,
    "climate change: biogenic": 8.22872237854184,
    "climate change: fossil": 0.008334869917959519,
    "climate change: land use and land use change": 8.220375333020788,
    "climate change": 1.217560309303082e-05,
    "ecotoxicity: freshwater, inorganics": 8.64358236117717,
    "ecotoxicity: freshwater, organics": 6.727766657368409,
    "ecotoxicity: freshwater": 1.915815703808752,
    "energy resources: non-renewable": 128.9220217960538,
    "eutrophication: freshwater": 0.0004418517492404292,
    "eutrophication: marine": 0.0136002470670914,
    "eutrophication: terrestrial": 0.0671458929591999,
    "human toxicity: carcinogenic, inorganics": 7.333572372308712e-10,
    "human toxicity: carcinogenic, organics": 7.127253864494591e-10,
    "human toxicity: carcinogenic": 2.063185078141238e-11,
    "human toxicity: non-carcinogenic, inorganics": 7.082929010270977e-09,
    "human toxicity: non-carcinogenic, organics": 3.99579720363779e-09,
    "human toxicity: non-carcinogenic": 3.087131806633185e-09,
    "ionising radiation: human health": 0.0005148032684637021,
    "land use": 0.1157863030026106,
    "material resources: metals/minerals": 3.398505223036284e-06,
    "ozone depletion": 1.603398291858807e-09,
    "particulate matter formation": 3.533542975168737e-07,
    "photochemical oxidant formation: human health": 0.0204755610901608,
    "water use": 9.726354884840223
  },
  {
    "DB명": "Copper, cathode",
    "국가": "AU",
    "acidification": 0.7086895128418595,
    "climate change: biogenic": 8.913662972503863,
    "climate change: fossil": 0.01897977741244305,
    "climate change: land use and land use change": 8.884722048261445,
    "climate change": 0.00996114682998593,
    "ecotoxicity: freshwater, inorganics": 427.72053422241714,
    "ecotoxicity: freshwater, organics": 425.8524252010187,
    "ecotoxicity: freshwater": 1.8681090214010068,
    "energy resources: non-renewable": 102.0078870000646,
    "eutrophication: freshwater": 0.03897444783964606,
    "eutrophication: marine": 0.03006164618344063,
    "eutrophication: terrestrial": 0.41787392013840563,
    "human toxicity: carcinogenic, inorganics": 1.3219315583061182e-07,
    "human toxicity: carcinogenic, organics": 1.3027650875842696e-07,
    "human toxicity: carcinogenic": 1.9166470721849227e-09,
    "human toxicity: non-carcinogenic, inorganics": 1.2213381505031477e-05,
    "human toxicity: non-carcinogenic, organics": 7.540802192021066e-06,
    "human toxicity: non-carcinogenic": 5.93901722847983e-07,
    "ionising radiation: human health": 0.5523524793357427,
    "land use": 258.6257475834349,
    "material resources: metals/minerals": 0.012050062076394858,
    "ozone depletion": 8.153522661421283e-08,
    "particulate matter formation": 1.359331523740057e-06,
    "photochemical oxidant formation: human health": 0.12248379774296976,
    "water use": 3.2696705588394384
  },
  {
    "DB명": "Copper, cathode",
    "국가": "CA",
    "acidification": 0.715587086847661,
    "climate change: biogenic": 7.949551852866387,
    "climate change: fossil": 0.02803629030843921,
    "climate change: land use and land use change": 7.856967156380153,
    "climate change": 0.06454840617780354,
    "ecotoxicity: freshwater, inorganics": 1645.800607226167,
    "ecotoxicity: freshwater, organics": 1643.2027647203965,
    "ecotoxicity: freshwater": 2.597842505772478,
    "energy resources: non-renewable": 106.8986821631894,
    "eutrophication: freshwater": 0.06789181924694865,
    "eutrophication: marine": 0.03233920045365714,
    "eutrophication: terrestrial": 0.45951914380915626,
    "human toxicity: carcinogenic, inorganics": 1.3772473684462377e-07,
    "human toxicity: carcinogenic, organics": 1.3483033209284049e-07,
    "human toxicity: carcinogenic": 2.8944047517833544e-09,
    "human toxicity: non-carcinogenic, inorganics": 1.2860151054498768e-05,
    "human toxicity: non-carcinogenic, organics": 7.594710544550236e-06,
    "human toxicity: non-carcinogenic": 1.1867629197861042e-06,
    "ionising radiation: human health": 1.8458365499819478,
    "land use": 493.239769111782,
    "material resources: metals/minerals": 0.012024663308755288,
    "ozone depletion": 8.501722788497915e-08,
    "particulate matter formation": 1.5404864181488031e-06,
    "photochemical oxidant formation: human health": 0.1303760009361235,
    "water use": 8.699611003327048
  },
  {
    "DB명": "Copper, cathode",
    "국가": "CL",
    "acidification": 0.7913491372618027,
    "climate change: biogenic": 7.376716587581444,
    "climate change: fossil": 0.015157103109842425,
    "climate change: land use and land use change": 7.35383164578412,
    "climate change": 0.007727838687474626,
    "ecotoxicity: freshwater, inorganics": 284.8215349982603,
    "ecotoxicity: freshwater, organics": 283.0485197959013,
    "ecotoxicity: freshwater": 1.7730152023607149,
    "energy resources: non-renewable": 86.07152443761746,
    "eutrophication: freshwater": 0.035968868410773805,
    "eutrophication: marine": 0.028301452485480896,
    "eutrophication: terrestrial": 0.39606602128770524,
    "human toxicity: carcinogenic, inorganics": 1.2944748769959768e-07,
    "human toxicity: carcinogenic, organics": 1.2760192515533303e-07,
    "human toxicity: carcinogenic": 1.8455625442647533e-09,
    "human toxicity: non-carcinogenic, inorganics": 1.2066571590116516e-05,
    "human toxicity: non-carcinogenic, organics": 1.1460179721252592e-05,
    "human toxicity: non-carcinogenic": 6.063918688639026e-07,
    "ionising radiation: human health": 0.4232102926697159,
    "land use": 261.90762535651464,
    "material resources: metals/minerals": 0.010786163745630255,
    "ozone depletion": 8.159467674182787e-08,
    "particulate matter formation": 1.433188118401194e-06,
    "photochemical oxidant formation: human health": 0.12446328593262143,
    "water use": 2.7904628679394308
  },
  {
    "DB명": "Copper, cathode",
    "국가": "CN",
    "acidification": 0.7519965396854298,
    "climate change: biogenic": 7.855448956762617,
    "climate change: fossil": 0.014330234724591006,
    "climate change: land use and land use change": 7.832415300434998,
    "climate change": 0.008703421603031619,
    "ecotoxicity: freshwater, inorganics": 410.7059685802203,
    "ecotoxicity: freshwater, organics": 409.1271043790294,
    "ecotoxicity: freshwater": 1.5788642011941896,
    "energy resources: non-renewable": 85.44802473681327,
    "eutrophication: freshwater": 0.023029844876723316,
    "eutrophication: marine": 0.02598369010511001,
    "eutrophication: terrestrial": 0.3690868935762084,
    "human toxicity: carcinogenic, inorganics": 1.4081271613866682e-07,
    "human toxicity: carcinogenic, organics": 1.3929800528685634e-07,
    "human toxicity: carcinogenic": 1.5147108518103178e-09,
    "human toxicity: non-carcinogenic, inorganics": 1.270336322966987e-05,
    "human toxicity: non-carcinogenic, organics": 1.2311309170212758e-05,
    "human toxicity: non-carcinogenic": 3.920540594571048e-07,
    "ionising radiation: human health": 0.5494192670300722,
    "land use": 179.15489476451754,
    "material resources: metals/minerals": 0.012095879501773201,
    "ozone depletion": 5.6586295474306607e-08,
    "particulate matter formation": 1.463469793059e-06,
    "photochemical oxidant formation: human health": 0.11652660262920336,
    "water use": 2.8252270616837603
  },
  {
    "DB명": "Copper, cathode",
    "국가": "ID",
    "acidification": 0.2814292998760648,
    "climate change: biogenic": 11.045973472401315,
    "climate change: fossil": 0.0281639122176163,
    "climate change: land use and land use change": 11.000987557005544,
    "climate change": 0.016822003178157918,
    "ecotoxicity: freshwater, inorganics": 1270.3002857578117,
    "ecotoxicity: freshwater, organics": 1268.1113681514091,
    "ecotoxicity: freshwater": 2.188917606407258,
    "energy resources: non-renewable": 122.32444265702163,
    "eutrophication: freshwater": 0.04534505582724448,
    "eutrophication: marine": 0.03666593086258586,
    "eutrophication: terrestrial": 0.4983994204464893,
    "human toxicity: carcinogenic, inorganics": 1.4623305083820428e-07,
    "human toxicity: carcinogenic, organics": 1.4412782946653465e-07,
    "human toxicity: carcinogenic": 2.1052213716696777e-09,
    "human toxicity: non-carcinogenic, inorganics": 1.311948728483616e-05,
    "human toxicity: non-carcinogenic, organics": 1.2470505285605345e-05,
    "human toxicity: non-carcinogenic": 6.489819992307919e-07,
    "ionising radiation: human health": 0.5015076290423118,
    "land use": 282.7791820319444,
    "material resources: metals/minerals": 0.013988976277155932,
    "ozone depletion": 8.790217303212905e-08,
    "particulate matter formation": 1.3872884219504142e-06,
    "photochemical oxidant formation: human health": 0.11209972471028354,
    "water use": 3.8491229639006668
  },
  {
    "DB명": "Copper, cathode",
    "국가": "KZ",
    "acidification": 0.6956180204907363,
    "climate change: biogenic": 6.905320980367119,
    "climate change: fossil": 0.01511568488138718,
    "climate change: land use and land use change": 6.881331352877166,
    "climate change": 0.008873942608574286,
    "ecotoxicity: freshwater, inorganics": 215.88251510882782,
    "ecotoxicity: freshwater, organics": 214.5362253389829,
    "ecotoxicity: freshwater": 1.346289769847388,
    "energy resources: non-renewable": 79.1417672866945,
    "eutrophication: freshwater": 0.013371565734287747,
    "eutrophication: marine": 0.0251982592985207,
    "eutrophication: terrestrial": 0.3675165098123068,
    "human toxicity: carcinogenic, inorganics": 1.2848751552664845e-07,
    "human toxicity: carcinogenic, organics": 1.2722992806684851e-07,
    "human toxicity: carcinogenic": 1.2575874598000027e-09,
    "human toxicity: non-carcinogenic, inorganics": 1.1777586172857992e-05,
    "human toxicity: non-carcinogenic, organics": 7.4862417748151385e-06,
    "human toxicity: non-carcinogenic": 2.1266680788042483e-07,
    "ionising radiation: human health": 0.5163544206344084,
    "land use": 104.8138006428227,
    "material resources: metals/minerals": 0.012032069805463414,
    "ozone depletion": 6.226600195952524e-08,
    "particulate matter formation": 1.2791480026293292e-06,
    "photochemical oxidant formation: human health": 0.1118000725287871,
    "water use": 2.461986317285688
  },
  {
    "DB명": "Copper, cathode",
    "국가": "RU",
    "acidification": 2.053751025133349,
    "climate change: biogenic": 8.83680341849109,
    "climate change: fossil": 0.017769381697176432,
    "climate change: land use and land use change": 8.802752396434624,
    "climate change": 0.01628164035929857,
    "ecotoxicity: freshwater, inorganics": 491.93474116777503,
    "ecotoxicity: freshwater, organics": 489.8600219286067,
    "ecotoxicity: freshwater": 2.074719239170694,
    "energy resources: non-renewable": 114.76397006264678,
    "eutrophication: freshwater": 0.03541000859334944,
    "eutrophication: marine": 0.03139633640294759,
    "eutrophication: terrestrial": 0.45273843119308654,
    "human toxicity: carcinogenic, inorganics": 1.319917985858688e-07,
    "human toxicity: carcinogenic, organics": 1.2987864921419162e-07,
    "human toxicity: carcinogenic": 2.113149371677082e-09,
    "human toxicity: non-carcinogenic, inorganics": 1.2176409430635315e-05,
    "human toxicity: non-carcinogenic, organics": 1.158137889358998e-05,
    "human toxicity: non-carcinogenic": 5.950305370452758e-07,
    "ionising radiation: human health": 1.236763888130168,
    "land use": 262.29962372842675,
    "material resources: metals/minerals": 0.013862996146728819,
    "ozone depletion": 8.499627329370089e-08,
    "particulate matter formation": 2.5269692307438983e-06,
    "photochemical oxidant formation: human health": 0.2135705603958493,
    "water use": 3.882592570918741
  },
  {
    "DB명": "Copper, cathode",
    "국가": "US",
    "acidification": 0.6984960480404345,
    "climate change: biogenic": 8.178640799535842,
    "climate change: fossil": 0.020113705864315466,
    "climate change: land use and land use change": 8.147451146267095,
    "climate change": 0.011075947404440026,
    "ecotoxicity: freshwater, inorganics": 722.480441216301,
    "ecotoxicity: freshwater, organics": 720.275892569159,
    "ecotoxicity: freshwater": 2.204548647144553,
    "energy resources: non-renewable": 109.54289707942957,
    "eutrophication: freshwater": 0.05188789822428277,
    "eutrophication: marine": 0.027206502142463684,
    "eutrophication: terrestrial": 0.38226625675926224,
    "human toxicity: carcinogenic, inorganics": 1.3461887824097495e-07,
    "human toxicity: carcinogenic, organics": 1.3215157165129034e-07,
    "human toxicity: carcinogenic": 2.467306589684698e-09,
    "human toxicity: non-carcinogenic, inorganics": 1.2525400686655213e-05,
    "human toxicity: non-carcinogenic, organics": 7.553789352768866e-06,
    "human toxicity: non-carcinogenic": 8.929337437239186e-07,
    "ionising radiation: human health": 1.3265328565852914,
    "land use": 382.1482986393868,
    "material resources: metals/minerals": 0.010810163621280004,
    "ozone depletion": 7.538329461299274e-08,
    "particulate matter formation": 1.3843004185647985e-06,
    "photochemical oxidant formation: human health": 0.11654423675909599,
    "water use": 3.8513677360197414
  },
  {
    "DB명": "Copper, cathode",
    "국가": "ZM",
    "acidification": 0.6913861623181318,
    "climate change: biogenic": 5.808713683445196,
    "climate change: fossil": 0.0159737352842301,
    "climate change: land use and land use change": 5.783582623466766,
    "climate change": 0.009157324694207674,
    "ecotoxicity: freshwater, inorganics": 715.0516520494024,
    "ecotoxicity: freshwater, organics": 713.5019422137824,
    "ecotoxicity: freshwater": 1.549709835623014,
    "energy resources: non-renewable": 68.1985871265955,
    "eutrophication: freshwater": 0.02137718015218041,
    "eutrophication: marine": 0.025276348080762585,
    "eutrophication: terrestrial": 0.37163490192568915,
    "human toxicity: carcinogenic, inorganics": 1.2994594253873778e-07,
    "human toxicity: carcinogenic, organics": 1.284426892157504e-07,
    "human toxicity: carcinogenic": 1.5032533229874472e-09,
    "human toxicity: non-carcinogenic, inorganics": 1.1940303603588573e-05,
    "human toxicity: non-carcinogenic, organics": 7.497089458219342e-06,
    "human toxicity: non-carcinogenic": 3.645365552068034e-07,
    "ionising radiation: human health": 0.5280515432026004,
    "land use": 164.3228750793079,
    "material resources: metals/minerals": 0.012035639329436095,
    "ozone depletion": 6.038979260008985e-08,
    "particulate matter formation": 1.2730739600831256e-06,
    "photochemical oxidant formation: human health": 0.11160439761293615,
    "water use": 2.6595798321239714
  }
]



# ─── 기본 DB 데이터 ────────────────────────────────
def load_db_data():
    """DB 데이터를 파일에서 로드하거나 기본 데이터를 반환"""
    try:
        if os.path.exists('db_data.json'):
            with open('db_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return pd.DataFrame(data)
        else:
            # 기본 데이터 생성
            default_data = [
                {"물질명": "철", "DB명": "Iron_DB", "국가": "한국", "단위": "kg"},
                {"물질명": "알루미늄", "DB명": "Al_DB", "국가": "일본", "단위": "ton"},
                {"물질명": "전기", "DB명": "Electricity_DB", "국가": "독일", "단위": "kWh"},
                {"물질명": "물", "DB명": "Water_DB", "국가": "미국", "단위": "L"},
            ]
            sample_db_data = pd.DataFrame(default_data).assign(분류="원료물질")
            # 기본 데이터를 파일로 저장
            save_db_data(sample_db_data)
            return sample_db_data
    except Exception as e:
        print(f"DB 데이터 로드 중 오류: {e}")
        # 오류 시 기본 데이터 반환
        return pd.DataFrame([
            {"물질명": "철", "DB명": "Iron_DB", "국가": "한국", "단위": "kg"},
            {"물질명": "알루미늄", "DB명": "Al_DB", "국가": "일본", "단위": "ton"},
            {"물질명": "전기", "DB명": "Electricity_DB", "국가": "독일", "단위": "kWh"},
            {"물질명": "물", "DB명": "Water_DB", "국가": "미국", "단위": "L"},
        ]).assign(분류="원료물질")

def save_db_data(data):
    """DB 데이터를 파일로 저장"""
    try:
        if isinstance(data, pd.DataFrame):
            data_dict = data.to_dict('records')
        else:
            data_dict = data
        with open('db_data.json', 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=2)
        print("DB 데이터가 성공적으로 저장되었습니다.")
    except Exception as e:
        print(f"DB 데이터 저장 중 오류: {e}")

def load_material_data():
    """투입물 데이터를 파일에서 로드하거나 빈 리스트를 반환"""
    try:
        if os.path.exists('material_data.json'):
            with open('material_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        else:
            return []
    except Exception as e:
        print(f"투입물 데이터 로드 중 오류: {e}")
        return []

def save_material_data_to_file(data):
    """투입물 데이터를 파일로 저장"""
    try:
        with open('material_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("투입물 데이터가 성공적으로 저장되었습니다.")
    except Exception as e:
        print(f"투입물 데이터 저장 중 오류: {e}")

# 초기 DB 데이터 로드
sample_db_data = load_db_data()

# ─── 영향범주(25개) 데이터 ──────────────────────────
impact_categories = [
    ("acidification", "mol H+-Eq"),
    ("climate change: biogenic", "kg CO2-Eq"),
    ("climate change: fossil", "kg CO2-Eq"),
    ("climate change: land use and land use change", "kg CO2-Eq"),
    ("climate change", "kg CO2-Eq"),
    ("ecotoxicity: freshwater, inorganics", "CTUe"),
    ("ecotoxicity: freshwater, organics", "CTUe"),
    ("ecotoxicity: freshwater", "CTUe"),
    ("energy resources: non-renewable", "MJ, net calorific value"),
    ("eutrophication: freshwater", "kg P-Eq"),
    ("eutrophication: marine", "kg N-Eq"),
    ("eutrophication: terrestrial", "mol N-Eq"),
    ("human toxicity: carcinogenic, inorganics", "CTUh"),
    ("human toxicity: carcinogenic, organics", "CTUh"),
    ("human toxicity: carcinogenic", "CTUh"),
    ("human toxicity: non-carcinogenic, inorganics", "CTUh"),
    ("human toxicity: non-carcinogenic, organics", "CTUh"),
    ("human toxicity: non-carcinogenic", "CTUh"),
    ("ionising radiation: human health", "kBq U235-Eq"),
    ("land use", "dimensionless"),
    ("material resources: metals/minerals", "kg Sb-Eq"),
    ("ozone depletion", "kg CFC-11-Eq"),
    ("particulate matter formation", "disease incidence"),
    ("photochemical oxidant formation: human health", "kg NMVOC-Eq"),
    ("water use", "m3 world Eq deprived"),
]

# ─── LCA 분석결과 표 컬럼(분류별로 변경) ──────────────
lca_columns = [
    {"name": "No.", "id": "no"},
    {"name": "Impact category", "id": "impact"},
    {"name": "Unit", "id": "unit"},
    {"name": "TOTAL", "id": "total"},
    {"name": "원료물질", "id": "raw_material"},
    {"name": "보조물질", "id": "additive"},
    {"name": "에너지", "id": "energy"},
    {"name": "유틸리티", "id": "utility"},
    {"name": "수송", "id": "transport"},
    {"name": "폐기물처리", "id": "waste"},
]

# ─── 사이드바 ────────────────────────────────────────
sidebar = html.Div(
    [
        html.H2("LCA 분석", className="display-6", style={
            "fontSize": "1.5rem",
            "color": "#2d3748",
            "fontWeight": "600",
            "marginBottom": "1rem"
        }),
        html.Hr(style={"borderColor": "#e2e8f0", "marginBottom": "1.5rem"}),
        dbc.Nav(
            [
                dbc.NavLink([
                    html.I(className="fas fa-chart-line me-2"),
                    "대시보드"
                ], href="/", active="exact", className="nav-link"),
                dbc.NavLink([
                    html.I(className="fas fa-plus-circle me-2"),
                    "투입물 입력"
                ], href="/inputs", active="exact", className="nav-link"),
                dbc.NavLink([
                    html.I(className="fas fa-database me-2"),
                    "DB 관리"
                ], href="/db", active="exact", className="nav-link"),
                dbc.NavLink([
                    html.I(className="fas fa-chart-bar me-2"),
                    "LCA 분석결과"
                ], href="/lca", active="exact", className="nav-link"),
            ],
            vertical=True,
            pills=True,
            className="sidebar"
        ),
    ],
    style={
        "position": "fixed",
        "top": 0, "left": 0, "bottom": 0,
        "width": "16rem", "padding": "2rem 1rem",
        "zIndex": "1000"
    },
)

# ─── 앱 레이아웃 ──────────────────────────────────────

external_stylesheets = [
    "https://fonts.googleapis.com/css?family=Roboto:400,500,700&display=swap",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
    dbc.themes.BOOTSTRAP,
    "/assets/custom.css"
]

server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

login_manager = LoginManager()
login_manager.init_app(server)
server.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

@login_manager.user_loader
def user_loader(user_id):
    return get_user(user_id)

# 항상 모든 인증 관련 컴포넌트가 레이아웃에 존재하도록 포함
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    sidebar,
    html.Div(id="page-content", style={"margin-left": "18rem", "margin-right": "2rem", "padding": "2rem 1rem"})
])

# ─── 페이지 렌더링 ─────────────────────────────────────
def render_page(pathname):
    if pathname == "/":
        # 첫화면: 히어로 섹션 + 로그인 버튼
        return html.Div([
            html.Div([
                html.I(className="fas fa-leaf hero-icon"),
                html.H1("지속가능한 미래를 위한", className="hero-title"),
                html.H2("LCA 환경영향 분석 시스템", className="hero-subtitle"),
                html.P("제품의 전 생애주기에서 발생하는 환경영향을 과학적으로 측정하고 분석하여, 친환경적이고 지속가능한 의사결정을 지원하는 전문 도구입니다.", className="hero-description"),
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-line hero-feature-icon"),
                        html.H3("정확한 분석", className="hero-feature-title"),
                        html.P("과학적 방법론을 통한 정밀한 환경영향 평가", className="hero-feature-desc")
                    ], className="hero-feature"),
                    html.Div([
                        html.I(className="fas fa-database hero-feature-icon"),
                        html.H3("방대한 DB", className="hero-feature-title"),
                        html.P("국내외 다양한 환경영향 DB 내장", className="hero-feature-desc")
                    ], className="hero-feature"),
                    html.Div([
                        html.I(className="fas fa-bolt hero-feature-icon"),
                        html.H3("빠른 결과", className="hero-feature-title"),
                        html.P("즉각적인 분석 및 시각화 제공", className="hero-feature-desc")
                    ], className="hero-feature"),
                ], className="hero-features"),
            ], className="hero-content"),
            html.Button("로그인", id="login-button", className="login-btn", n_clicks=0, style={"position": "fixed", "top": "2rem", "right": "2rem", "zIndex": 1000}),
        ], style={"display": "flex", "alignItems": "center", "justifyContent": "center", "minHeight": "100vh"})
    elif pathname == "/inputs":
        return html.Div([
            sidebar,
            html.Div([
                html.H2("투입물 입력 페이지"),
                dbc.Row([
                    dbc.Col([
                        dbc.Input(id="material-name", placeholder="물질명", type="text", style={"marginBottom": "0.5rem"}),
                        dbc.Input(id="material-amount", placeholder="투입량", type="number", style={"marginBottom": "0.5rem"}),
                        dbc.Input(id="material-unit", placeholder="단위", type="text", style={"marginBottom": "0.5rem"}),
                        dbc.Input(id="material-category", placeholder="분류", type="text", style={"marginBottom": "0.5rem"}),
                        dbc.Input(id="material-db", placeholder="DB명", type="text", style={"marginBottom": "0.5rem"}),
                        dbc.Input(id="material-country", placeholder="국가", type="text", style={"marginBottom": "0.5rem"}),
                        dbc.Input(id="material-dbunit", placeholder="DB단위", type="text", style={"marginBottom": "0.5rem"}),
                        dbc.Button("추가", id="add-row", color="primary", n_clicks=0, style={"marginRight": "0.5rem"}),
                        dbc.Button("삭제", id="delete-row", color="danger", n_clicks=0),
                        dbc.Button("저장", id="save-data", color="success", n_clicks=0, style={"marginLeft": "0.5rem"}),
                        html.Div(id="analysis-result", style={"marginTop": "1rem"})
                    ], width=4),
                    dbc.Col([
                        dash_table.DataTable(
                            id="material-table",
                            columns=[
                                {"name": "물질명", "id": "name"},
                                {"name": "투입량", "id": "amount"},
                                {"name": "단위", "id": "unit"},
                                {"name": "분류", "id": "category"},
                                {"name": "DB명", "id": "db"},
                                {"name": "국가", "id": "country"},
                                {"name": "DB단위", "id": "dbunit"},
                            ],
                            data=[],
                            row_selectable="multi",
                            selected_rows=[],
                            style_table={"overflowX": "auto"},
                            style_cell={"textAlign": "center"},
                        )
                    ], width=8)
                ])
            ], style={"marginLeft": "18rem", "padding": "2rem 1rem"})
        ])
    elif pathname == "/db":
        return html.Div([
            sidebar,
            html.Div([
                html.H2("DB 관리 페이지"),
                dbc.Button("행 추가", id="add-db-row", color="primary", n_clicks=0, style={"marginRight": "0.5rem"}),
                dbc.Button("선택 삭제", id="delete-selected-rows", color="danger", n_clicks=0),
                dash_table.DataTable(
                    id="db-edit-table",
                    columns=[
                        {"name": "물질명", "id": "물질명"},
                        {"name": "분류", "id": "분류"},
                        {"name": "DB명", "id": "DB명"},
                        {"name": "국가", "id": "국가"},
                        {"name": "단위", "id": "단위"},
                    ],
                    data=[],
                    row_selectable="multi",
                    selected_rows=[],
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "center"},
                )
            ], style={"marginLeft": "18rem", "padding": "2rem 1rem"})
        ])
    elif pathname == "/lca":
        return html.Div([
            sidebar,
            html.Div([
                html.H2("LCA 분석결과 페이지"),
                dash_table.DataTable(
                    id="lca-result-table",
                    columns=[
                        {"name": "No.", "id": "no"},
                        {"name": "Impact category", "id": "impact"},
                        {"name": "Unit", "id": "unit"},
                        {"name": "TOTAL", "id": "total"},
                        {"name": "원료물질", "id": "raw_material"},
                        {"name": "보조물질", "id": "additive"},
                        {"name": "에너지", "id": "energy"},
                        {"name": "유틸리티", "id": "utility"},
                        {"name": "수송", "id": "transport"},
                        {"name": "폐기물처리", "id": "waste"},
                    ],
                    data=[],
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "center"},
                ),
                html.Div([
                    html.H4("환경영향 분포 파이차트"),
                    dcc.Graph(id="impact-pie-chart"),
                    html.H4("분류별 환경영향 막대그래프"),
                    dcc.Graph(id="impact-bar-chart"),
                    html.H4("영향범주별 상세 분석 스택바"),
                    dcc.Graph(id="impact-detailed-chart"),
                ], style={"marginTop": "2rem"})
            ], style={"marginLeft": "18rem", "padding": "2rem 1rem"})
        ])
    else:
        return html.Div([
            html.H2("페이지를 찾을 수 없습니다."),
            html.A("메인으로", href="/")
        ], style={"textAlign": "center", "marginTop": "5rem"})

# ─── 페이지 전환 콜백 ────────────────────────────────
@app.callback(
    [Output("sidebar-container", "style"),
     Output("page-content", "style"),
     Output("hero-section", "style"),
     Output("auth-forms-container", "style"),
     Output("login-button", "style"),
     Output("show-login-btn", "style"),
     Output("show-signup-btn", "style"),
     Output("login-form", "style"),
     Output("signup-form", "style"),
     Output("auth-message", "style")],
    [Input("url", "pathname")]
)
def update_page_visibility(pathname):
    styles = render_page(pathname)
    # auth-forms-container 표시 제어
    if pathname == "/login":
        auth_forms_style = {
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "justifyContent": "center",
            "minHeight": "100vh",
            "background": "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
        }
    else:
        auth_forms_style = {"display": "none"}
    return (
        styles["sidebar-container"],
        styles["page-content"],
        styles["hero-section"],
        auth_forms_style,
        styles["login-button"],
        styles["show-login-btn"],
        styles["show-signup-btn"],
        styles["login-form"],
        styles["signup-form"],
        styles["auth-message"]
    )

# ─── 인증/탭/로그인/회원가입 콜백 (중복 없이 함수 내부에 완전히 포함) ──────────
@app.callback(
    [
        Output("login-form", "className"),
        Output("signup-form", "className"),
        Output("show-login-btn", "className"),
        Output("show-signup-btn", "className"),
        Output("auth-message", "children"),
        Output("auth-message", "className"),
        Output("url", "pathname", allow_duplicate=True)
    ],
    [
        Input("login-button", "n_clicks"),
        Input("show-login-btn", "n_clicks"),
        Input("show-signup-btn", "n_clicks"),
        Input("login-submit-btn", "n_clicks"),
        Input("signup-submit-btn", "n_clicks")
    ],
    [
        State("login-username", "value"),
        State("login-password", "value"),
        State("signup-username", "value"),
        State("signup-password", "value"),
        State("signup-password-confirm", "value")
    ],
    prevent_initial_call='initial_duplicate'
)
def handle_auth_actions(login_btn_clicks, login_switch_clicks, signup_switch_clicks, login_submit_clicks, signup_submit_clicks,
                       login_username, login_password,
                       signup_username, signup_password, signup_password_confirm):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    # 상단 로그인 버튼 클릭 시 로그인 페이지로 이동 (n_clicks가 0이면 아무 동작 안 함)
    if button_id == "login-button" and login_btn_clicks:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, "", "", "/login"

    # 탭 전환 처리
    if button_id == "show-login-btn":
        return "auth-form active", "auth-form", "auth-tab-btn active", "auth-tab-btn", "", "", dash.no_update
    elif button_id == "show-signup-btn":
        return "auth-form", "auth-form active", "auth-tab-btn", "auth-tab-btn active", "", "", dash.no_update

    # 로그인 처리
    elif button_id == "login-submit-btn":
        if not login_username or not login_password:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, "아이디와 비밀번호를 모두 입력해주세요.", "auth-message error", dash.no_update
        try:
            response = requests.post('/login', json={'username': login_username, 'password': login_password})
            data = response.json()
            print(data)  # 서버 응답 콘솔 출력
            if data['success']:
                # 인증 상태 안내 메시지
                from flask_login import current_user
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, f"로그인 성공! 인증 상태: {getattr(current_user, 'is_authenticated', False)}", "auth-message success", "/"
            else:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, data['message'], "auth-message error", dash.no_update
        except Exception as e:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, "로그인 중 오류가 발생했습니다.", "auth-message error", dash.no_update

    # 회원가입 처리
    elif button_id == "signup-submit-btn":
        if not signup_username or not signup_password or not signup_password_confirm:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, "모든 필드를 입력해주세요.", "auth-message error", dash.no_update
        if signup_password != signup_password_confirm:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, "비밀번호가 일치하지 않습니다.", "auth-message error", dash.no_update
        if len(signup_password) < 6:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, "비밀번호는 최소 6자 이상이어야 합니다.", "auth-message error", dash.no_update
        try:
            response = requests.post('/signup', json={'username': signup_username, 'password': signup_password})
            data = response.json()
            print(data)
            if data['success']:
                from flask_login import current_user
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, f"회원가입 성공! 인증 상태: {getattr(current_user, 'is_authenticated', False)}", "auth-message success", "/"
            else:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, data['message'], "auth-message error", dash.no_update
        except Exception as e:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, "회원가입 중 오류가 발생했습니다.", "auth-message error", dash.no_update

    # 기본 반환 (초기 상태)
    return "auth-form active", "auth-form", "auth-tab-btn active", "auth-tab-btn", "", "", dash.no_update

# 전역 변수로 인증 상태 추적
authenticated_users = set()

# ─── 통계 카드 업데이트 콜백 ─────────────────────────────
@app.callback(
    [Output("total-impact", "children"),
     Output("analysis-items", "children"),
     Output("last-analysis", "children"),
     Output("analysis-status", "children")],
    [Input("run-lca-analysis", "n_clicks")],
    [State("table-store", "data")],
    prevent_initial_call=True
)
def update_statistics_cards(n_clicks, table_data):
    if not n_clicks or not table_data:
        return "0", "0", "미실행", "대기 중"
    
    # 총 환경영향 계산 (간단한 예시)
    total_impact = len(table_data) * 100  # 실제로는 LCA 계산 결과를 사용
    
    # 분석 항목 수
    analysis_items = len(table_data)
    
    # 최근 분석 시간
    last_analysis = datetime.now().strftime("%H:%M")
    
    # 상태
    status = "완료"
    
    return str(total_impact), str(analysis_items), last_analysis, status

# ─── 그래프 업데이트 콜백 ─────────────────────────────
@app.callback(
    [Output("impact-pie-chart", "figure"),
     Output("impact-bar-chart", "figure"),
     Output("impact-detailed-chart", "figure")],
    [Input("run-lca-analysis", "n_clicks")],
    [State("table-store", "data")],
    prevent_initial_call=True
)
def update_charts(n_clicks, table_data):
    if not n_clicks or not table_data:
        # 빈 그래프 반환
        empty_fig = {
            "data": [],
            "layout": {
                "title": "데이터가 없습니다",
                "xaxis": {"title": ""},
                "yaxis": {"title": ""},
                "font": {"color": "#718096"},
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)"
            }
        }
        return empty_fig, empty_fig, empty_fig
    
    # 샘플 데이터 생성 (실제로는 LCA 계산 결과 사용)
    categories = ["원료물질", "보조물질", "에너지", "유틸리티", "수송", "폐기물처리"]
    impact_values = [25, 15, 30, 10, 12, 8]  # 퍼센트
    
    # 파이 차트
    pie_fig = {
        "data": [{
            "type": "pie",
            "labels": categories,
            "values": impact_values,
            "hole": 0.4,
            "marker": {
                "colors": ["#6b7c93", "#a8b2d1", "#8b9dc3", "#7f9c9f", "#d4a574", "#c17f59"]
            },
            "textinfo": "label+percent",
            "textposition": "outside"
        }],
        "layout": {
            "title": {
                "text": "환경영향 분포",
                "font": {"color": "#2d3748", "size": 18}
            },
            "font": {"color": "#718096"},
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "showlegend": True,
            "legend": {"x": 0.02, "y": 0.98}
        }
    }
    
    # 막대 그래프
    bar_fig = {
        "data": [{
            "type": "bar",
            "x": categories,
            "y": impact_values,
            "marker": {
                "color": ["#6b7c93", "#a8b2d1", "#8b9dc3", "#7f9c9f", "#d4a574", "#c17f59"],
                "line": {"color": "#e2e8f0", "width": 1}
            },
            "text": [f"{v}%" for v in impact_values],
            "textposition": "auto"
        }],
        "layout": {
            "title": {
                "text": "분류별 환경영향",
                "font": {"color": "#2d3748", "size": 18}
            },
            "xaxis": {
                "title": "분류",
                "tickangle": -45,
                "color": "#718096"
            },
            "yaxis": {
                "title": "영향 비율 (%)",
                "color": "#718096"
            },
            "font": {"color": "#718096"},
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "bargap": 0.3
        }
    }
    
    # 상세 분석 그래프 (스택 바 차트)
    impact_categories = ["기후변화", "산성화", "부영양화", "오존층파괴", "인체독성"]
    detailed_data = []
    
    for i, category in enumerate(categories):
        detailed_data.append({
            "type": "bar",
            "name": category,
            "x": impact_categories,
            "y": [impact_values[i] * 0.2, impact_values[i] * 0.15, impact_values[i] * 0.25, 
                  impact_values[i] * 0.1, impact_values[i] * 0.3],
            "marker": {"color": ["#6b7c93", "#a8b2d1", "#8b9dc3", "#7f9c9f", "#d4a574", "#c17f59"][i]}
        })
    
    detailed_fig = {
        "data": detailed_data,
        "layout": {
            "title": {
                "text": "영향범주별 상세 분석",
                "font": {"color": "#2d3748", "size": 18}
            },
            "xaxis": {
                "title": "영향범주",
                "color": "#718096"
            },
            "yaxis": {
                "title": "영향 지수",
                "color": "#718096"
            },
            "font": {"color": "#718096"},
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "barmode": "stack",
            "bargap": 0.2,
            "showlegend": True,
            "legend": {"x": 0.02, "y": 0.98}
        }
    }
    
    return pie_fig, bar_fig, detailed_fig

@app.callback(
    Output("auth-button-container", "children"),
    [Input("url", "pathname")]
)
def update_auth_button(pathname):
    # URL 변경 시 인증 상태 확인
    if current_user.is_authenticated:
        return dbc.Button([
            html.I(className="fas fa-sign-out-alt me-2"),
            "로그아웃"
        ], id="logout-button", className="logout-btn")
    else:
        return dbc.Button([
            html.I(className="fas fa-sign-in-alt me-2"),
            "로그인"
        ], id="login-button", className="login-btn")


# ─── Flask 라우트 추가 ──────────────────────────────────
@app.server.route('/login', methods=['POST'])
def login_api():
    from flask import request, redirect
    try:
        # 1. JSON 요청 처리
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        # 2. Form 요청 처리
        else:
            username = request.form.get('username')
            password = request.form.get('password')

        if not username or not password:
            return "아이디와 비밀번호를 모두 입력해주세요.", 400

        users = load_users()
        if username in users and check_password_hash(users[username]['password_hash'], password):
            user = User(username, users[username]['password_hash'])
            login_user(user)
            # 로그인 성공 시 LCA 분석 대시보드로 리디렉션
            return redirect('/lca')
        else:
            return "아이디 또는 비밀번호가 올바르지 않습니다.", 401

    except Exception as e:
        return f"로그인 중 오류가 발생했습니다: {str(e)}", 500

@app.server.route('/signup', methods=['POST'])
def signup_api():
    from flask import request, redirect
    try:
        # 1. JSON 요청 처리
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        # 2. Form 요청 처리
        else:
            username = request.form.get('username')
            password = request.form.get('password')

        if not username or not password:
            return "모든 필드를 입력해주세요.", 400
        if len(password) < 6:
            return "비밀번호는 최소 6자 이상이어야 합니다.", 400

        users = load_users()
        if username in users:
            return "이미 존재하는 아이디입니다.", 400

        # 새 사용자 생성
        password_hash = generate_password_hash(password)
        users[username] = {
            "password_hash": password_hash,
            "created_at": str(pd.Timestamp.now())
        }
        save_users(users)
        user = User(username, password_hash)
        login_user(user)
        # 회원가입 성공 시 LCA 분석 대시보드로 리디렉션
        return redirect('/lca')
    except Exception as e:
        return f"회원가입 중 오류가 발생했습니다: {str(e)}", 500

# 앱 시작 시 사용자 데이터 파일 초기화
init_users_file()

# ─── Flask 라우트: 인증 페이지 ─────────────────────
@app.server.route('/auth', methods=['GET'])
def auth_page():
    try:
        return render_template('auth_page.html')
    except Exception:
        return '<h2>로그인/회원가입 페이지가 준비 중입니다.</h2>'

# ─── Dash 페이지 전환 콜백: 인증 분기 ──────────────
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page_content(pathname):
    protected_paths = ['/', '/inputs', '/db', '/lca']
    if pathname in protected_paths and not current_user.is_authenticated:
        return dcc.Location(href="/auth", id="force-auth-redirect")
    return render_page(pathname)

# 로그인 버튼 클릭 시 /auth로 이동하는 콜백은 유지
@app.callback(
    Output("url", "pathname"),
    Input("login-button", "n_clicks"),
    prevent_initial_call=True
)
def go_to_auth(n_clicks):
    if n_clicks:
        return "/auth"
    return dash.no_update

if __name__ == "__main__":
    print("Dash is running on http://0.0.0.0:8050/")
    app.run(host='0.0.0.0', port=8050, debug=False)