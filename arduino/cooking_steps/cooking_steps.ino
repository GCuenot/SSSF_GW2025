#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); // Adresse I2C du LCD

String ligne = "";  // Pour stocker la ligne reçue

void setup() {
  lcd.init();
  lcd.backlight();
  Serial.begin(9600);
  lcd.setCursor(0, 0);
  lcd.print("Pret !");
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();

    // Fin de message
    if (c == '\n') {
      afficherMessage(ligne);
      ligne = "";
    } else {
      ligne += c;
    }
  }
}

void afficherMessage(String msg) {
  lcd.clear();
  if (msg.length() <= 16) {
    lcd.setCursor(0, 0);
    lcd.print(msg);
  } else {
    // Scrolling si trop long
    for (int i = 0; i <= msg.length() - 16; i++) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(msg.substring(i, i + 16));
      delay(300);
    }
  }
}
