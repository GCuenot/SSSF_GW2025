#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);  // Vérifie ces pins avec ton câblage

String currentText = "";
unsigned long lastScrollTime = 0;
int scrollPos = 0;

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.print("Pret");
}

void loop() {
  // Vérifie si un nouveau message est arrivé
  if (Serial.available()) {
    currentText = Serial.readStringUntil('\n');
    currentText.trim();

    if (currentText.length() == 0) return;

    scrollPos = 0;
    lastScrollTime = millis();
    afficherEtape();
  }

  // Fait défiler le texte s'il dépasse 24 caractères
  if (currentText.length() > 24 && millis() - lastScrollTime > 700) {
    scrollPos++;
    if (scrollPos > currentText.length() - 24) scrollPos = 0;
    afficherEtape();
    lastScrollTime = millis();
  }
}

void afficherEtape() {
  lcd.clear();

  // Séparer "Etape X/Y: texte"
  int sepIndex = currentText.indexOf(':');
  String titre = (sepIndex != -1) ? currentText.substring(0, sepIndex) : "Etape ?";
  String corps = (sepIndex != -1) ? currentText.substring(sepIndex + 1) : currentText;
  corps.trim();

  // Ligne 1 = Etape X/Y
  lcd.setCursor(0, 0);
  lcd.print(titre.substring(0, 16));

  // Ligne 2 = texte défilant
  String toDisplay = "                " + corps + "                ";
  lcd.setCursor(0, 1);
  lcd.print(toDisplay.substring(scrollPos, scrollPos + 16));
}
