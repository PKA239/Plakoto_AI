# Plakoto AI
Mit der Plakoto AI Anwendung kann man Plakoto gegen mit Deep-Q-Learning trainierte
AI Agents spielen, oder dsiese gegeneinander antreten lassen.
Als Codebasis wurde das Projekt https://github.com/weekend37/Backgammon genutzt.

## Wie das Projekt gestartet wird
Laden Sie das Projekt herunter und installieren Sie alle notwendigen Packages.
Das Programm wird mit dem Ausführen von Plakoto.py gestartet.

## Aufbau des Spielbrettes
Das Spiel ist in der Datei **Plakoto_game.py** implementiert.
Es gibt die Spieler 1 und -1.
Insgesamt werden 50 Positionen benutzt:
- Die Positionen 1-24 stellen die Spielpositionen auf dem Brett dar.
- Die Positionen 25-48 geben zu jeder Position auf dem Brett die Information, ob auf diesem Feld ein Spielstein geblockt wird.
- An die Positionen 49 und 50 werden die aus dem Spiel entfernten Spielsteine gesetzt. 49 für Spieler 1. 50 für Spieler -1.
- Position 0 wird nicht genutzt.

Die Anzahl der Spielsteine auf einem Feld n ist duch |n| gegeben.
Welchem Spieler das Feld gehört list sich am Vorzeichen von n ab.
Die Position n+24 gibt auserdem an, ob sich unter den |n| steiben von
Spieler sign(n) ein geplackter Stein des gegenspielers befindet.
Die Position n+24 kann die Werte 1, -1 oder 0 haben;
1 und -1 für den jeweiligen geblockten Spielstein, oder 0, falls kein geblockter Stein vorhanden ist.

Beispiele:
- `board[23] = 3`
    `board[23+24] = -1` bedeuted, dass Spieler 1 3 Steine auf Feld 23 hat und dabei einen Stein von Spieler -1 blockt.
- `board[21] = -10` `board[21+24] = 0` bedeuted, dass -1 10 Steine auf Feld 21 des Brettes hat und dabei keinen gegnerischen Stein blockt.

## Das Bewegen von Spielsteinen
Ein Spiel wird zwischen Agents gespielt. Der Agent für dieses Spiel ist in der Datei **psai.py**.
In einem Plakoto Spiel wird dieser Agent importiert. 
Der Agent gibt zu einem bestimmten board und Würfelpaar seinen besten Zug zurück.
Züge werden als eine Liste von Zahlenpaaren zurückgegeben.
- Die erste Zahl eines Paares gibt die Startposition des Zuges an.
- Die zweite Zahl eines Paares gibt die Endposition des Zuges an.

Da zu der Runde des Spielers zwei Würfel gehören, gibt ein Agent typischerweise eine Liste mit zwei Zügen zurück.
Für die Fälle, dass es nur einen möglichen Zug, oder gar keinen gibt, kann die Liste auch nur einen Zug enthalten, oder leer sein.

Für den Fall eines Pasches, darf ein Spieler mit demselben Augenpaar zweimal rücken.
In diesem Fall wird der Agent zweimal aufgefordert, seine Spielzüge zu bestimmen.
Er gibt nicht etwa eine einzelne Liste von vier Zügen zurück.

## Die Dateien
### Plakoto.py
In Plakoto.py ist das Hauptmenü angelegt.
Von dort aus werden pygame gestartet, die Agents ausgewählt und die Spiele oder Simulationen gestartet.

### Plakoto_game.py
In Plakoto_game.py ist die Spiellogik implementiert.
Hier läuft die Hauptroutine eines Spieles ab.
In dieser werden abwechselnd die Züge der Agents abgefragt.

### classGUI.py
classGUI.py implementiert die grafische Oberfläche.
Hier wird das Spielbrett mit Checkern und Würfeln gezeichnet und die jeweiligen Bilder dafür geladen.


### psai.py
psai ist der Agent für Plakoto.
Hier befindet sich der Code für das zu trainiernde Netz,
für die Auswahl von Zügen und für das Deep-Q-Learning.

### userAgent.py
userAgent.py ist ein Agent, der beim Spielen eines Benutzers verwendet wird.
Er erfasst die Eingaben, die der Benutzer während des eigenen Zuges tätigt
und gibt diese als Liste der gewählten Züge zurück.
Schwerpunkt ist es außerdem, dem Benutzer ein grafisches Feedback zum Stand seines Zuges zu geben.
Das geschieht durch das Setzen und Löschen von blauen Markern an den Startpositionen eines Zuges.

### randomAgent.py
randomAgent.py ist ein einfacher Agent, der einen zufälligen korrekten Zug zurückgibt.
Der randomAgent wird als Gegenspieler zur Bewertung trainierter Agents benutzt.

### train.py
train.py enthält Funktionen zum trainieren und evaluieren eines Agents.
