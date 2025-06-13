#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); // Change à 0x3F si nécessaire

// Capteur ultrason
const int trigPin = 8;
const int echoPin = 9;
const int seuil = 25; // cm

// Messages à afficher
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

// Buffer de réception série
String commande = "";

void setup() {
  lcd.init();
  lcd.backlight();
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  bool changementDemande = afficherMessage(messages[index]);

  if (changementDemande) {
    index = (index + 1) % totalMessages;
    delay(1000); // Anti-rebond
  }

  verifierCommandeSerie();
}

// Affiche le message avec scroll si nécessaire
bool afficherMessage(String msg) {
  int len = msg.length();

  if (len <= 16) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(msg);
    delay(300); // court délai d'affichage
    return objetDetecte();
  } else {
    for (int i = 0; i <= len - 16; i++) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(msg.substring(i, i + 16));
      delay(300);
      if (objetDetecte()) {
        return true;
      }
    }
    delay(500);
    return false;
  }
}

// Détection de présence avec capteur HC-SR04
bool objetDetecte() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duree = pulseIn(echoPin, HIGH, 30000); // Timeout de sécurité
  float distance = duree * 0.034 / 2;

  return (distance > 0 && distance < seuil);
}

// Vérifie si une commande est reçue du PC
void verifierCommandeSerie() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      commande.trim();
      if (commande == "next") {
        index = (index + 1) % totalMessages;
        afficherMessage(messages[index]);
      } else if (commande == "prev") {
        index = (index - 1 + totalMessages) % totalMessages;
        afficherMessage(messages[index]);
      }
      commande = ""; // réinitialise
    } else {
      commande += c;
    }
  }
}
