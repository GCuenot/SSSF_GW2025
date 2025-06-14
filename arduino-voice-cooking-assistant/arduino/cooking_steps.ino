#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); // Change to 0x3F if necessary

// Cooking steps
String cookingSteps[] = {
  "Step 1: Gather ingredients",
  "Step 2: Preheat oven",
  "Step 3: Mix ingredients",
  "Step 4: Bake for 30 minutes",
  "Step 5: Let cool before serving"
};
int totalSteps = sizeof(cookingSteps) / sizeof(cookingSteps[0]);
int currentStep = 0;

// Buffer for serial command
String command = "";

void setup() {
  lcd.init();
  lcd.backlight();
  Serial.begin(9600);
}

void loop() {
  displayStep(cookingSteps[currentStep]);
  checkSerialCommand();
}

// Display the current cooking step on the LCD
void displayStep(String step) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(step);
  delay(2000); // Display for 2 seconds
}

// Check for commands from the Raspberry Pi
void checkSerialCommand() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      command.trim();
      if (command == "next") {
        currentStep = (currentStep + 1) % totalSteps;
        displayStep(cookingSteps[currentStep]);
      } else if (command == "prev") {
        currentStep = (currentStep - 1 + totalSteps) % totalSteps;
        displayStep(cookingSteps[currentStep]);
      }
      command = ""; // Reset command
    } else {
      command += c;
    }
  }
}