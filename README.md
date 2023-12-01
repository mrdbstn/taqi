# Taqi

Run this application with
```
docker-compose up
```
Then visit http://localhost:3000

## TO-DO
- Fix CSRF
- Fix CORS
- E2E Testing
- Meer comments/docs
- Haal Next uit dev mode.

  
## Questions
### API-endpoints
- Hoe zou je een API endpoint ontwerpen waarmee externe applicaties
toegang krijgen tot de gegevens van de leden?

Maak een api-endpoint genaamd "api/members" die een lijst van leden terugstuurt met de parameters limit en offset, die aangeven welke subset van het leden bestand opgestuurd moeten worden. Deze zouden een bepaalde default waarden hebben als ze niet worden meegestuurd en limit zou een bepaalde limiet hebben. Een tweede api-endpoint genaamt "api/members/<id\>" zou een specifiek lid kunnen ophalen

- Welke authenticatie- en autorisatiemethoden zou je gebruiken om te zorgen
dat de API veilig is?

Implementeer OAuth in de Django applicatie waarmee iemand zich kan authentiseren in de applicatie. De gebruiker kan na authorisatie een API-sleutel ophalen die hij mee kan sturen met het request om zichzelf te authoriseren.

### Beveiligingsimplementatie
- Hoe zou je de uploadfunctionaliteit beveiligen om te voorkomen dat
kwaadwillenden schadelijke bestanden uploaden?

Zorg dat alleen .xlsx bestanden geuploadt kunnen worden. Dit wordt gedaan in de process_csv view. Verder zou je een bestandgrootte limiet moeten aanhouden en meer geavanceerde parsing van het bestand moeten doen om te valideren dat het niet om een kwaadwillend bestand gaat. Ten slotte zou je virus scanning kunnen implementeren, maar ik heb hier persoonlijk geen ervaring mee en weet niet hoe schaalbaar dat is.

- Welke stappen zou je ondernemen om de database te beveiligen tegen
mogelijke aanvallen, zoals SQL-injectie?

Aangezien ik alleen gebruik maak van de Django ORM, is de kans op SQL-injectie klein (maar nooit 0), sinds er geen pure SQL queries worden gemaakt en uitgevoerd op de database. Verder zou je de cellen van het bestand kunnen sanitizen en zo potentiële injecties kunnen voorkomen.

### Database Optimalisatie
- Hoe zou je de gegevens in de database normaliseren om redundantie te
vermijden?

1. Een custom e-mail veld maken die de validatie automatisch doet, zodat het reusable is in de toekomst. 
2. Family en Team zijn nu precies hetzelfde model praktisch gezien. Je kan een Group model maken en Family en Team een 1-to-1 relatie geven met dit Group model. Hoewel ik denk dat deze verandering meer complexiteit met zich mee brengt t.o.v. de redundantie die het vermindert.

- Welke indexeringstechnieken zou je toepassen om de query-efficiëntie te
verbeteren, gezien het feit dat we vaak zoeken op e-mailadressen en
teamnamen?

1. Zet een index op e-mail van User en team_name van Team met db_index=True
2. Breng de applicatie in productie en verzamel data over de queries die door users uiteindelijk uitgevoerd worden. Op basis daarvan kan je verdere optimalisaties ontwikkelen.

### Error Handling
- Hoe zou je foutafhandeling implementeren voor het geval een gebruiker een
corrupt Excel-bestand probeert te uploaden?

Wrap het lezen van de het excel bestand in een try. Return een error-code naar de gebruiker als dit faalt. Zie process_csv

- Hoe zou je omgaan met onverwachte waarden in het Excel-bestand, zoals
ontbrekende of ongeldige e-mailadressen?

Ik hou bij welke rijen van het excel bestand een foute/missende waarde hebben en laat dat weten aan de gebruiker. Zie parse_spreadsheet

### Testing
- Welke benadering zou je gebruiken voor het schrijven van unit tests voor
deze applicatie? Welke delen van de code zou je prioriteit geven?

De belangrijkste unit-test is test_parse_spreadsheet. process_csv testen was iets lastiger door wat serializatie issues die meer tijd nodig zouden hebben om op te lossen. Sinds dit van scratch is gemaakt heb ik de tests na minimale setup geschreven. Voor nieuwe functionaliteit zou ik TDD aanhouden.

- Hoe zou je end-to-end tests opzetten en uitvoeren, gezien de functionaliteit
van de applicatie?

Met Cypress zou ik de hele flow van uploaden vanaf de frontend testen. Met Cypress zou dan een upload worden uitgevoerd met een test bestand en kan het resultaat dat wordt getoond op het scherm vergeleken worden met verwachtte waardes

### Algemene Ontwikkelingsvragen:
- Welke Django-extensies of externe bibliotheken zou je overwegen te
gebruiken voor deze opdracht en waarom?
  1. Django Rest Framework: Sneller API opzetten voor mijn modellen
       - Hiermee kan je ook typing voor client-side code automatiseren voor Typescript aan de hand van je database model, which is very nice.
  2. React-query: Beter state-management bij het data fetchen.
  3. Django OAuth Toolkit: Voor het opzetten van OAuth flow.
   

- Hoe zou je de applicatie schaalbaar maken voor duizenden gebruikers en
uploads?

Maak het uploaden, processen en parsen van een spreadsheet asynchroon.