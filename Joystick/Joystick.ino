#include <LiquidCrystal.h>
#include <Wire.h>
#include <EEPROM.h>
#include <Filters.h>

#define PCF_address B0111000
// The different pushbuttons
#define TOPL 5
#define TOPR 4
#define MENULU 6
#define MENULD 7
#define MENURU 1
#define MENURD 0

int pushdebounce = 50;
int number1 = 0;
int number2 = 0;
int number3 = 0;
int number4 = 0;
bool laststate_menulu = false;
bool laststate_menuld = false;
bool laststate_menurd = false;
bool laststate_menuru = false;
bool password_bypass = false;

float filtercutof = 5.0;
String readString;

int cnumber1, cnumber2, cnumber3, cnumber4 = 0;

const int VRX1 = A0;
const int VRY1 = A1;
const int VRX2 = A2;
const int VRY2 = A3;
int     nJoyX;
int     nJoyY;
int     nMotMixL;
int     nMotMixR;
float fPivYLimit = 32.0;
const int cor1 = 0;
const int cor2 = 0;
const int sel = 2;
const int led = 13;
const int bl = 11;
const int sel1 = 3;
const int sel2 = 4;

unsigned long savedtime = 0;
bool toggleled = false;
bool togglebl = true;
const int rs = 5, en = 6, d4 = 7, d5 = 8, d6 = 9, d7 = 10;
uint8_t idd = 0;
uint8_t count = 0;



unsigned long lastPush = 0;

int joy2x = A2;
int joy2y = A3;

float filterVal = 0.5;       // this determines smoothness  - .0001 is max  1 is off (no smoothing)
float smoothedVal1;     // this holds the last loop value just use a unique variable for every different sensor that needs smoothing
float smoothedVal2;


FilterOnePole lowpassFilter( LOWPASS, filtercutof );
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(2);
  pinMode(sel, OUTPUT);
  pinMode(led, OUTPUT);
  pinMode(bl, OUTPUT);
  //delay(1000);
  digitalWrite(sel, HIGH);
  digitalWrite(bl, HIGH);
  lcd.begin(16, 2);
  lcd.print("Thumper remote!");
  lcd.setCursor(0, 1);
  lcd.print("Made by ALDGE!");
  delay(2000);
  lcd.clear();
  Wire.begin();
  loadPassword();
}

void loop() {
  if ((!getPushButton(TOPL) and !getPushButton(TOPR) and !getPushButton(MENURD)) or password_bypass) {
    lcd.setCursor(0, 0);
    lcd.print("Password bypass!");
    delay(1000);
    lcd.clear();
  }
  else {
    askForPassword();
  }
  digitalWrite(sel, HIGH);
  delayMicroseconds(10);
  unsigned long savedtime2 = 0;
  while (true) {
    int pot = analogRead(A7);
    filterVal = pot / 1024.0;
    readXbeedata();
    unsigned long currentTime = millis();
    if ((currentTime - savedtime) > 2000) {
      savedtime = currentTime;
      lcd.setCursor(0, 0);
      lcd.print("Bat: ");
      lcd.print(getBatteryVoltage());
      lcd.print("V ");
      lcd.print(filterVal);
      lcd.print("s");
    }
    currentTime = millis();
    if ((currentTime - savedtime2) > 10) {
      savedtime2 = currentTime;
      sendXbeedata();
    }
  }
}

float getBatteryVoltage(void) {
  int temp = analogRead(A6);
  float voltage = float((temp / 1024.0) * 5);
  return voltage;
}

void readXbeedata(void) {
  String temp = Serial.readStringUntil('&');
  if (temp != "") {
    char received_buffer[40];
    temp.toCharArray(received_buffer, 40);
    char *p = received_buffer;
    char *str;
    String received_string(received_buffer);
    float vbat = atof(strtok_r(p, ":", &p));
    float ibat = atof(strtok_r(p, ":", &p));
    int rfrating = atoi(strtok_r(p, ":", &p));
    if (count > 10) {
      lcd.setCursor(0,1);
      lcd.print("                ");
      count = 0;
    } else {
      count ++;
    }
    
    lcd.setCursor(0, 1);
    lcd.print(vbat);
    lcd.print("V");
    lcd.setCursor(6, 1);
    lcd.print(ibat);
    lcd.print("A");
    if (rfrating == 100) {
      lcd.setCursor(12, 1);
    }
    else {
      lcd.setCursor(13, 1);
    }
    lcd.print(rfrating);
    lcd.print("%");
  }
}

