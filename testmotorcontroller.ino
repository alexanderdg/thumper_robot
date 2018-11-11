#include <Servo.h>

int pwm1_1 = 6;
int pwm2_1 = 5;
int en_1 = 4;

int pwm1_2 = 11;
int pwm2_2 = 3;
int en_2 = 12;
int mode = -1;
bool mode9 = false;
bool mode10 = false;
int cor1, cor2;
Servo servo1, servo2;
bool timeout = true;
unsigned long savedTime = 0;
String readString;

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(115200);
  Serial.println("Thumper motor controller V3.00");
  pinMode(pwm1_1, OUTPUT);
  pinMode(pwm2_1, OUTPUT);
  pinMode(en_1, OUTPUT);
  pinMode(pwm1_2, OUTPUT);
  pinMode(pwm2_2, OUTPUT);
  pinMode(en_2, OUTPUT);
  digitalWrite(en_1, HIGH);
  digitalWrite(en_2, HIGH);
  TCCR2B = TCCR2B & B11111000 | B00000101;
  TCCR0B = TCCR0B & B11111000 | B00000100;
  servo1.attach(9);
  servo2.attach(10);
}

void printInfo() {
  Serial.println("----------------------------------------------------");
  Serial.println("- The methods to control the motors                -");
  Serial.println("----------------------------------------------------");
  Serial.println("- 0: Basic stop command (coasting braking)         -");
  Serial.println("- 1: Forward drive command                         -");
  Serial.println("- 2: Backward drive command                        -");
  Serial.println("- 3: Right drive command                           -");
  Serial.println("- 4: Left drive command                            -");
  Serial.println("- 6: Timeout control command                       -");
  Serial.println("- 9: Right weel manual speed command               -");
  Serial.println("-10: Left weel manual speed command                -");
  Serial.println("-12: Emercy stop (dynamic braking)                 -");
  Serial.println("----------------------------------------------------");
}

int calculateReg(int level) {
  int regression = (int) ((0.0008009 * pow(level, 2)) + (-0.171963 * level) - 0.7819);
  if (regression >= 0) {
    cor2 = regression;
  }
  else {
    cor1 = -regression;
  }
  return regression;
}

