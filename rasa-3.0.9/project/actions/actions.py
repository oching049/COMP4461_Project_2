# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from turtle import update
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import urllib.parse
import http.client
import json

import datetime

clinics = [
    {
        "name": "1/F, Shau Kei Wan Jockey Club General Out-patient Clinic",
        "address": "1/F, 8 Chai Wan Road, Shau Kei Wan",
        "area": "Hong Kong",
        "tel": 25600211,
        "careLine": 25601599,
        "latitude": 22.27648965449197,
        "longitude": 114.22847540253501,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Wan Tsui General Out-patient Clinic",
        "address": "G/F, Block 12, Wan Tsui Estate, Chai Wan",
        "area": "Hong Kong",
        "tel": 28975527,
        "careLine": 28971058,
        "latitude": 22.263120748233476,
        "longitude": 114.23933339679101,
        "distance": {},
        "duration": {},
    },
    {
        "name": "G/F, Violet Peel General Out-patient Clinic",
        "address": "G/F, Tang Shiu Kin Hospital, Community Ambulatory Care Centre, 282 Queen's Road East, Wanchai",
        "area": "Hong Kong",
        "tel": 35533116,
        "careLine": 23871776,
        "latitude": 22.275328913447083,
        "longitude": 114.17775699741416,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Kennedy Town Jockey Club General Out-patient Clinic",
        "address": "45 Victoria Road, Kennedy Town",
        "area": "Hong Kong",
        "tel": 28173215,
        "careLine": 70837500,
        "latitude": 22.281869430059388,
        "longitude": 114.12397929361025,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Aberdeen Jockey Club General Out-patient Clinic",
        "address": "10 Aberdeen Reservoir Road, Aberdeen",
        "area": "Hong Kong",
        "tel": 25550381,
        "careLine": 70836500,
        "latitude": 22.24975652151861,
        "longitude": 114.15638976120827,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Robert Black General Out-patient Clinic",
        "address": "600 Prince Edward Road East, San Po Kong",
        "area": "Kowloon",
        "tel": 23772660,
        "careLine": 35064277,
        "latitude": 22.332467954700263,
        "longitude": 114.19566312317806,
        "distance": {},
        "duration": {},
    },
    {
        "name": "East Kowloon General Out-patient Clinic",
        "address": "160 Hammer Hill Road, Diamond Hill, Kowloon",
        "area": "Kowloon",
        "tel": 23277260,
        "careLine": 35062989,
        "latitude": 22.3396002279426,
        "longitude": 114.20779189741147,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Wang Tau Hom Jockey Club General Out-patient Clinic",
        "address": "200 Junction Road, Wang Tau Hom",
        "area": "Kowloon",
        "tel": 52784988,
        "careLine": 52784279,
        "latitude": 22.339072672465548,
        "longitude": 114.18535592685244,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Yau Ma Tei Jockey Club General Out-patient Clinic",
        "address": "1/F, 145 Battery Street, Yau Ma Tei",
        "area": "Kowloon",
        "tel": 24407659,
        "careLine": 35064989,
        "latitude": 22.309525452763694,
        "longitude": 114.16928844000961,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Kowloon Bay Health Centre General Out-patient Clinic",
        "address": "1/F, 9 Kai Yan Street, Kowloon Bay",
        "area": "Kowloon",
        "tel": 21162812,
        "careLine": 52152312,
        "latitude": 22.32863672853433,
        "longitude": 114.20689793911059,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Lam Tin Polyclinic General Out-patient Clinic",
        "address": "99 Kai Tin Road, Lam Tin",
        "area": "Kowloon",
        "tel": 24887408,
        "careLine": 23701279,
        "latitude": 22.310518944543762,
        "longitude": 114.23334706428211,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Cheung Sha Wan Jockey Club General Out-patient Clinic",
        "address": "2 Kwong Lee Road, Cheung Sha Wan",
        "area": "Kowloon",
        "tel": 24974416,
        "careLine": 23878211,
        "latitude": 22.34067202091219,
        "longitude": 114.15858228820822,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Shek Kip Mei General Out-patient Clinic",
        "address": "2 Berwick Street, Shek Kip Mei",
        "area": "Kowloon",
        "tel": 24647315,
        "careLine": 27883023,
        "latitude": 22.330795581164676,
        "longitude": 114.16720348755547,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Tseung Kwan O (Po Ning Road) General Out-patient Clinic",
        "address": "G/F, 28 Po Ning Road, Tseung Kwan O",
        "area": "New Territories",
        "tel": 21911083,
        "careLine": 95282106,
        "latitude": 22.31778434621669,
        "longitude": 114.26794570231405,
        "distance": {},
        "duration": {},
    },
    {
        "name": "South Kwai Chung Jockey Club General Out-patient Clinic",
        "address": "310 Kwai Shing Circuit, Kwai Chung",
        "area": "New Territories",
        "tel": 24974413,
        "careLine": 26157333,
        "latitude": 22.360854714524216,
        "longitude": 114.12532212685285,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Mrs Wu York Yu General Out-patient Clinic",
        "address": "310 Wo Yi Hop Road, Lei Muk Shue, Kwai Chung",
        "area": "New Territories",
        "tel": 24974420,
        "careLine": 24010124,
        "latitude": 22.376057611544752,
        "longitude": 114.1367170891989,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Tsing Yi Town General Out-patient Clinic",
        "address": "21 Tsing Luk Street, Tsing Yi",
        "area": "New Territories",
        "tel": 22548155,
        "careLine": 24346205,
        "latitude": 22.35441236586844,
        "longitude": 114.10592568022616,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Yuen Chau Kok General Out-patient Clinic",
        "address": "G/F, 29 Chap Wai Kon Street, Shatin",
        "area": "New Territories",
        "tel": 26473383,
        "careLine": 91472400,
        "latitude": 22.382326725110115,
        "longitude": 114.20163229434353,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Tai Po Jockey Club General Out-patient Clinic",
        "address": "G/F, 37 Ting Kok Road, Tai Po",
        "area": "New Territories",
        "tel": 26642039,
        "careLine": 66252483,
        "latitude": 22.453986048594217,
        "longitude": 114.16582318822114,
        "distance": {},
        "duration": {},
    },
    {
        "name": "1/F, Fanling Family Medicine Centre",
        "address": "1/F, Fanling Health Centre, 2 Pik Fung Road, Fanling",
        "area": "New Territories",
        "tel": 26394601,
        "careLine": 60164814,
        "latitude": 22.49615829995044,
        "longitude": 114.13883851397394,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Yan Oi General Out-patient Clinic",
        "address": "G/F, 6 Tuen Lee Street, Tuen Mun",
        "area": "New Territories",
        "tel": 29885516,
        "careLine": 70724784,
        "latitude": 22.391208065106806,
        "longitude": 113.97919525814908,
        "distance": {},
        "duration": {},
    },
    {
        "name": "1/F, Tin Shui Wai (Tin Yip Road) Community Health Centre",
        "address": "1/F, 3 Tin Yip Road, Tin Shui Wai (Opposite HK Wetland Park and Vianni Cove of Tin Kwai Road)",
        "area": "New Territories",
        "tel": 31242200,
        "careLine": 70724795,
        "latitude": 22.465441385172607,
        "longitude": 114.00578077225663,
        "distance": {},
        "duration": {},
    },
    {
        "name": "Madam Yung Fung Shee Health Centre",
        "address": "26 Sai Ching Street, Yuen Long",
        "area": "New Territories",
        "tel": 25291308,
        "careLine": 64680113,
        "latitude": 22.44090336541119,
        "longitude": 114.02699446184727,
        "distance": {},
        "duration": {},
    }

]