void sendXbeedata(void) {
  int sVRX1 = analogRead(VRX1);
  int sVRY1 = analogRead(VRY1);
  int sVRX2 = analogRead(VRX2);
  int sVRY2 = analogRead(VRY2);
  smoothedVal1 =  smooth(sVRX1, filterVal, smoothedVal1);
  smoothedVal2 =  smooth(sVRY1, filterVal, smoothedVal2);
  int output1 = (int) smoothedVal1;
  int output2 = (int) smoothedVal2;
  int crc = output1 + output2 + digitalRead(sel1) + sVRX2 + sVRY2 + digitalRead(sel2);
  Serial.print(output1);
  Serial.print(":");
  Serial.print(output2);
  Serial.print(":");
  Serial.print(digitalRead(sel1));
  Serial.print(":");
  Serial.print(sVRX2);
  Serial.print(":");
  Serial.print(sVRY2);
  Serial.print(":");
  Serial.print(digitalRead(sel2));
  Serial.print(":");
  Serial.print(idd);
  Serial.print(":");
  Serial.print(crc);
  Serial.println(":");
  idd ++ ;
}


bool askForPassword(void) {
  digitalWrite(sel, LOW);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Give password:");
  lcd.setCursor(0, 1);
  lcd.print("****");
  int digitToChange = 1;
  bool keep_looping = true;
  while (true) {
    //check the lower right menu button
    if ((getPushButton(MENURD) == false) and (laststate_menurd == false)) {
      delay(pushdebounce);
      laststate_menurd = true;
      if (getPushButton(MENURD) == false) {
        if (digitToChange >= 4) {
          if (checkPassword()) {
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("Password ok");
            delay(2000);
            goto label;
          }
          else {
            keep_looping = true;
            number1 = 0;
            number2 = 0;
            number3 = 0;
            number4 = 0;
            digitToChange = 1;
            lastPush = 0;
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("Wrong password");
            delay(5000);
            lcd.setCursor(0, 0);
            lcd.print("Give password:");
            lcd.setCursor(0, 1);
            lcd.print("****");
          }
        }
        else {
          keep_looping = true;
          lastPush = millis();
          lcd.setCursor(0, 1);
          lcd.print("****");
          digitToChange ++;
        }
      }
    }
    else if (getPushButton(MENURD) == true) {
      laststate_menurd = false;
    }
    //check the upper right menu button
    if ((getPushButton(MENURU) == false) and (laststate_menuru == false)) {
      delay(pushdebounce);
      laststate_menuru = true;
      if (getPushButton(MENURU) == false) {
        if (digitToChange <= 1) {

        }
        else {
          lastPush = millis();
          lcd.setCursor(0, 1);
          lcd.print("****");
          digitToChange --;
        }
      }
    }
    else if (getPushButton(MENURU) == true) {
      laststate_menuru = false;
    }
    changeDigit(digitToChange);
  }
label:
  lcd.clear();
}

bool checkPassword(void) {
  bool result = false;
  if ((number1 == cnumber1) and (number2 == cnumber2) and (number3 == cnumber3) and (number4 = cnumber4)) {
    result = true;
  }
  else {
    result = false;
  }
  return result;
}

void changeDigit(int digit) {
  int change = 0;
  int number = 0;
  unsigned long currenttime = millis();
  switch (digit)
  {
    case 1:
      number = number1;
      break;
    case 2:
      number = number2;
      break;
    case 3:
      number = number3;
      break;
    case 4:
      number = number4;
      break;
    default:
      number = 0;
      break;
  }

  if ((currenttime - lastPush) > 1000) {
    lcd.setCursor(0, 1);
    lcd.print("****");
  }
  else {
    lcd.setCursor(digit - 1, 1);
    lcd.print(number);
  }

  if ((getPushButton(MENULU) == false) and (laststate_menulu == false) and (number < 9)) {
    delay(pushdebounce);
    laststate_menulu = true;
    if (getPushButton(MENULU) == false) {
      lastPush = millis();
      number ++;
      lcd.setCursor(digit - 1, 1);
      lcd.print(number);
    }
  }
  else if (getPushButton(MENULU) == true) {
    laststate_menulu = false;
  }

  if ((getPushButton(MENULD) == false) and (laststate_menuld == false) and (number > 0)) {
    delay(pushdebounce);
    laststate_menuld = true;
    if (getPushButton(MENULD) == false) {
      lastPush = millis();
      number --;
      lcd.setCursor(digit - 1, 1);
      lcd.print(number);
    }
  }
  else if (getPushButton(MENULD) == true) {
    laststate_menuld = false;
  }
  switch (digit)
  {
    case 1:
      number1 = number;
      break;
    case 2:
      number2 = number;
      break;
    case 3:
      number3 = number;
      break;
    case 4:
      number4 = number;
      break;
    default:
      change = 0;
      break;
  }
}

