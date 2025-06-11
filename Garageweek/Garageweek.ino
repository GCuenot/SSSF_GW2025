#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); // Change à 0x3F si nécessaire

// Capteur ultrason
const int trigPin = 8;
const int echoPin = 9;
const int seuil = 25; // cm

// Messages à faire défiler
String messages[] = {
  "Haron",
  "Khalis",
  "Chaimae",
  "Guillaume",
  "Clement",
  "Choisir votre recette !"
};
int totalMessages = sizeof(messages) / sizeof(messages[0]);
int index = 0;

void setup() {
  lcd.init();
  lcd.backlight();
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  bool changementDemande = afficherMessage(messages[index]);

  // Si détection pendant l'affichage → passer au message suivant
  if (changementDemande) {
    index = (index + 1) % totalMessages;
    delay(1000); // Anti-rebond
  }
}

// Affiche le message avec défilement, retourne true si détection pendant le scroll
bool afficherMessage(String msg) {
  int len = msg.length();

  if (len <= 16) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(msg);
    delay(300); // petit délai
    return objetDetecte(); // Retourne vrai si détection
  } else {
    for (int i = 0; i <= len - 16; i++) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(msg.substring(i, i + 16));
      delay(300);

      // Si objet détecté pendant le scroll → sortir
      if (objetDetecte()) {
        return true;
      }
    }
    delay(500);
    return false;
  }
}

// Fonction de détection (HC-SR04)
bool objetDetecte() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duree = pulseIn(echoPin, HIGH, 30000); // Timeout sécurité
  float distance = duree * 0.034 / 2;

  return (distance > 0 && distance < seuil);
}