key = "AIzaSyB9BuzmAq-fomht165r93txlOw_6DVygrA"


class ActionAskSituation(Action):

    def name(self) -> Text:
        return "action_ask_situation"

    def getInfo(self):
        conn = http.client.HTTPSConnection("disease.sh")
        payload = ''
        headers = {}
        conn.request("GET", "/v3/covid-19/countries/HK", payload, headers)
        res = conn.getresponse()
        data = res.read()
        r = json.loads(data.decode("utf-8"))
        return r

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = self.getInfo()
        updated = result["updated"]
        updated_date = datetime.datetime.fromtimestamp(
            int(str(updated)[:10]))
        cases = result["cases"]
        todayCases = result["todayCases"]
        deaths = result['deaths']
        todayDeaths = result['todayDeaths']
        dispatcher.utter_message(
            text=f"Here is the latest covid situation in Hong Kong as of {updated_date}:\nCumulative number of confirmed cases: {cases}\nNewly confirmed cases: {todayCases}\nTotal deaths from the confirmed cases: {deaths}\nNew deaths from the confirmed cases: {todayDeaths}")

        return []


class ActionFindClinic(Action):
    def name(self) -> Text:
        return "action_find_clinic"

    def getInfo(self, address):
        filtered_clinic = []
        conn = http.client.HTTPSConnection("maps.googleapis.com")
        payload = ''
        headers = {}
        origin = urllib.parse.quote_plus(address, safe='')

        for clinic in clinics:
            destination = urllib.parse.quote_plus(clinic["name"], safe='')
            conn.request(
                "GET", f"/maps/api/directions/json?key={key}&destination={destination}&origin={origin}&language=en&region=hk&mode=walking", payload, headers)
            res = conn.getresponse()
            data = res.read()
            r = json.loads(data.decode("utf-8"))
            #print(json.dumps(r, indent=4, sort_keys=True))

            if(r["routes"] != []):
                clinic["distance"] = r["routes"][0]["legs"][0]["distance"]
                clinic["duration"] = r["routes"][0]["legs"][0]["duration"]
                if(filtered_clinic == []):
                    filtered_clinic = clinic
                else:
                    if(filtered_clinic["distance"]["value"] > clinic["distance"]["value"]):
                        filtered_clinic = clinic
            else:
                break

        return filtered_clinic

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        address_string = tracker.latest_message.get('text')
        filtered_clinic = self.getInfo(address_string)

        if(filtered_clinic != []):
            duration = filtered_clinic["duration"]["text"]
            dispatcher.utter_message(
                text=f"We have found a designated near {address_string}, which is just about {duration} of walking.")

            dispatcher.utter_message(text="Your nearest clinic is:")

            name = filtered_clinic["name"]
            address = filtered_clinic["address"]
            tel = filtered_clinic["tel"]
            careLine = filtered_clinic["careLine"]
            dispatcher.utter_message(
                text=f"Clinic name: {name}\nAddress: {address}\nBook appointment tel number: {tel}\nCare booking line: {careLine}")
        else:
            dispatcher.utter_message(
                text="Sorry. We could not find any designated clinic near you. Please try again next time")

        return [SlotSet(key="address_string", value=None)]
