import requests

def få_hubspot_kunder(kundidn=None,
                      antal_kunder=10,
                      hubspot_api_key="pat-na1-003cd583-9877-4c70-97ba-4c8cb7b980e0"):
    headers = {"Authorization": "Bearer " + hubspot_api_key}
    params = {"limit": antal_kunder}
    # För specifika kunder
    if kundidn != None:
        kundlista = []
        for kundid in kundidn:
            svar = requests.get(f"https://api.hubapi.com/crm/v3/objects/contacts/{kundid}", headers=headers)
            # Request lyckades
            if svar.status_code == 200:
                kund = svar.json()
                kundlista.append(kund)
            # Request misslyckades   
            else:
                print(f"Request misslyckades: {svar.status_code}")
        return kundlista
    # Om inga specifika kunder blev efterfrågade
    else:
        svar = requests.get("https://api.hubapi.com/crm/v3/objects/contacts", headers=headers, params=params)
        # Request lyckades
        if svar.status_code == 200:
            kundlista = svar.json()["results"]
            return kundlista
        # Request misslyckades 
        else:
            print(f"Request misslyckades: {svar.status_code}")
            return []


def få_status_newsletters(api_nyckeln="70b63d7973cf57ed48c2fd9c2393b228d1db",
                          base_url = "http://localhost:3001"):
    '''
    Function för att få status från Newsletters.

    Output: Status från Newsletters om status-request fungerade,
    felmeddelande om det inte fungerar.
    
    '''
    status_url = f"{base_url}/status"
    headers = {"x-api-key": api_nyckeln}
    svar = requests.get(status_url, headers=headers)

    if svar.status_code == 200:
        # Request lyckades
        data = svar.json()
        return data
    else:
        # Request misslyckades
        print(f"Request misslyckades: {svar.status_code}")
        return []


def få_newsletters_kunder(api_nyckeln="70b63d7973cf57ed48c2fd9c2393b228d1db",
                          base_url="http://localhost:3001", 
                          limit=10,
                          after=None,
                          kundidn=None, 
                          förnamn=None,
                          efternamn=None
                          ):
    """
    Hämtar kunder från newsletters.

    Parametrar:
    api_nyckeln (str, default: 70b63d7973cf57ed48c2fd9c2393b228d1db): API-nyckeln.
    base_url (str, default: http://localhost:3001): Bas-URL för newsletters.
    limit (int, default: 10): Det maximala antalet kunder att hämta.
    efter (int, valfritt): ID för den senaste kunden som returnerades i föregående begäran, används för sidnumrering.
    kundidn (list, valfritt): Lista med ID:n för specifika kunder att hämta.
    förnamn (list, valfritt): Lista med förnamn på kunder att filtrera efter.
    efternamn (list, valfritt): Lista med efternamn på kunder att filtrera efter.

    Returnerar:
    En lista över newsletterskunder.

    """
    url = f"{base_url}/newsletters"
    params = {"limit": limit, "after": after}
    headers = {"x-api-key": api_nyckeln}
    if kundidn:
        params["id"] = ",".join(kundidn)
    if förnamn:
        params["firstName"] = ",".join(förnamn)
    if efternamn:
        params["lastName"] = ",".join(efternamn)
    svar = requests.get(url, params=params, headers=headers)
    if svar.status_code == 200:
        # Request lyckades
        data = svar.json()
        kundlista = data.get("newsletterSubscribers", [])
        return kundlista
    else:
        # Request misslyckades
        print(f"Request failed with status code {svar.status_code}")
        return []


def få_preferrence(api_nyckeln="eecd57cc228732f3f92bb9719476e3d308db",
                              base_url="http://localhost:3002",
                              kundnummer=None,
                              limit=10):
    """
    Hämtar kommunikationsvägar för kunder från preferrence API:t.

    Parametrar:
    api_nyckeln (str, default: eecd57cc228732f3f92bb9719476e3d308db): API-nyckeln.
    base_url (str, default: http://localhost:3002): Bas-URL för Kunders kommunikationsväg.
    kundnummer (list, valfritt): En lista av kundnumbers av kunder för att hänta kommunikationsvägar ifrån.
    limit (int, valfritt): Det maximala antalet kunder att hämta kommunikationsvägar för, om inga kundnummer anges.

    Returnerar:
    En dict över kundnummer mappade till deras kommunikationsvägar.
    
    """
    url = f"{base_url}/customers/"
    params = {"limit": limit}
    if kundnummer:
        params["customerNumbers"] = ",".join(kundnummer)
    headers = {"x-api-key": api_nyckeln}
    svar = requests.get(url, params=params, headers=headers)

    if svar.status_code == 200:
        # Request lyckades
        data = svar.json()
        kommunikationsvägar = {}
        for kund in data:
            kommunikationsvägar[kund["customerNumber"]] = kund["CommunicationMethod"]
        return kommunikationsvägar
    else:
        # Request misslyckades
        print(f"Request failed with status code {svar.status_code}")
        return {}

if __name__ == "__main__":
    # Se resultat här nere
    print(få_status_newsletters())
    print(få_newsletters_kunder(limit=10))
    #print(få_preferrence(kundnummer=[1])) # Fortfarande konstig för mig, ska fixa
    print(få_hubspot_kunder(kundidn=[51, 1]))
    print(få_hubspot_kunder(num_customers=10))