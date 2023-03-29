import requests
import zeep

def få_hubspot_companies(companyidn=None,
                      antal_companies=10,
                      hubspot_api_key="pat-na1-003cd583-9877-4c70-97ba-4c8cb7b980e0"):
    '''
    Function för att få företag från Hubspot companies API:t.

    Parametrar:
    hubspot_api_key (str, default: pat-na1-003cd583-9877-4c70-97ba-4c8cb7b980e0): API-nyckeln.
    antal_companies (int, default: 10): Antalet företag att hämta.
    kundidn (list, default: None): Lista av company-ID:n att hämta.

    Output: Lista med Hubspot-företag.
    
    '''
    headers = {"Authorization": "Bearer " + hubspot_api_key}
    params = {"limit": antal_companies}
    # För specifika deals
    if companyidn != None:
        companylista = []
        for companyid in companyidn:
            svar = requests.get(f"https://api.hubapi.com/crm/v3/objects/companies/{companyid}", headers=headers)
            # Request lyckades
            if svar.status_code == 200:
                deal = svar.json()
                companylista.append(deal)
            # Request misslyckades   
            else:
                print(f"Request misslyckades: {svar.status_code}")
        return companylista
    # Om inga specifika företag blev efterfrågade
    else:
        svar = requests.get("https://api.hubapi.com/crm/v3/objects/companies", headers=headers, params=params)
        # Request lyckades
        if svar.status_code == 200:
            companylista = svar.json()["results"]
            return companylista
        # Request misslyckades 
        else:
            print(f"Request misslyckades: {svar.status_code}")
            return []

def få_hubspot_deals(dealidn=None,
                      antal_deals=10,
                      hubspot_api_key="pat-na1-003cd583-9877-4c70-97ba-4c8cb7b980e0"):
    '''
    Function för att få deals från Hubspot deals API:t.

    Parametrar:
    hubspot_api_key (str, default: pat-na1-003cd583-9877-4c70-97ba-4c8cb7b980e0): API-nyckeln.
    antal_deals (int, default: 10): Antalet deals att hämta.
    kundidn (list, default: None): Lista av deal-ID:n att hämta.

    Output: Lista med Hubspot-deals.
    
    '''
    headers = {"Authorization": "Bearer " + hubspot_api_key}
    params = {"limit": antal_deals}
    # För specifika deals
    if dealidn != None:
        deallista = []
        for dealid in dealidn:
            svar = requests.get(f"https://api.hubapi.com/crm/v3/objects/deals/{dealid}", headers=headers)
            # Request lyckades
            if svar.status_code == 200:
                deal = svar.json()
                deallista.append(deal)
            # Request misslyckades   
            else:
                print(f"Request misslyckades: {svar.status_code}")
        return deallista
    # Om inga specifika deals blev efterfrågade
    else:
        svar = requests.get("https://api.hubapi.com/crm/v3/objects/deals", headers=headers, params=params)
        # Request lyckades
        if svar.status_code == 200:
            deallista = svar.json()["results"]
            return deallista
        # Request misslyckades 
        else:
            print(f"Request misslyckades: {svar.status_code}")
            return []

def få_hubspot_kunder(kundidn=None,
                      antal_kunder=10,
                      hubspot_api_key="pat-na1-003cd583-9877-4c70-97ba-4c8cb7b980e0"):
    '''
    Function för att få kunder från Hubspot contacts API:t.

    Parametrar:
    hubspot_api_key (str, default: pat-na1-003cd583-9877-4c70-97ba-4c8cb7b980e0): API-nyckeln.
    antal_kunder (int, default: 10): Antalet kunder att hämta.
    kundidn (list, default: None): Lista av kund-ID:n att hämta.

    Output: Lista med Hubspot-kunderna.
    
    '''
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
        print(f"Request misslyckades: {svar.status_code}")
        return []



def få_payments(order_numbers, wsdl="http://localhost:3080/ws/bs.wsdl"):
    client = zeep.Client(wsdl=wsdl)

    paymentlista = []
    for order_number in order_numbers:
        try:
            payment = client.service.getPayment(order_number)
        except zeep.exceptions.Fault:
            print(f"Payments Request \"{order_number}\" misslyckades.")
            continue
        if payment != None:
            payment_info = {
                "orderNumber": payment["orderNumber"],
                "amount": payment["amount"],
                "currency": payment["currency"],
                "method": payment["method"],
                "status": payment["status"]
            }
            paymentlista.append(payment_info)

    return paymentlista

def få_credits_kunder(customer_numbers, wsdl="http://localhost:3080/ws/bs.wsdl"):
    client = zeep.Client(wsdl=wsdl)

    creditlista = []
    for customer_number in customer_numbers:
        try:
            credit = client.service.getCredit(customer_number)
        except zeep.exceptions.Fault:
            print(f"Credits Request \"{customer_number}\" misslyckades.")
            continue
        if credit != None:
            credit_info = {
                "customerNumber": credit["customerNumber"],
                "amount": credit["amount"],
                "currency": credit["currency"],
            }
            creditlista.append(credit_info)

    return creditlista

if __name__ == "__main__":
    # Se resultat här nere
    print(få_status_newsletters())
    print(få_newsletters_kunder(limit=5))
    print(få_hubspot_kunder(kundidn=[51, 1]))
    print(få_hubspot_kunder(antal_kunder=10))
    print(få_hubspot_deals(dealidn=[9801031437, 9801031438]))
    print(få_hubspot_deals(antal_deals=2))
    print(få_hubspot_companies(companyidn=[9366363952, 9366363956]))
    print(få_hubspot_companies(antal_companies=2))
    print(få_payments(order_numbers=["330495", "330496", "123456", "330497", "330498", "999999"]))
    print(få_credits_kunder(customer_numbers=["10001", "10002", "10003", "10004", "330495", "330496", "123456", "330497", "330498", "999999"]))
    print(få_newsletters_kunder())
    print(få_hubspot_kunder())
    print(få_hubspot_companies())
    print(få_hubspot_deals())
