# ❌⭕ Win-Tac-Toe ⭕❌
Win-Tac-Toe ist eine interaktive Spielbox, die es ermöglicht, Tic-Tac-Toe um echtes Geld zu spielen, indem das Spiel über einen eingebauten Joystick gesteuert wird, sodass Spieler*innen auf einfache Weise Strategie und potenziellen Gewinn miteinander verbinden können, wobei die gewinnende Person des Spiels den gesamten Einsatz erhält.

# ⭐ Kozept
**🎮 Spielstart:**
Das Spiel beginnt, sobald eine Münze eingeworfen und vom Modulino Distance Sensor erkannt wird. Eine LED-Animation und eine Soundansage signalisieren den Start.
Spielablauf:
Spieler/in 1 (Blau) und Spieler/in 2 (Rot) wechseln sich ab und setzen mithilfe eines Joysticks ihre Züge auf dem LED-Spielfeld.

**🏆 Gewinnbedingung:**
Ein/e Spieler/in gewinnt eine Runde, sobald eine gültige Gewinnkombination erreicht wird. Wer zuerst drei Runden gewinnt, entscheidet das Spiel für sich.

**🏁 Spielende:**
Nach der Siegerankündigung kann der/die Gewinner/in die beleuchtete Klappe öffnen und die Münze entnehmen. Danach ist das Spiel bereit für einen Neustart.

# 🎥 Video

# 📜 Spielanleitung
1. Wirf eine Münze in den Schlitz. 🪙
  <img width="171" height="179" alt="image" src="https://github.com/user-attachments/assets/f96f0514-c64c-4650-bdc8-79369ac0e5f9" />


2. Warte, bis die Spielankündigung erscheint.
3. Spieler/in Blau beginnt das Spiel. 💙
4. Bewege den Joystick nach vorne oder nach hinten, um den Auswahlpunkt über die LEDs zu bewegen. 🕹️
  <img width="185" height="178" alt="image" src="https://github.com/user-attachments/assets/3b949948-32d9-41c9-a0e9-66e836bfa789" />


6. Drücke auf den Joystick, um das ausgewählte Feld zu setzen. 🕹️
7. Danach ist Spieler/in Rot an der Reihe. ❤️
8. Die Spieler/innen wechseln sich ab.
9. Sobald eine Spielerin oder ein Spieler eine **Gewinnkombination in der eigenen Farbe** erreicht, gewinnt diese Person die Runde. 🎉
  <img width="768" height="468" alt="image" src="https://github.com/user-attachments/assets/f919c7cb-f4da-4c1d-a0cb-7f27a546e60d" />


10. Das Spiel wird so oft wiederholt, bis eine Spielerin oder ein Spieler **drei Runden** gewonnen hat. 🏆🏆🏆
11. Warte auf die Siegerankündigung.
12. Der/die Gewinner/in kann die hintere Klappe öffnen, um die Münze herauszuholen. 🪙
  <img width="264" height="151" alt="image" src="https://github.com/user-attachments/assets/82b2fb5d-04f3-4915-b263-c83c4d61020f" />


13. Schliesse die Klappe wieder.
14. Das Spiel kann bei Bedarf erneut gestartet werden.

# 👾 Anforderungen Software / Hardware
- Arduino Nano ESP32: 1 Stk. 
- Modulino Distance: 1 Stk. 
- Modulino Pixels : 1 Stk. 
- OLED Bildschirm: 1 Stk. 
- Joystick: 1 Stk. 
- MP3- Player: 1 Stk.  
- SD Karte klein: 1 Stk. 
- Soundbox klein: 1 Stk. 
- NeoPixel LED Strip: 9 LEDs durch 3 teilen und zusammen löten
<img width="727" height="395" alt="image" src="https://github.com/user-attachments/assets/a093c997-93dd-4384-bf01-3e13b8f341b8" />

# 🛠️ Aufbau
<img width="797" height="251" alt="image" src="https://github.com/user-attachments/assets/167bc55d-6979-473c-bbbb-b3785e154e8c" />


**Wichtig zu beachten:**
- Der NeoPixel-LED-Streifen muss genau in der vorgesehenen Anordnung montiert werden, da das Spiel sonst nicht korrekt funktioniert.
- Der Joystick wird durch das obere Loch geführt, der OLED-Bildschirm durch das rechteckige Loch unterhalb des Münzschlitzes.
- Im Inneren der Box muss der Bereich direkt unter dem Münzschlitz frei bleiben, damit die Münze ausreichend Platz hat und direkt auf den Modulino Distance Sensor fallen kann. Wir haben ein Stück Karton benutzt, um diesen Bereich zu erhöhen.
- Der Joystick muss im Inneren der Box stabil fixiert werden, zum Beispiel mit einem dünnen Holzstab oder einer anderen festen Stütze, damit er sich beim Spielen nicht verschiebt.
- Die Modulino Pixels können an der Decke der Box befestigt werden.
- Die restlichen Komponenten müssen kompackt in der Box verstaut werden.
