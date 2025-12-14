# Win Tac Toe

from modulino import ModulinoDistance
from modulino import ModulinoPixels
from machine import Pin, ADC, I2C, UART   # UART dazu
from neopixel import NeoPixel
import time
import sh1106
from dfplayer import DFPlayer            # DFPlayer dazu


# ---------------------------
# Audio / DFPlayer
# ---------------------------

# UART zum DFPlayer (TX/RX ggf. an dein Board anpassen!)
uart = UART(0, tx=Pin("TX"), rx=Pin("RX"))
player = DFPlayer(uart)
player.volume = 90   # ziemlich laut, kannst du anpassen


# ---------------------------
# Hardware / Globals
# ---------------------------

# OLED Bildschirm (SH1106)
bus = I2C(1, sda=Pin("D9"), scl=Pin("D8"))
display = sh1106.SH1106_I2C(128, 64, bus)

display.fill(0)
display.show()

# Sensor (Münzenerkennung)
d = ModulinoDistance()

# NeoPixel-Streifen
LEDS = 9
pixels = NeoPixel(Pin("D5"), LEDS)
level_shift = Pin("D4", Pin.OUT)
level_shift.on()

# Joystick + Button
btn = Pin("A3", Pin.IN, Pin.PULL_UP)
joystick_x = ADC("A2")

# Empfindlichkeit und Kalibrierung
THRESHOLD = 6000

# Abstand (cm) bei dem die Münze erkannt wird
DISTANCE_TO_COIN = 2

# Farben
BLUE  = (0, 0, 255)        # Player Blue
RED   = (255, 0, 0)        # Player Red
WHITE = (255, 255, 255)
OFF   = (0, 0, 0)

# Gewinnkombinationen im LED Streifen (0-based)
WIN_CONDITIONS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (2, 3, 8),
    (1, 4, 7),
    (0, 5, 6),
    (0, 4, 8),
    (2, 4, 6)
]


# ---------------------------
# Hilfsfunktionen / Animationen
# ---------------------------

def check_win(field):
    """Gibt die Gewinnerfarbe (tuple) zurück oder None, wenn kein Gewinner."""
    for a, b, c in WIN_CONDITIONS:
        if field[a] is not None and field[a] == field[b] == field[c]:
            return field[a]
    return None


def animate_winner(color):
    for _ in range(4):
        pixels.fill(color)
        pixels.write()
        time.sleep(0.3)
        pixels.fill(OFF)
        pixels.write()
        time.sleep(0.3)


def animate_draw():
    for _ in range(3):
        pixels.fill(WHITE)
        pixels.write()
        time.sleep(0.2)
        pixels.fill(OFF)
        pixels.write()
        time.sleep(0.2)


def animate_champion(color):
    for _ in range(8):
        pixels.fill(color)
        pixels.write()
        time.sleep(0.15)
        pixels.fill(OFF)
        pixels.write()
        time.sleep(0.15)


def animate_champion_pixel(color):
    pixels_mod = ModulinoPixels()
    r, g, b = color
    pixels_mod.set_all_rgb(r, g, b)   # alle LEDs in Gewinnerfarbe
    pixels_mod.show()


def reset_pixels():
    for i in range(LEDS):
        pixels[i] = OFF
    pixels.write()


def show_lines(lines, duration=2):
    """Zeigt mehrere Textzeilen zentriert (links) auf dem OLED an."""
    display.fill(0)
    y = 8
    for line in lines:
        display.text(str(line), 0, y, 1)
        y += 12
    display.show()
    time.sleep(duration)
    display.fill(0)
    display.show()


def sound_intro():
    # 004.mp3 -> Ordner 1, Track 4
    player.play_track(1, 4)


def sound_round_win():
    # 001.mp3 -> Ordner 1, Track 1
    player.play_track(1, 1)


def sound_game_win():
    # 002.mp3 -> Ordner 1, Track 2
    player.play_track(1, 2)


def sound_collect_money():
    # 005.mp3 -> Ordner 1, Track 5
    player.play_track(1, 5)


def sound_game_over():
    # 006.mp3 -> Ordner 1, Track 6
    player.play_track(1, 6)


def sound_stop():
    player.pause()


# ---------------------------
# Münzenerkennung (Lauflicht)
# ---------------------------

def coin_detection():
    reset_pixels()
    pixels_mod = ModulinoPixels()
    pixels_mod.set_all_rgb(0, 0, 0)   # alles aus
    pixels_mod.show()

    def welcome():
        sound_intro()
        show_lines(["Welcome to:", "Win Tac Toe!"], duration=3)
        # 🔊 Intro-Sound direkt am Start, bevor Coin
        show_lines(["Insert", "your coin!"], duration=2)

    welcome()

    while True:
        dist = d.distance  # Annahme: property oder Attribut
        if dist is None:
            time.sleep(0.1)
            continue

        if dist < DISTANCE_TO_COIN:
            # Lauflicht: jede LED nacheinander weiss
            for i in range(LEDS):
                pixels[i] = WHITE
                pixels.write()
                time.sleep(0.15)
            reset_pixels()
            time.sleep(0.2)
            break
        else:
            reset_pixels()

        time.sleep(0.1)