void calculateMotors(void) {

  nJoyX = -map(analogRead(VRX1), 0, 1023, -128, 127);
  nJoyY = map(analogRead(VRY1) , 0, 1023, -128, 127);
  // TEMP VARIABLES
  float   nMotPremixL;    // Motor (left)  premixed output        (-128..+127)
  float   nMotPremixR;    // Motor (right) premixed output        (-128..+127)
  int     nPivSpeed;      // Pivot Speed                          (-128..+127)
  float   fPivScale;      // Balance scale b/w drive and pivot    (   0..1   )

  Serial.println("-----------------");
  Serial.println(cor1);
  Serial.println(cor2);
  Serial.println("-----------------");


  // Calculate Drive Turn output due to Joystick X input
  if (nJoyY >= 0) {
    // Forward
    nMotPremixL = (nJoyX >= 0) ? 127.0 : (127.0 + nJoyX);
    nMotPremixR = (nJoyX >= 0) ? (127.0 - nJoyX) : 127.0;
  } else {
    // Reverse
    nMotPremixL = (nJoyX >= 0) ? (127.0 - nJoyX) : 127.0;
    nMotPremixR = (nJoyX >= 0) ? 127.0 : (127.0 + nJoyX);
  }

  // Scale Drive output due to Joystick Y input (throttle)
  nMotPremixL = nMotPremixL * nJoyY / 128.0;
  nMotPremixR = nMotPremixR * nJoyY / 128.0;

  // Now calculate pivot amount
  // - Strength of pivot (nPivSpeed) based on Joystick X input
  // - Blending of pivot vs drive (fPivScale) based on Joystick Y input
  nPivSpeed = nJoyX;
  fPivScale = (abs(nJoyY) > fPivYLimit) ? 0.0 : (1.0 - abs(nJoyY) / fPivYLimit);

  // Calculate final mix of Drive and Pivot
  nMotMixL = (1.0 - fPivScale) * nMotPremixL + fPivScale * ( nPivSpeed);
  nMotMixR = (1.0 - fPivScale) * nMotPremixR + fPivScale * (-nPivSpeed);
  int snMotMixL = map(nMotMixL, -128, 127, -255 , 255);
  int snMotMixR = map(nMotMixR , -128, 127, -255 , 255);
  if (abs(snMotMixL) < 10) {
    snMotMixL = 0;
  }
  if (abs(snMotMixR) < 10) {
    snMotMixR = 0;
  }
  if (snMotMixL > 255) {
    snMotMixL = 255;
  }
  if (snMotMixR > 255) {
    snMotMixR = 255;
  }
  if (snMotMixL < -255) {
    snMotMixL = -255;
  }
  if (snMotMixR < -255) {
    snMotMixR = -255;
  }

  Serial.print(snMotMixL);
  Serial.print(":");
  Serial.print(snMotMixR);
  Serial.println(":");

}

bool getPushButton(int pin) {
  byte temp = 0;
  Wire.requestFrom(PCF_address, 1);
  if (Wire.available())
    temp = Wire.read();
  return bitRead(temp, pin);
}

void savePassword(String password) {
  EEPROM.write(0, (password.charAt(0)) - '0');
  delay(1);
  EEPROM.write(1, (password.charAt(1)) - '0');
  delay(1);
  EEPROM.write(2, (password.charAt(2)) - '0');
  delay(1);
  EEPROM.write(3, (password.charAt(3)) - '0');
}

void loadPassword(void) {
  cnumber1 = EEPROM.read(0);
  cnumber2 = EEPROM.read(1);
  cnumber3 = EEPROM.read(2);
  cnumber4 = EEPROM.read(3);
}

int smooth(int data, float filterVal, float smoothedVal) {


  if (filterVal > 1) {     // check to make sure param's are within range
    filterVal = .99;
  }
  else if (filterVal <= 0) {
    filterVal = 0;
  }

  smoothedVal = (data * (1 - filterVal)) + (smoothedVal  *  filterVal);

  return (int)smoothedVal;
}

