# Forbedret objektnavigering.
* Forfatter: Emil-18.
* NVDA-kompatibilitet: 2024.1 og utover.
* Last ned: [Stabil versjon](https://github.com/Emil-18/enhanced-object-navigation/releases/download/v0.3/enhancedObjectNavigation-0.3.nvda-addon).

Dette tillegget legger til forbedringer i objektnavigasjon. [Les dette hvis du ikke vet hva objektnavigasjon er eller hvordan du bruker det](https://afb.org/aw/fall2025/nvda-object-navigation-getting-started).
Dette tillegget legger til følgende:

* En navigasjonsmodus som lar deg bruke piltastene til å flytte navigasjonsobjektet mellom objekter. Du kan også bruke hurtignavigasjonskommandoer (b for knapp, x for avkryssingsboks, osv.), for å flytte navigasjonsobjektet til neste/forrige objekt av den angitte typen.
* muligheten til å liste opp objekter, søke etter objektet du er ute etter, og flytte direkte til det.
* bedre berøringsstøtte.

alle disse funksjonene påvirkes av «Enkel lesemodus»-innstillingen, så når innstillingen er slått av, vil du kunne finne flere objekter som ikke nødvendigvis er relevante for den gjennomsnittlige brukeren.

## Navigasjonsmodus.

For å slå på navigasjonsmodus, trykk NVDA+skjift + kontroll+mellomrom.
Navigasjonsmodus kan slås på i alle applikasjoner.

Merk:

Alle navigasjonskommandoer beskrevet nedenfor vil kun navigere til objekter i samme prosess som navigasjonsobjektet befinner seg i, med mindre annet er oppgitt.

De vil også navigere til objekter uavhengig av hierarki, med mindre annet er oppgitt.


### Grunnleggende kommandoer i navigasjonsmodus.

* Venstre og høyre pil: flytt navigasjonsobjektet til forrige og neste objekt.
* Pil opp og ned: Flytt navigasjonsobjektet til forrige og neste objekt avhengig av rotorinnstillingen.
* Side opp og ned: gå til neste/forrige rotorinnstilling.
* Mellomrom: samhandle med kontrollen hvor navigasjonsobjektet er plassert. Dette kan inkludere å trykke på en knapp, merke av i en avmerkingsboks eller sette fokus på et redigeringsfelt slik at du kan begynne å skrive.
* Enter, applikasjonstast, shift+f10: sett fokus på navigasjonsobjektet, og send deretter den trykkte tasten gjennom til applikasjonen.

### Avansert navigasjon.

For å slå avansert navigasjon på eller av, trykk på NVDA+A mens du er i navigasjonsmodus. NVDA vil huske tilstanden til den avanserte navigasjonsmodusen mellom øktene.

Når avansert navigasjon er slått på, vil piltastene flytte deg rundt på samme måte som vanlig objektnavigering, for eksempel pil opp for å flytte til objektet som inneholder navigasjonsobjektet, venstre og høyre pil til forrige/neste objekt, og pil ned flytter til det første objektet inne i navigasjonsobjektet.
Når du bruker disse kommandoene, kan du navigere utenfor den gjeldende prosessen.
Når avansert navigasjon er slått på, er ikke rotoren tilgjengelig, men alle andre kommandoer fungerer som normalt, bortsett fra piltastene som beskrevet ovenfor.

### enkeltbokstavnavigasjon.

Når navigasjonsmodus er slått på, kan du bruke enkeltbokstavnavigasjon, som i nettmodus, for å hoppe til forskjellige typer objekter. Følgende enkeltbokstavnavigasjonstaster støttes for øyeblikket.
Trykk på tasten alene for å hoppe til neste objekt, legg til skift for å hoppe til forrige objekt, og legg til skift og kontroll for å liste opp alle objektene.

* b: knapp.
* c: kombinasjonsboks.
* d: dokument.
* e: redigeringskontroll.
* f: skjemafelt.
* g: grafikk.
* h: overskrift.
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
* w: kontroll (områder som kan omdefineres med [Forbedret kontroll støtte-tillegget](https://github.com/emil-18/enhanced-control-support)).
* x: avkryssingsboks.
* y: fokuserbart skjemafelt.
* z: statuslinje.

Alle disse er tilgjengelige i rotoren også.

### UIA vs ingen UIA-navigasjonsmodus

Som standard bruker dette tillegget UI automasjon når du navigerer i navigasjonsmodus. Dette fører til at det går raskere, og det vil fungere på steder hvor NVDAs normale objektnavigasjon har problemer, men dette har noen bivirkninger.

* Den vil gjenkjenne noen objekter merkelig, for eksempel gjenkjenne tekst i Mozilla-applikasjoner som redigeringsbokser, og ikke gjenkjenne overskrifter i mange situasjoner.
* Den vil ikke gjenkjenne objekter som NVDA har tilpasset (enten i kjernen eller via andre tillegg). For eksempel, hvis objektet vises som en rute for skjermlesere normalt, men NVDA er tilpasset til å behandle det som en redigeringsboks, vil det bli behandlet som en rute av navigasjonsmodus når tilleget bruker UI-automasjon.

Du kan konfigurere tillegget til ikke eksplisitt å bruke UI automasjon i navigasjonsmodus. Når du gjør dette, navigerer tillegget gjennom objekter slik NVDA ser dem normalt, og du vil ikke oppleve noen av bivirkningene som er oppført ovenfor.

## Søkelisten.

Søkelisten lar deg vise objekter i en liste, søke etter objektet du vil ha, og flytte direkte til det. Du kan velge å liste opp hvert objekt i det gjeldende vinduet, hvert objekt i gjeldende nettmodusdokument eller alle objekter i operativsystemet.
uavhengig av dette kan du velge å liste opp alle objekttyper, eller bare typen assosiert med et spesifikt tegn, for eksempel kan du trykke på kontroll+skjift+b mens du er i navigasjonsmodus for å kun liste opp knapper.
For å liste objekter uavhengig av rolle, trykk NVDA+control+enter. Denne kommandoen er tilgjengelig selv når navigasjonsmodus er slått av. Du kan også trykke NVDA+shift+f7 hvor som helst, og deretter trykke på en navigasjonstast, f.eks. b for knapp, for bare å liste opp knapper.
### Den virtuelle søkelisten

Som standard bruker tillegget en virtuell liste for å liste opp objekter. Dette betyr at når du åpner listen og navigerer rundt i den, vises ingenting på skjermen, og systemfokuset flyttes ikke. Dette har flere fordeler og ulemper.
#### Fordeler:

* Mindre lastetid, og ingen lastetid i det hele tatt mens du skriver i listen,siden systemet ikke trenger å vise listeelementene.
* Muligheten til å brukes i områder som forsvinner når fokus flyttes bort fra dem.
* Rapportering av det faktiske objektet, inkludert eventuelle objekter som det er inne i, mens du beveger deg i listen.

#### Ulemper:

* Fungerer ikke med Windows-diktering.
* forsvinner når fokus flyttes bort fra den.
* Fungerer ikke bra med berøring.

Når du er i listen, kan du begynne å skrive for å filtrere listen. Hold nede venstre alt og skriv inn et tegn for å flytte til neste objekt som starter med det tegnet.
Du kan bruke følgende kommandoer mens du er i listen.

* enter: gå til det valgte elementet og lukk søkelisten.
* tilbaketast eller slett: fjern søketeksten og returner alle elementer til listen.
* pil opp og ned: gå til neste eller forrige element.
* venstre og høyre pil: gå til neste eller forrige element som starter med et annet tegn.
* Hjem og slutt: Flytt til begynnelsen eller slutten av listen.
* shift+backspace eller shift+delete: tilbakestill søketeksten. Dette vil beholde listen i gjeldende tilstand, men fjerner søketeksten, slik at du kan starte et nytt søk. Du kan for eksempel skrive "NV", trykke på denne kommandoen og skrive "A" og elementer som inneholder "NVDA" vil dukke opp.
* escape: gå ut av søkelisten og returner fokuset og navigasjonsobjektet til der de var før du åpnet listen.

### den fysiske søkelisten

Den fysiske søkelisten brukes alltid i java-applikasjoner, fordi den virtuelle søkelisten ikke støttes i dem. Du kan også konfigurere tillegget til å bruke den overalt.

#### Fordeler:

* vises visuelt på skjermen, og kan samhandles med som alle andre applikasjoner

#### Ulemper:

* Tar lengre tid å søke eller liste opp elementer.
* Kan ikke brukes i områder som forsvinner når fokus flyttes bort fra dem.

#### Kontroller i den fysiske søkelisten

* Filtrer etter kontrolltype redigeringsboks: Denne redigeringsboksen lar deg søke etter objekter som har en kontrolltype som starter med søket ditt. For eksempel, hvis du søker etter "knapp", vil alle knapper vises, og kontroller som radioknapper, som inneholder, men ikke starter med ordet "knapp", vil ikke vises.
* Filtrer etter navn redigeringsboks: Denne redigeringsboksen lar deg søke etter objektene i listen etter navn.
* Objektliste: Denne listen inneholder objektene du har søkt etter. Du kan bruke  førstebokstavsnavigasjon for å hoppe raskt til et element. Hvis du trykker mellomrom mens du er i listen, flyttes navigasjonsobjektet til objektet representert av det fokuserte listeelementet, men søkelisten vil ikke bli lukket.
* Flytt navigasjonsobjekt-knapp: Denne knappen lukker dialogen og flytter navigasjonsobjektet til objektet representert av det valgte listeelementet, uavhengig av hvilken modus du var i før du åpnet søkelisten.
* OK-knapp: Dette er standardknappen, aktivert ved å trykke enter. Dette vil flytte den aktive markøren til objektet representert av det valgte listeelementet,samme som å trykke enter i den virtuelle søkelisten

### Hva skjer når du trykker enter i søkelisten?

Listen lukkes, og:

* Hvis du var i navigasjonsmodus før du åpnet søkelisten, vil navigasjonsobjektet bli flyttet til objektet representert av gjeldende listeelement.
* Hvis objektet representert av det gjeldende listeelementet er i et nettmodusdokument, og hvis nettmodus er slått på for det dokumentet, flyttes nettmodusmarkøren.
* Ellers flyttes fokus. Hvis fokus ikke kan flyttes, flyttes navigasjonsobjektet i stedet.

## Forbedret berøringsstøtte.

En ny berøringsmodus er lagt til, kalt navigasjon. Dette er ikke komplett ennå.
Bevegelsene for denne modusen er som følger.
* 1 finger sveip opp/ned: Flytt til neste/forrige objekt avhengig av rotorinnstillingen.
* Sveip til venstre med to fingre: gå til neste/forrige rotorinnstilling.
* Sveip med tre fingre til høyre/venstre: trykk på tab/shift+tab.
* Sveip opp/ned med tre fingre: trykk på f6/shift+f6.
* Sveip opp med to fingre: trykk på escape.
* Trippeltrykk med to fingre: list opp alle objekter i vinduet der navigasjonsobjektet er plassert.
## Innstillinger.

* Bruk navigasjonsmodus som standard.
Denne innstillingen bestemmer om navigasjonsmodus skal være på som standard, det samme som å trykke på NVDA+shift+control+mellomrom.
* Når du søker, sorterer elementene i tabrekkefølge i stedet for alfabetisk.
Når slått på, vil søkelisten bli sortert i tabrekkefølge i stedet for alfabetisk.
* Søkeomfang.
Dette er en kombinasjonsboks som lar deg velge omfang når du søker etter objekter.
Du kan nå velge mellom 3 alternativer.
    * Forgrunnsvinduet.
    * Alle objekter i operativsystemet.
    * Det gjeldende dokumentet i søkemodus som navigasjonsobjektet er i.
* Bruk forbedret deteksjon mens du søker etter samme element.
Når det er merket av, vil navigasjonstasten s med én bokstav bare inkludere objekter som er programmatisk like, i stedet for alle objekter med samme rolle.
* Bruk UI-automasjon i navigasjonsmodus når tilgjengelig. Se delen "UIA vs ingen UIA-navigasjonsmodus".
* deaktiver asynkron navigasjon, nyttig hvis du støter på problemer mens du navigerer, for eksempel at NVDA blir stille eller spiller av feillyder. Når dette ikke er krysset av, og når du søker etter elementer som knapper med navigasjonsmodus, vil ikke NVDA fryse mens den søker. Gjelder bare når «Bruk UI-automasjon i navigasjonsmodus når tilgjengelig»-innstillingen er slått på. Hvis den ikke er slått på, vil denne bli behandlet som avkrysset.
* Bruk en virtuell liste når du lister opp objekter (fungerer ikke i Java-applikasjoner). Se delen "Søkeliste".
* Innstillinger for den virtuelle søkelisten:
    * Rapporter objektkontekst mens du navigerer i søkelisten.
    Når det er krysset av, vil NVDA rapportere objekter som inneholder objektet du havnet i når du navigerte i listen hvis det er forskjellig fra det forrige objektet, slik NVDA vanligvis gjør når du flytter fokus.
    * Når du er i søkelisten og holder nede venstre alt, bruk første bokstavsnavigasjon. Når det er krysset av, kan du holde nede venstre alt mens du er i søkelisten og trykke på tegn for å gå til neste element som starter med det tegnet.
* Innstillinger for den fysiske søkelisten:
    * Bruk UI-automasjon når du lister opp objekter (samme som i den virtuelle søkelisten).
    * Bruk regulære uttrykk når du søker.
    Når det er merket av, kan regulære uttrykk brukes til å søke etter navn på objekter
* Når du er i navigasjonsmodus eller i søkelisten, oppdater leselisten automatisk når innholdet til det viste objektet endres. Deaktiver hvis du får problemer med å bruke tillegget, for eksempel hakking. Selvforklarende.

* Bruk lyder for å indikere om navigasjonsmodus har blitt vekslet. Selvforklarende.


## Forandringslogg.

### v0.3

* Lagt til en valgfri fysisk søkeliste.
* Lagt til støtte for java-applikasjoner.
* Lagt til muligheten for å ikke bruke UI-automasjon når du navigerer i navigasjonsmodus.
* Tillegget vil nå respektere "enkel lesemodus"-innstillingen
* Når du trykker mellomrom i et redigeringsfelt, vil tillegget automatisk gå inn i skjemamodus. Du trenger ikke lenger å trykke mellomrom to ganger.

### v0.2.2
* Lagt til kompatibilitet med NVDA 2025.1

### v0.2
* Fjernet konseptet med å lagre navigasjonsmodus. Nå lagres den automatisk når gesten trykkes én gang.
* Navigasjonsmodus vil ikke lenger slå seg av automatisk når fokus flyttes, bortsett fra hvis fokus lander i et dokument i nettmodus der nettmodus er aktivert. For å gå inn i skjemamodus må du trykke mellomrom på en redigerbar kontroll. én gang hvis kontrollen har fokus, og to ganger på annen måte.
* Når du trykker enter på et element i søkelisten, flyttes den aktive markøren. Hvis navigasjonsmodus er aktiv, flyttes navigasjonsobjektet. Hvis objektet som representeres av det gjeldende elementet er i et nettmodusdokument og nettmodus er slått på, flyttes nettmodusmarkøren.
ellers flyttes fokuset. Hvis fokus ikke kan flyttes, flyttes navigasjonsobjektet i stedet.
* Rettet en feil der NVDA noen ganger krasjet ved avslutning eller omstart.
* Gjorde søket etter neste og forrige objekt i navigasjonsmodus asynkront.
* Lagt til en ny hurtignavigasjonstast, y, som er for fokuserbare skjemafelt.
* Fjernet "Sett fokus til elementet valgt i søkelisten" og "Aktiver elementet valgt i søkelisten"-innstillingene

### v0.1.1

* gestene i søkelisten skal nå fungere overalt
* Du bør kunne bruke navigasjonsmodus i flere situasjoner

### v0.1.

Første utgivelse.