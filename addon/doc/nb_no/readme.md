<p lang = "nb_no">
# Forbedret objektnavigering.
* Forfatter: Emil-18.
* NVDA-kompatibilitet: 2024.1 og utover.
* Last ned: [Stabil versjon](https://github.com/Emil-18/enhanced-object-navigation/releases/download/v0.2/enhancedObjectNavigation-0.2.nvda-addon).

Dette tillegget legger til forbedringer i objektnavigering. Merk at foreløpig fungerer det ikke i java-applikasjoner.

## Navigasjonsmodus.

For å slå på navigasjonsmodus, trykk NVDA+shift+control+mellomrom.
Navigasjonsmodus kan slås på i alle applikasjoner.

Merk:

Alle navigasjonskommandoer beskrevet nedenfor vil kun navigere til objekter i samme prosess som navigasjonsobjektet befinner seg i, med mindre annet er oppgitt.

De vil også navigere til objekter uavhengig av hierarki, med mindre annet er oppgitt.


### Grunnleggende kommandoer i navigasjonsmodus.

* Venstre og høyre pil: flytt navigasjonsobjektet til forrige og neste objekt.
* Pil opp og ned: Flytt navigasjonsobjektet til forrige og neste objekt avhengig av rotorinnstillingen.
* Side opp og ned: gå til neste/forrige rotorinnstilling.
* mellomrom: samhandle med kontrollen hvor navigasjonsobjektet er plassert. Dette kan inkludere å trykke på en knapp, merke av i en avmerkingsboks eller sette fokus på et redigeringsfelt slik at du kan begynne å skrive.
* Enter, applikasjonstast, shift+f10: sett fokus på navigasjonsobjektet, og send deretter den trykte tasten gjennom til applikasjonen.

### Avansert navigasjon.

For å slå på avansert navigasjon, trykk NVDA+A mens du er i navigasjonsmodus. NVDA vil huske tilstanden til den avanserte navigasjonsmodusen mellom økter.

Når avansert navigasjon er slått på, vil piltastene flytte deg rundt på samme måte som vanlig objektnavigering, f.eks pil opp for å flytte til objektet som inneholder navigasjonsobjektet, venstre og høyre pil til forrige/neste objekt, og pil ned flytter til det første objektet inne i navigasjonsobjektet. «Enkel lesemodus»-innstillingen vil påvirke hva du kan navigere til.
Når du bruker disse kommandoene, kan du navigere utenfor den gjeldende prosessen.
Når avansert navigasjon er slått på, er ikke rotoren tilgjengelig, men alle andre kommandoer fungerer som normalt, bortsett fra piltastene som beskrevet ovenfor.

### enkeltbokstavnavigering.

Når navigasjonsmodus er slått på, kan du bruke enkeltbokstavnavigering, som i nettmodus, for å hoppe til forskjellige typer objekter.

Følgende enkeltbokstavsnavigasjonstaster støttes for øyeblikket.
Trykk på tasten alene for å hoppe til neste objekt, legg til skift for å hoppe til forrige objekt, og legg til skift og kontroll for å liste opp alle objekter.

* b: knapp.
* c: kombinasjonsboks.
* d: dokument.
* e: redigeringskontroll
* f: skjemafelt.
* g: grafikk.
* h: overskrift (kun støttet i Edge).
* i: listeelement.
* j: fokuserbar kontroll.
*k: lenke.
* l: liste.
* m: meny, menylinje eller menyelement.
* n: landemerke.
* o: verktøylinje.
*p: tekst.
* q: fane eller faneelement.
*r: radioknapp.
*s: samme objekt.
*t: tabell.
* u: gruppe.
* v: tre eller treelement.
* w:kontroll (områder som kan omdefineres med [Enhanced control support-tillegget](https://github.com/emil-18/enhanced-control-support)).
* x: avkrysningsboks.
* y: fokuserbart skjemafelt.
* z: statuslinje.

Alle disse er tilgjengelige i rotoren også.
## Søkelisten.

Søkelisten er en virtuell liste som inneholder objektene du har listet opp, for eksempel ved å trykke kontroll+shift+b mens du er i navigasjonsmodus for å liste opp knapper.
For å liste objekter uavhengig av rolle, trykk NVDA+control+enter. Denne kommandoen er tilgjengelig selv når navigasjonsmodus er slått av. Du kan også trykke NVDA+shift+f7 hvor som helst, og deretter trykke på en navigasjonstast, f.eks. b for knapp, for bare å liste opp knapper.
Siden listen er virtuell, kan du gjøre ting som å liste opp alle objektene i en meny, uten at menyen lukkes, fordi systemfokuset ikke flyttes.

Når du er i listen, kan du begynne å skrive for å filtrere listen. Hold nede venstre alt og skriv inn et tegn for å flytte til neste objekt som starter med det tegnet.

Du kan bruke følgende kommandoer mens du er i listen.

* enter: gå til det valgte elementet og lukk søkelisten.
* tilbaketast eller slett: fjern søketeksten og returner alle elementer til listen.
* pil opp og ned: gå til neste eller forrige element.
* venstre og høyre pil: gå til neste eller forrige element som starter med et annet tegn.
* Hjem og slutt: Flytt til begynnelsen og slutten av listen.
* shift+ tilbaketast eller shift+delete: tilbakestill søketeksten. Dette vil beholde listen i gjeldende tilstand, men fjerner søketeksten, slik at du kan starte et nytt søk. Du kan for eksempel skrive "NV", trykke på denne kommandoen og skrive "A" og elementer som inneholder "NVDA" vil dukke opp.
* escape: gå ut av søkelisten og returner fokuset og navigasjonsobjektet til der de var før du åpnet listen.

## Forbedret berøringsstøtte.

En ny berøringsmodus er lagt til, kalt navigasjon. Dette er ikke komplett ennå.
Bevegelsene for denne modusen er som følger.
* 1 finger sveip opp/ned: Flytt til neste/forrige objekt avhengig av rotorinnstillingen.
* 2 fingre sveip venstre: flytt til neste/forrige rotorinnstilling.
* sveip med tre fingre til høyre/venstre: trykk på tab/shift+tab.
* Sveip opp/ned med tre fingre: trykk på f6/shift+f6.
* sveip opp med to fingre: trykk på escape.
* Trippeltrykk med to fingre: list opp alle objekter i vinduet der navigasjonsobjektet er plassert.
## Innstillinger.

* Bruk navigasjonsmodus som standard.
Denne innstillingen bestemmer om navigasjonsmodus skal være på som standard, det samme som å trykke NVDA+shift+control+mellomrom.
* Når du søker, sorter elementene i tabulatorekkefølge i stedet for alfabetisk.
Når slått på, vil søkelisten bli sortert i tabulatorekkefølge i stedet for alfabetisk.
* Søkeomfang.
Dette er en kombinasjonsboks som lar deg velge omfang når du søker etter objekter.
Du kan velge mellom 3 alternativer.
    * Forgrunnsvinduet.
    * Alle objekter i operativsystemet.
    * Det gjeldende nettmodusdokumentet som navigasjonsobjektet er i.
* Bruk forbedret deteksjon mens du søker etter samme element.Når det er merket av, vil navigasjonstasten s  bare inkludere objekter som er programmatisk like, i stedet for alle objekter med samme rolle.
* Rapporter objektkontekst mens du navigerer i søkelisten.
Når det er merket av, vil NVDA rapportere objekter som inneholder objektet du havnet i når du navigerte i listen hvis det er forskjellig fra det forrige objektet, slik NVDA vanligvis gjør når du flytter fokus.
* Når du er i navigasjonsmodus eller i søkelisten, oppdater leselisten automatisk når innholdet til det viste objektet endres. Deaktiver hvis du får problemer med å bruke tillegget, for eksempel hakking. Selvforklarende.
* Når du er i søkelisten og holder nede venstre alt, bruk første bokstavsnavigasjon.
Når det er merket av, kan du holde nede venstre alt mens du er i søkelisten og trykke på tegn for å gå til neste element som starter med det tegnet.
* Bruk lyder for å indikere om navigasjonsmodus har blitt vekslet. Selvforklarende.
* deaktiver asynkron navigasjon, nyttig hvis du støter på problemer mens du navigerer, for eksempel at NVDA blir stille eller spiller av feillyder. Selvforklarende.

## Forandrings logg.


### v0.2
* Fjernet konseptet med å lagre navigasjonsmodus. Nå lagres den automatisk når kommandoen trykkes én gang.
* Navigasjonsmodus vil ikke lenger slå seg av automatisk når fokus flyttes, bortsett fra hvis fokus lander i et dokument i nettmodus der nettmodus er aktivert. For å gå inn i skjemamodus må du trykke mellomrom på en redigerbar kontroll. én gang hvis kontrollen har fokus, og to ganger hvis ikke.
* Når du trykker enter på et element i søkelisten, flyttes den aktive markøren. Hvis navigasjonsmodus er aktiv, flyttes navigasjonsobjektet. Hvis objektet som representeres av det gjeldende elementet er i et nettmodusdokument og nettmodus er slått på, flyttes nettmodusmarkøren.
ellers flyttes fokuset. Hvis fokus ikke kan flyttes, flyttes navigasjonsobjektet i stedet.
* Rettet en feil der NVDA noen ganger krasjet ved avslutning eller omstart.
* Gjorde søket etter neste og forrige objekt i navigasjonsmodus asynkront.
* Lagt til en ny hurtignavigeringstast, y, som er for fokuserbare skjemafelt.
* Fjernet "Sett fokus til elementet valgt i søkelisten" og "Aktiver elementet valgt i søkelisten"-innstillingene


### v0.1.1

* kommandoene i søkelisten skal nå fungere overalt
* Du bør kunne bruke navigasjonsmodus i flere situasjoner

### v0.1.

Første utgivelse.
</p>