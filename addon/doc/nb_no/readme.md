<div lang = "nb_no">
# Forbedret objektnavigering.
* Forfatter: Emil-18.
* NVDA-kompatibilitet: 2023.1 og utover.
* Last ned: [Stabil versjon](https://github.com/Emil-18/enhanced-object-navigation/releases/download/v0.1/enhancedObjectNavigation-0.1.nvda-addon).

Dette tillegget legger til forbedringer i objektnavigering. Merk at foreløpig fungerer det ikke i java-applikasjoner.

## Navigasjonsmodus.

For å gå inn i navigasjonsmodus, trykk NVDA+shift+control+mellomrom. Dette vil slå navigasjonsmodus på eller av til fokus flyttes.
Trykk to ganger for å lagre gjeldende tilstand.
Når navigasjonsmodus er slått på på denne måten, vil den automatisk slås på når fokus flyttes, med mindre fokuset lander i en redigerbar kontroll, et dokument i nett modus eller en virtuell kontroll opprettet av NVDA, for eksempel et OCR-resultatdokument. I disse tilfellene vil den bli slått av.
Hvis du havnet i en redigeringskontroll, kan du slå den på igjen ved å trykke på escape.

Navigasjonsmodus kan slås på i alle applikasjoner.

Merk:

Alle navigasjonskommandoer beskrevet nedenfor vil kun navigere til objekter i samme prosess som navigasjonsobjektet befinner seg i, med mindre annet er oppgitt.

De vil også navigere til objekter uavhengig av hierarki, med mindre annet er oppgitt.


### Grunnleggende kommandoer i navigasjonsmodus.

* Venstre og høyre pil: flytt navigasjonsobjektet til forrige og neste objekt.
* Pil opp og ned: Flytt til neste objekt avhengig av rotorinnstillingen.
* Side opp og ned: gå til neste/forrige rotorinnstilling.
* mellomrom: samhandle med kontrollen hvor navigasjonsobjektet er plassert. Dette kan inkludere å trykke på en knapp, merke av i en avkryssingsboks eller sette fokus på et redigeringsfelt slik at du kan begynne å skrive.
* Enter, applikasjonstast, shift+f10: sett fokus på navigasjonsobjektet, og send deretter den trykkte tasten gjennom til applikasjonen.

### Avansert navigasjon.

For å slå på avansert navigasjon, trykk NVDA+A mens du er i navigasjonsmodus. NVDA vil huske tilstanden til den avanserte navigasjonsmodusen mellom økter.

Når avansert navigasjon er slått på, vil piltastene flytte deg rundt på samme måte som vanlig objektnavigering. «enkel lesemodus»-innstillingen vil påvirke hva du kan navigere til.
Når du bruker disse kommandoene, kan du navigere utenfor den gjeldende prosessen.
Når avansert navigasjon er slått på, er ikke rotoren tilgjengelig, men alle andre kommandoer fungerer som normalt, bortsett fra piltastene som beskrevet ovenfor.

### enkeltbokstavnavigering.

Når navigasjonsmodus er slått på, kan du bruke enkeltbokstavnavigering, som i nettmodus, for å hoppe til forskjellige typer objekter.

Følgende enkeltbokstav navigasjonstaster  støttes for øyeblikket.
Trykk på tasten alene for å hoppe til neste objekt, legg til skift for å hoppe til forrige objekt, og legg til skift og kontroll for å liste opp alle objektene.

* b: knapp.
* c: kombinasjonsboks.
* d: dokument.
* e: redigeringskontroller.
* f: skjemafelt.
*g: grafikk.
*h: overskrift (kun støttet i edge).
*i: listeelement.
* j:fokuserbar kontroll.
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
* w: kontroll (område som kan omdefineres med [Enhanced control support-tillegget](https://github.com/emil-18/enhanced-control-support)).
* x: avkrysningsboks.
* z: statuslinje.

Alle disse er tilgjengelige i rotoren også.
## Objektlisten.

Objektlisten er en virtuell liste som inneholder objektene du har listet opp, for eksempel ved å trykke kontroll+shift+b mens du er i navigasjonsmodus for å liste opp knapper.
For å liste objekter uavhengig av rolle, trykk NVDA+control+enter. denne kommandoen er tilgjengelig selv når navigasjonsmodus er slått av.
Siden listen er virtuell, kan du gjøre ting som å liste alle objektene i en meny, uten at menyen lukkes, fordi systemfokuset ikke flyttes.

Når du er i listen, kan du begynne å skrive for å filtrere listen. Hold nede venstre alt og skriv inn et tegn for å flytte til neste objekt som starter med det tegnet.

Du kan bruke følgende kommandoer mens du er i listen.

* enter: flytt navigasjonsobjektet til det valgte elementet og lukk søkelisten.
* tilbaketast eller slett: fjern søketeksten og returner alle elementer til den.
* pil opp og ned: gå til neste eller forrige element.
* venstre og høyre pil: gå til neste eller forrige element som starter med et annet tegn.
* Hjem og slutt: Flytt til begynnelsen og slutten av listen.
* shift+backspace eller shift+delete: tilbakestill søketeksten. Dette vil beholde listen i gjeldende tilstand, men fjerner søketeksten, slik at du kan starte et nytt søk.
* escape: gå ut av søkelisten og returner fokuset og navigasjonsobjektet til der de var før du åpnet listen.

## Forbedret berøringsstøtte.

En ny berøringsmodus er lagt til, kalt navigasjon. Denne er ikke komplett ennå.
Bevegelsene for denne modusen er som følger.
* 1 finger sveip opp/ned: Flytt til neste/forrige objekt avhengig av rotorinnstillingen.
* sveip venstre med to fingre: gå til neste/forrige rotorinnstilling.
* sveip med tre fingre til høyre/venstre: trykk på tab/shift+tab.
* Sveip opp/ned med tre fingre: trykk på f6/shift+f6.
* sveip opp med to fingre: trykk på escape.
* Trippeltrykk med to fingre: liste opp alle objekter i vinduet der navigasjonsobjektet er plassert.
## Innstillinger.

* Bruk navigasjonsmodus som standard.
Denne innstillingen bestemmer om navigasjonsmodus skal slås på når fokus flyttes, det samme som å trykke NVDA+shift+control+mellomrom to ganger.
* Når du søker, sorter elementene i tabulatorekkefølge i stedet for alfabetisk.
Når slått på, vil søkelisten bli sortert i tabulatorrekkefølge i stedet for alfabetisk.
* Søkeomfang.
Dette er en kombinasjonsboks som lar deg velge omfang når du søker etter objekter.
Du kan nå velge mellom 3 alternativer.
    * Forgrunnsvinduet.
    * Alle objekter i operativsystemet.
    * Den gjeldende kontrollen som navigasjonsobjektet er i, for eksempel en liste eller en nettside.
* Bruk forbedret deteksjon mens du søker etter samme element.
Når denne er merket av, vil enkeltbokstav navigasjonstasten s  bare inkludere objekter som er programmatisk like, i stedet for alle objekter med samme rolle.
* Rapporter objektkontekst mens du navigerer i søkelisten.
Når det er merket av, vil NVDA rapportere objekter som inneholder objektet du landet i når du navigerte i listen hvis det er forskjellig fra det forrige objektet, slik NVDA vanligvis gjør når du flytter fokus.
* Sett fokus på elementet som er valgt i søkelisten.
Når det er merket av, vil NVDA prøve å automatisk sette fokus på objektet, i tillegg til å flytte navigasjonsobjektet til det, når du trykker enter i søkelisten.
* Aktiver elementet som er valgt i søkelisten.
Når det er merket av, vil NVDA automatisk utføre standardhandlingen på objektet som er valgt i søkelisten.
* Når du er i navigasjonsmodus eller i søkelisten, oppdater leselisten automatisk når innholdet til det viste objektet endres. Deaktiver hvis du får problemer med å bruke tillegget, for eksempel hakking. Selvforklarende.
* Når du er i søkelisten og holder nede venstre alt, bruk første bokstavsnavigasjon.
Når den er merket av, kan du holde nede venstre alt mens du er i søkelisten og trykke på tegn for å gå til neste element som starter med det tegnet.
* Bruk lyder for å indikere om navigasjonsmodus har blitt vekslet. Selvforklarende.

## forandringslog.

### v0.1.

Første utgivelse.
</div>