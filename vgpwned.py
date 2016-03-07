import hashlib,urllib, urllib2, hmac, base64,json
from base64 import b64encode

def bygglenke(versjon):
    #Generer lenker for vg-pluss-artikler
    lenken = ''
    if versjon == 0:
        lenken='http://ws.vg.no/api/ipad/lastEditions?clientType=iphone&clientVersion=1.3&format=json&publicKey=11e46c971f1eba3e00fb1f03306dc415&timestamp='
    else:
        lenken = 'http://ws.vg.no/api/ipad/edition?clientType=iphone&clientVersion=1.3&editionId=' + str(versjon) + '&format=json&layoutFilter=iphone&publicKey=11e46c971f1eba3e00fb1f03306dc415&timestamp='        
    
    #Signer-klassen: public static final String PRIVATE_KEY = "d7df18b06b8aa839607dc465340fcfae"; - darlig sikkerhet. Denne finnes i no/vg.pluss/services/signature pakken.
    private_key = "d7df18b06b8aa839607dc465340fcfae"

    #Henter timestamp fra vg pa formaten som blir brukt i Android-applikasjonen. Dette er fra no/vg.pluss/services/constants pakken.
    #public static final String SERVER_TIMESTAMP_FORMAT = "E, dd MMM YYY HH:mm:ss Z";
    timestamp = urllib.quote(urllib2.urlopen('http://ws.vg.no/api/time').read()[0:16].replace(' ', 'T') + 'Z')
    lenken += timestamp + "&version=5"

    #Generer signatur som outlina i apk. (no/vg.pluss/services/constants pakka.) Spiller ingen rolle om noe er dynamisk nar det er forutsigbart.
    signature = b64encode(hmac.new(private_key, msg=lenken, digestmod=hashlib.sha256).digest())
    lenken += "&signature=" + signature
    return lenken
 
 

#Her ligger jsondata om samtlige artikler pa vg pluss.
jsonData = json.loads(urllib2.urlopen(bygglenke(0)).read())
print bygglenke(0)
#print jsonData
 #Skriver om url i henhold til adressen i json-objektet 
def lagURL(printurl, shareurl):
    return shareurl[:35] + printurl[29:]


#Iterer over alt i json-objektet, lager URLer og printer det ut pa et "leselig format."
for edition in jsonData:
    try:
        url = bygglenke(edition['id'])
        #print url
        artiklene = json.loads(urllib2.urlopen(url).read())
        try:
            for seksjoner in artiklene['sections']:
                for artikler in seksjoner['compiledArticles']:
                    print "Published: "+ artikler['publishDate']['iphone']+"  Tittel: "+artikler['title'] + ":\nLenke: " + lagURL(artikler['printUrl'], artikler['shareUrl']) +"\n"
                    #Dette vil skrive ut samtlige vgpluss artikler fra de siste 14 dagene.
        except:
            pass
    except:
        pass
