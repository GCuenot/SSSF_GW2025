#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

String currentText = "";
unsigned long lastScrollTime = 0;
int scrollPos = 0;

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.print("Pret");
}

void loop() {
  // Lecture série
  if (Serial.available()) {
    String ligne = Serial.readStringUntil('\n');
    ligne.trim();

    // Si format "Etape X/Y: texte"
    if (ligne.startsWith("Etape")) {
      currentText = ligne;
      scrollPos = 0;
      lastScrollTime = millis();
      afficherEtape();
    }
  }

  // Scroll automatique si texte long
  if (currentText.length() > 24 && millis() - lastScrollTime > 700) {
    scrollPos++;
    if (scrollPos > currentText.length() - 24) scrollPos = 0;
    afficherEtape();
    lastScrollTime = millis();
  }
}

void afficherEtape() {
  lcd.clear();

  // Première ligne : "Etape X/Y"
  int sepIndex = currentText.indexOf(':');
  String titre = (sepIndex != -1) ? currentText.substring(0, sepIndex) : "Etape ?";
  lcd.setCursor(0, 0);
  lcd.print(titre.substring(0, 16));

  // Deuxième ligne : texte défilant
  String corps = (sepIndex != -1) ? currentText.substring(sepIndex + 1) : "";
  corps.trim();

  String toDisplay = "                " + corps + "                ";
  lcd.setCursor(0, 1);
  lcd.print(toDisplay.substring(scrollPos, scrollPos + 16));
}
