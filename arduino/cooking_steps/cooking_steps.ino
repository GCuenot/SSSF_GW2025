#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

// Capteur HC-SR04
const int trigPin = 8;
const int echoPin = 9;
const int seuil = 25; // cm

unsigned long lastDetection = 0;
const unsigned long debounceDelay = 500;

void setup() {
  lcd.init();
  lcd.backlight();
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  lcd.setCursor(0, 0);
  lcd.print("Pret...");
}

void loop() {
  // 1. Lire les messages du PC
  if (Serial.available()) {
    String ligne = Serial.readStringUntil('\n');
    lcd.clear();

    if (ligne.length() <= 16) {
      lcd.setCursor(0, 0);
      lcd.print(ligne);
    } else {
      // Scroll rapide sans delay bloquant
      unsigned long scrollStart = millis();
      for (int i = 0; i <= ligne.length() - 16; i++) {
        lcd.setCursor(0, 0);
        lcd.print(ligne.substring(i, i + 16));
        while (millis() - scrollStart < 200); // ≈ 200 ms entre scrolls
        scrollStart = millis();
      }
    }
  }

  // 2. Détection avec HC-SR04
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duree = pulseIn(echoPin, HIGH, 30000);
  float distance = duree * 0.034 / 2;

  if (distance > 0 && distance < seuil && millis() - lastDetection > debounceDelay) {
    Serial.println("next"); // Envoi immédiat
    lastDetection = millis();
  }
}