// the loop function runs over and over again forever
void loop() {
  if (timeout) {
    unsigned long currenttime = millis();
    if ((currenttime - savedTime) > 300)
    {
      analogWrite(pwm1_1, 0);
      analogWrite(pwm1_2, 0);
      analogWrite(pwm2_1, 0);
      analogWrite(pwm2_2, 0);
      mode = 0;
    }
  }
  if (Serial.available()) {
    savedTime = millis();
    int command = 0;
    int word1 = 0;
    int word2 = 0;
    readString = Serial.readStringUntil('\n');
    char received_buffer[40];
    readString.toCharArray(received_buffer, 40);
    char *p = received_buffer;
    char *str;
    String received_string(received_buffer);
    if (received_string == "info") {
      printInfo();
    }
    command = atoi(strtok_r(p, ":", &p));
    word1 = atoi(strtok_r(p, ":", &p));
    word2 = atoi(strtok_r(p, ":", &p));
    Serial.print("Command: ");
    Serial.print(command);
    Serial.print(" with argument : ");
    Serial.println(word1);

    //-----------------------------------------------------------------------------------------
    //- Basic stop command, the controller use Coasting braking to stop the motors            -
    //-----------------------------------------------------------------------------------------
    if (command == 0x00) {
      mode = 0;
      Serial.println("Method stop");
      safeMode();
      analogWrite(pwm1_1, 0);
      analogWrite(pwm1_2, 0);
      analogWrite(pwm2_1, 0);
      analogWrite(pwm2_2, 0);
    }

    //-----------------------------------------------------------------------------------------
    //- Forward command, the controller set both off the motors forward with the choosen speed-
    //-----------------------------------------------------------------------------------------
    else if (command == 0x01) {
      Serial.print("Set both moters forward with speed off ");
      Serial.println(word1);
      safeMode();
      if (word1 > 110 && (mode != 1)) {
        calculateReg(word1 / 2);
        analogWrite(pwm2_1, 0);
        analogWrite(pwm2_2, 0);
        analogWrite(pwm1_1, (word1 / 2) - cor1);
        analogWrite(pwm1_2, (word1 / 2) - cor2);
        delay(100);
      }
      calculateReg(word1);
      analogWrite(pwm2_1, 0);
      analogWrite(pwm2_2, 0);
      analogWrite(pwm1_1, word1 - cor1);
      analogWrite(pwm1_2, word1 - cor2);
      mode = 1;
    }

    //-----------------------------------------------------------------------------------------
    //- Backward command, the controller set the motors backward with the choosen speed       -
    //-----------------------------------------------------------------------------------------
    else if (command == 0x02) {
      Serial.print("Set both moters reverse with speed off ");
      Serial.println(word1);
      safeMode();
      if (word1 > 110 && (mode != 2)) {
        calculateReg(word1 / 2);
        analogWrite(pwm1_1, 0);
        analogWrite(pwm1_2, 0);
        analogWrite(pwm2_1, word1 / 2);
        analogWrite(pwm2_2, word1 / 2);
        delay(100);
      }
      calculateReg(word1);
      analogWrite(pwm1_1, 0);
      analogWrite(pwm1_2, 0);
      analogWrite(pwm2_1, word1);
      analogWrite(pwm2_2, word1);
      mode = 2;
    }

    //-----------------------------------------------------------------------------------------
    //-Right drive command,the controller set the motors to drive right with the choosen speed-
    //-----------------------------------------------------------------------------------------
    else if (command == 0x03) {
      Serial.print("Right drive with speed off ");
      Serial.println(word1);
      safeMode();
      if (word1 > 110 && (mode != 3)) {
        analogWrite(pwm1_1, 0);
        analogWrite(pwm2_2, 0);
        analogWrite(pwm1_2, word1 / 2);
        analogWrite(pwm2_1, word1 / 2);
        delay(100);
      }
      analogWrite(pwm1_1, 0);
      analogWrite(pwm2_2, 0);
      analogWrite(pwm1_2, word1);
      analogWrite(pwm2_1, word1);
      mode = 3;
    }

    //-----------------------------------------------------------------------------------------
    //-Left drive command, the controller set the motors to drive left with the choosen speed -
    //-----------------------------------------------------------------------------------------
    else if (command == 0x04) {
      Serial.print("Left drive with speed off ");
      Serial.println(word1);
      safeMode();
      if (word1 > 110 && (mode != 4)) {
        analogWrite(pwm1_2, 0);
        analogWrite(pwm2_1, 0);
        analogWrite(pwm2_2, word1 / 2);
        analogWrite(pwm1_1, word1 / 2);
        delay(100);
      }
      analogWrite(pwm1_2, 0);
      analogWrite(pwm2_1, 0);
      analogWrite(pwm2_2, word1);
      analogWrite(pwm1_1, word1);
      mode = 4;
    }

    //-----------------------------------------------------------------------------------------
    //- Timeout command, control the 1s timeout                                               -
    //-----------------------------------------------------------------------------------------
    else if (command == 0x06) {
      if (word1 == 0) {
        timeout = false;
        Serial.println("Set timeout off");
      }
      else if (word1 == 1) {
        timeout = true;
        Serial.println("Set timeout on");
      }
    }

    else if (command == 0x09) {
      if (word1 < 0) {
        if (mode9 == true) {
          safeMode();
        }
        mode9 = false;
        analogWrite(pwm1_1, 0);
        analogWrite(pwm2_1, abs(word1));
      }
      else if (word1 >= 0) {
        if (mode9 == false) {
          safeMode();
        }
        mode9 = true;
        analogWrite(pwm2_1, 0);
        Serial.println(abs(word1));
        analogWrite(pwm1_1, word1);
      }
    }

    else if (command == 0x0A) {
      if (word1 < 0) {
        if (mode10 == true) {
          safeMode();;
        }
        mode10 = false;
        analogWrite(pwm1_2, 0);
        analogWrite(pwm2_2, abs(word1));
      }
      else if (word1 >= 0) {
        if (mode10 == false) {
          safeMode();
        }
        mode10 = true;
        Serial.println(abs(word1));
        analogWrite(pwm2_2, 0);
        analogWrite(pwm1_2, word1);
      }
    }
    //-----------------------------------------------------------------------------------------
    //- Emergy stop command, the controller use Dynamic braking to stop the motors            -
    //-----------------------------------------------------------------------------------------
    else if (command == 0x0C) {
      analogWrite(pwm1_1, 255);
      analogWrite(pwm1_2, 255);
      analogWrite(pwm2_1, 255);
      analogWrite(pwm2_2, 255);
      Serial.println("Method emergy stop");
      delay(50);
      analogWrite(pwm1_1, 0);
      analogWrite(pwm1_2, 0);
      analogWrite(pwm2_1, 0);
      analogWrite(pwm2_2, 0);
    }

    else if (command == 0x0E) {
      servo1.write(word1);
    }

    else if (command == 0x0F) {
      servo2.write(word1);
    }

  }
}

void safeMode(void) {
  Serial.println("Call to safe mode");
  analogWrite(pwm1_1, 0);
  analogWrite(pwm1_2, 0);
  analogWrite(pwm2_1, 0);
  analogWrite(pwm2_2, 0);
  delayMicroseconds(5);
}


