#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

const int trigPin = 8;
const int echoPin = 9;
const int seuil = 25;

unsigned long lastDetection = 0;
const unsigned long debounceDelay = 2000;

String currentLine = "";
int scrollIndex = 0;
unsigned long lastScrollTime = 0;
const unsigned long scrollInterval = 300;

void setup() {
  lcd.init();
  lcd.backlight();
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  lcd.setCursor(0, 0);
  lcd.print("Pret !");
}

void loop() {
  // --- 1. Capteur actif tout le temps
  if (objetDetecte()) {
    if (millis() - lastDetection > debounceDelay) {
      Serial.println("next");
      lastDetection = millis();
      currentLine = ""; // Annule l'affichage en cours
    }
  }

  // --- 2. Réception message depuis le PC
  if (Serial.available()) {
    currentLine = Serial.readStringUntil('\n');
    scrollIndex = 0;
    lastScrollTime = millis();
    lcd.clear();
  }

  // --- 3. Affichage scrollable non-bloquant
  if (currentLine.length() <= 16) {
    lcd.setCursor(0, 0);
    lcd.print(currentLine);
  } else {
    if (millis() - lastScrollTime >= scrollInterval) {
      lcd.setCursor(0, 0);
      lcd.print(currentLine.substring(scrollIndex, scrollIndex + 16));
      scrollIndex++;
      if (scrollIndex > currentLine.length() - 16) scrollIndex = 0;
      lastScrollTime = millis();
    }
  }
}

// --- Détection ultrason
bool objetDetecte() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duree = pulseIn(echoPin, HIGH, 30000);
  float distance = duree * 0.034 / 2;

  return (distance > 0 && distance < seuil);
}