# ---------------------------
# Eine einzelne Runde spielen
# ---------------------------

def play_single_round():
    """
    Spielt eine einzelne Tic-Tac-Toe-Runde.
    Rückgabe:
      - BLUE  -> Player Blue gewinnt die Runde
      - RED   -> Player Red gewinnt die Runde
      - None  -> Unentschieden
    """
    # Re-Kalibrierung des Joysticks pro Runde
    center = joystick_x.read_u16()

    # Spielfeld initialisieren
    field = [None] * LEDS      # None = frei, sonst Farbe (tuple)
    locked = [False] * LEDS    # True = Feld belegt / fixiert
    wander_color = BLUE        # Player 1 beginnt
    led_index = 0
    last_btn = 1

    reset_pixels()

    show_lines(["Player Blue:", "Make your move!"], duration=1)

    # Zeige initialen Cursor (wandernden Pixel) falls frei
    if not locked[led_index]:
        pixels[led_index] = wander_color
        pixels.write()

    while True:
        btn_val = btn.value()

        # Taste gedrückt -> Feld setzen
        if last_btn == 1 and btn_val == 0:
            if not locked[led_index]:
                # fixieren
                locked[led_index] = True
                pixels[led_index] = wander_color
                pixels.write()

                field[led_index] = wander_color

                # Gewinner prüfen
                winner = check_win(field)
                if winner is not None:
                    # 🔊 Runde gewonnen
                    sound_round_win()
                    animate_winner(winner)
                    return winner  # Runde beendet -> Gewinner zurückgeben

                # Unentschieden prüfen
                if all(locked):
                    animate_draw()
                    return None  # Unentschieden -> None zurückgeben

                # Spieler wechseln und Ansage
                if wander_color == BLUE:
                    wander_color = RED
                    time.sleep(1)
                    show_lines(["Player Red:", "Make your move!"], duration=1)
                else:
                    wander_color = BLUE
                    time.sleep(1)
                    show_lines(["Player Blue:", "Make your move!"], duration=1)

                # Wenn Cursor jetzt auf einem belegten Feld, suche nächstes freies
                if locked[led_index]:
                    for offset in range(1, LEDS + 1):
                        idx = (led_index + offset) % LEDS
                        if not locked[idx]:
                            led_index = idx
                            break

                # Setze wandernden Pixel sichtbar (lösche vorher alle freien Cursors)
                for i in range(LEDS):
                    if not locked[i]:
                        pixels[i] = OFF
                if not locked[led_index]:
                    pixels[led_index] = wander_color
                pixels.write()

        last_btn = btn_val

        # Joystick lesen
        x = joystick_x.read_u16() - center

        # LINKS bewegen
        if x < -THRESHOLD:
            if not locked[led_index]:
                pixels[led_index] = OFF

            led_index = (led_index + 1) % LEDS

            if not locked[led_index]:
                pixels[led_index] = wander_color

            pixels.write()
            time.sleep(0.25)

        # RECHTS bewegen
        elif x > THRESHOLD:
            if not locked[led_index]:
                pixels[led_index] = OFF

            led_index = (led_index - 1) % LEDS

            if not locked[led_index]:
                pixels[led_index] = wander_color

            pixels.write()
            time.sleep(0.25)

        time.sleep(0.01)


# ---------------------------
# Hauptprogramm
# ---------------------------

def main():
    coin_detection()

    blue_wins = 0
    red_wins = 0

    while True:
        result = play_single_round()

        if result == BLUE:
            blue_wins += 1
            show_lines(
                ["Blue wins:", "this round!", f"Blue: {blue_wins}"],
                duration=2
            )

        elif result == RED:
            red_wins += 1
            show_lines(
                ["Red wins:", "this round!", f"Red: {red_wins}"],
                duration=2
            )

        else:
            show_lines(["It's a Tie!", "Play again!"], duration=2)
            time.sleep(0.5)
            continue

        if blue_wins == 3:
            sound_game_win()
            show_lines(["Congratulations!", "Player Blue won!"], duration=2)
            animate_champion(BLUE)
            animate_champion_pixel(BLUE)
            sound_collect_money()
            show_lines(
                ["Player Blue:", "Collect your", "money!"],
                duration=2
            )
            break

        if red_wins == 3:
            show_lines(["Congratulations!", "Player Red won!"], duration=2)
            sound_game_win()
            animate_champion(RED)
            animate_champion_pixel(RED)
            sound_collect_money()
            show_lines(
                ["Player Red:", "Collect your", "money!"],
                duration=2
            )
            break

        time.sleep(0.6)
        reset_pixels()

    sound_game_over()
    show_lines(
        ["Game Over!", "Restart the", "device to play", "again"],
        duration=3
    )
    sound_stop()


if __name__ == "__main__":
    main()
