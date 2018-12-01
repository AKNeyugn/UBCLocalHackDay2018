'''
    Parse translink alerts website and output json file with station access alerts.
'''

from bs4 import BeautifulSoup
import requests
import json

url = "https://alerts.translink.ca/"
list_alerts = []

def main(): 
    # Get request
    resp = requests.get(url)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")
        alerts_cats = soup.find_all("details", class_="category")
        for cat in alerts_cats:
            # Get Station Access alerts bloc
            if "hasAlerts" in cat["class"] and "StationAccess" in cat["class"]:
                alert_details = cat.find_all("details")
                # Get alert bloc
                for detail in alert_details:
                    station_name = detail.find("span", class_="RouteLongName").text
                    section = detail.find("section")

                    # Parse Effects
                    temp_alert_effects = section.find_all("span", class_="AlertEffect")
                    alert_effects = []
                    for temp_effect in temp_alert_effects:
                        effect = temp_effect.text
                        alert_effects.append(effect)
                 
                    # Parse Effective Period
                    temp_alert_periods = section.find_all("span", class_="effectivePeriod")
                    alert_periods = []
                    for temp_period in temp_alert_periods:
                        period = temp_period.text
                        alert_periods.append(period)

                    # Parse Info & Description
                    temp_alert_infos = section.find_all("p", class_="info")
                    alert_infos = []
                    for temp_info in temp_alert_infos:
                        temp_alert_desc = temp_info.find_next_sibling("p", class_="description")
                        info = temp_info.text
                        if temp_alert_desc != None:
                            info += temp_alert_desc.text
                        alert_infos.append(info)

                    # Parse Last Updated
                    temp_alert_last_upds = section.find_all("span", class_="AlertLastModifiedDate")
                    alert_last_upds = []
                    for temp_upd in temp_alert_last_upds:
                        upd = temp_upd.text
                        alert_last_upds.append(upd)

                    # Add alert to list
                    num_alerts = len(alert_effects)
                    for i in range(num_alerts):
                        new_alert = {
                            "Station": station_name,
                            "Effect": alert_effects[i],
                            "Effective Period": alert_periods[i],
                            "Info": alert_infos[i],
                            "Last Updated": alert_last_upds[i]
                        }
                        list_alerts.append(new_alert)
    else:
        print("Page not found")
    
    # Create JSON file
    with open("StationAccessAlerts.json", "w") as f:
        json.dump(list_alerts, f)



if __name__ == '__main__':
    main()
