//-------------------------------------------------------------------------------------------
//-    Pin definitions DO NOT CHANGE!!!!!                                                   -
//-------------------------------------------------------------------------------------------
int F1 = 6;
int F2 = 8;
int R1 = 7;
int R2 = 9;
int PWM1 = 3;
int PWM2 = 11;
//-------------------------------------------------------------------------------------------
bool F1Var, F2Var, R1Var, R2Var;
int PWM1Var, PWM2Var, mode, accl = 3;
char serialbuffer[3];
String readString;
char receivebuffer[15];
unsigned long savedtime;
unsigned long savedtime2;
bool timeout = true;
int motorslipcompensation = 0;


void setup() {
  Serial.begin(115200);
  Serial.println("Thumper motor controller V1.00");
  //-----------------------------------------------------------------------------------------
  //- Set PWM frequency to 1KHz for less audiodible noise                                   -
  //                                                                                        -
  //TCCR2B = TCCR2B & B11111000 | B00000001 divisor 1 for PWM frequency of 31372.55 Hz      -
  //TCCR2B = TCCR2B & B11111000 | B00000010 divisor 8 for PWM frequency of 3921.16 Hz       -
  //TCCR2B = TCCR2B & B11111000 | B00000011 divisor 32 for PWM frequency of 980.39 Hz       -
  //TCCR2B = TCCR2B & B11111000 | B00000100 divisor 64 for PWM frequency of 490.20 Hz       -
  //TCCR2B = TCCR2B & B11111000 | B00000101 divisor 128 for PWM frequency of 245.10 Hz      -
  //TCCR2B = TCCR2B & B11111000 | B00000110 divisor 256 for PWM frequency of 122.55 Hz      -
  //TCCR2B = TCCR2B & B11111000 | B00000111 divisor 1024 for PWM frequency of 30.64 Hz      -
  //-----------------------------------------------------------------------------------------
  TCCR2B = TCCR2B & B11111000 | B00000011;
  //-----------------------------------------------------------------------------------------
  //-   Init pin definitions DO NOT CHANGE!!!                                               -
  //-----------------------------------------------------------------------------------------
  pinMode(F1, OUTPUT);
  pinMode(F2, OUTPUT);
  pinMode(R1, OUTPUT);
  pinMode(R2, OUTPUT);
  pinMode(PWM1, OUTPUT);
  pinMode(PWM2, OUTPUT);
  //-----------------------------------------------------------------------------------------
  //-   Safe reset state                                                                    -
  //-----------------------------------------------------------------------------------------
  digitalWrite(F1, LOW);
  digitalWrite(F2, LOW);
  digitalWrite(R1, LOW);
  digitalWrite(R2, LOW);
  analogWrite(PWM1, 0);
  analogWrite(PWM2, 0);
  F1Var = false;
  F2Var = false;
  R1Var = false;
  R2Var = false;
  PWM1Var = 0;
  PWM2Var = 0;
  writeMotorVab();


  //------------------------------------------------------------------------------------------
}


void loop() {
  if (timeout) {
    unsigned long currenttime = millis();
    if ((currenttime - savedtime) > 1000 && (currenttime - savedtime) < 1500) {
      if (PWM1Var > 100) {
        setPWM(1, PWM1Var / 2);
      }
      else {
        setPWM(1, 0);
      }
      if (PWM2Var > 100) {
        setPWM(2, PWM2Var / 2);
      }
      else {
        setPWM(2, 0);
      }
      savedtime = savedtime - 500;
    }
    else if ((currenttime - savedtime) > 2000 && (currenttime - savedtime) < 2500) {
      setPWM12(0);
      savedtime = savedtime - 500;
    }
  }

  /*
    writeForward12();
    for(int i =0; i < 256; i++) {
    setPWM12(i);
    delay(2);
    }
  */
  if (Serial.available()) {
    savedtime2 = millis();
    int command = 0;
    int word1 = 0;
    int word2 = 0;
    readString = Serial.readStringUntil('\n');
    char received_buffer[40];
    readString.toCharArray(received_buffer, 40);
    char *p = received_buffer;
    char *str;
    command = atoi(strtok_r(p, ":", &p));
    word1 = atoi(strtok_r(p, ":", &p));
    word2 = atoi(strtok_r(p, ":", &p));
    Serial.print("Command: ");
    Serial.println(command);
    
    //-----------------------------------------------------------------------------------------
    //- Basic stop command, the controller use Coasting braking to stop the motors            -
    //-----------------------------------------------------------------------------------------
    if (command == 0x00) {
      /*method for electric brake
        setPWM12(0);
        digitalWrite(F1, HIGH);
        digitalWrite(F2, HIGH);
        digitalWrite(R1, HIGH);
        digitalWrite(R2, HIGH);
        F1Var = false;
        F2Var = false;
        R1Var = false;
        R2Var = false;
        Serial.println("Method stop");
        writeMotorVab();
      */
      stopMotor();
      setPWM12(0);

    }
    
    //-----------------------------------------------------------------------------------------
    //- Forward command, the controller set both off the motors forward with the choosen speed-
    //-----------------------------------------------------------------------------------------
    else if (command  == 0x01)
    {
      Serial.print("Set both moters forward with speed off ");
      Serial.println(word1);
      if (word1 > 0 && word1 <= 255) {
        writeForward12();
        setPWM12(word1);
      }
      savedtime = millis();
    }
    
    //-----------------------------------------------------------------------------------------
    //- Backward command, the controller set the motors backward with the choosen speed       -
    //-----------------------------------------------------------------------------------------
    else if (command == 0x02) {
      Serial.print("Set both moters reverse with speed off ");
      Serial.println(word1);
      if (word1 > 0 && word1 <= 255) {
        writeReverse12();
        setPWM12(word1);
      }
      savedtime = millis();
    }

    //-----------------------------------------------------------------------------------------
    //-Right drive command,the controller set the motors to drive right with the choosen speed-
    //-----------------------------------------------------------------------------------------
    else if (command == 0x03) {
    
      Serial.print("Drive with speed off ");
      Serial.println(word1);
      if (mode != 2) {
        setPWM12(0);
        delay(200);
      }
      mode = 2;
      writeForward(1);
      writeReverse(2);
      if (word1 > 0 && word1 <= 255) {
        setPWM12(word1);
      }
    }

    //-----------------------------------------------------------------------------------------
    //-Left drive command, the controller set the motors to drive left with the choosen speed -
    //-----------------------------------------------------------------------------------------
    else if (command == 0x04) {
      if (mode != 3) {
        setPWM12(0);
        delay(200);
      }
      mode = 3;
      writeForward(2);
      writeReverse(1);
      if (word1 > 0 && word1 <= 255) {
        setPWM12(word1);
      }
    }

    //-----------------------------------------------------------------------------------------
    //- Acceleration command, the controller set the acceleration off the 0x01,0x02,0x03,0x04 -
    //- commands.                                                                             -
    //-----------------------------------------------------------------------------------------
    else if (command == 0x05) {
      if (word1 >= 0 && word1 <= 20) {
        Serial.print("Changing acceleration to ");
        Serial.println(word1);
        accl = word1;
      }
    }
    
    //-----------------------------------------------------------------------------------------
    //- Timeout command, control the 1s timeout                                     -
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

    //-----------------------------------------------------------------------------------------
    //- Left drive command, the controller set the motors to drive left with the choosen speed-
    //-----------------------------------------------------------------------------------------
    else if (command == 0x07) {
      mode = 4;
      if (word2 >= 0 && word2 <= 255) {
        setPWM(1, abs(word2));
      }
      if (word1 == 0) {
        writeForward(1);
      }
      else if (word1 == 1) {
        writeReverse(1);
      }
    }

    else if (command == 0x08) {
      mode = 5;
      if (word2 >= 0 && word2 <= 255) {
        setPWM(2, abs(word2));
      }
      if (word1 == 0) {
        writeForward(2);
      }
      else if (word1 == 1) {
        writeReverse(2);
      }
    }

    else if (command == 0x09) {
      mode = 6;
      if (abs(word1) <= 255) {
        setPWM(1, abs(word2));
      }
      if (word1 >= 0) {
        writeForward(1);
      }
      else if (word1 < 0) {
        writeReverse(1);
      }
    }

    else if (command == 0x0A) {
      mode = 7;
      if (abs(word1) <= 255) {
        setPWM(2, abs(word2));
      }
      if (word1 >= 0) {
        writeForward(2);
      }
      else if (word1 < 0) {
        writeReverse(2);
      }
    }

    else if (command == 0x0B) {
      if (word1 < 15 && word1 >= -15) {
        motorslipcompensation = word1;
        Serial.print("Set yaw compensation to ");
        Serial.println(motorslipcompensation);
      }
    }

    //-----------------------------------------------------------------------------------------
    //- Emergy stop command, the controller use Dynamic braking to stop the motors            -
    //-----------------------------------------------------------------------------------------
    else if (command == 0x0C) {
      setPWM12(0);
      digitalWrite(F1, HIGH);
      digitalWrite(F2, HIGH);
      digitalWrite(R1, HIGH);
      digitalWrite(R2, HIGH);
      F1Var = true;
      F2Var = true;
      R1Var = true;
      R2Var = true;
      Serial.println("Method emergy stop");
      delay(100);
      digitalWrite(F1, LOW);
      digitalWrite(F2, LOW);
      digitalWrite(R1, LOW);
      digitalWrite(R2, LOW);
      F1Var = false;
      F2Var = false;
      R1Var = false;
      R2Var = false;
      writeMotorVab();
    }

    //-----------------------------------------------------------------------------------------
    //- Unsafe Emergy stop command, the controller use Dynamic braking to stop the motors     -
    //-----------------------------------------------------------------------------------------
    else if (command == 0x0D) {
      setPWM12(0);
      digitalWrite(F1, HIGH);
      digitalWrite(F2, HIGH);
      digitalWrite(R1, HIGH);
      digitalWrite(R2, HIGH);
      F1Var = true;
      F2Var = true;
      R1Var = true;
      R2Var = true;
      Serial.println("Method unsafe emergy stop");
    }



    savedtime = millis();
  }

  readString = "";
}




//methods
bool writeForward12(void) {
  if (mode != 0) {
    setPWM12(0);
    delay(200);
  }
  mode = 0;
  writeForward(1);
  writeForward(2);
}

bool writeReverse12(void) {
  if (mode != 1) {
    setPWM12(0);
    delay(200);
  }
  mode = 1;
  writeReverse(1);
  writeReverse(2);
}

bool setPWM12(int level) {
  if (level > PWM1Var) {
    int startvalue = 50;
    if (PWM1Var > 50) {
      startvalue = PWM1Var;
    }
    int temp = 0;
    for (int i = startvalue; i < level; i++) {
      temp = temp + 1;
      if (temp > accl) {
        temp = 0;
        setPWM(1, i);
        setPWM(2, i);
        delay(1);
      }
    }
    setPWM(1, level - motorslipcompensation);
    setPWM(2, level);
  }
  else {
    setPWM(1, level - motorslipcompensation);
    setPWM(2, level);
  }
}

bool writeForward(uint8_t channel) {
  if (channel == 1) {
    digitalWrite(R1, LOW);
    digitalWrite(F1, HIGH);
    R1Var = false;
    F1Var = true;
  }
  else if (channel == 2) {
    digitalWrite(R2, LOW);
    digitalWrite(F2, HIGH);
    R2Var = false;
    F2Var = true;
  }
  else {
    digitalWrite(F1, LOW);
    digitalWrite(F2, LOW);
    digitalWrite(R1, LOW);
    digitalWrite(R2, LOW);
    F1Var = false;
    F2Var = false;
    R1Var = false;
    R2Var = false;
  }
  Serial.println("Method writeForward");
  writeMotorVab();
}

bool writeReverse(uint8_t channel) {
  if (channel == 1) {
    digitalWrite(F1, LOW);
    digitalWrite(R1, HIGH);
    F1Var = false;
    R1Var = true;
  }
  else if (channel == 2) {
    digitalWrite(F2, LOW);
    digitalWrite(R2, HIGH);
    F2Var = false;
    R2Var = true;
  }
  else {
    digitalWrite(F1, LOW);
    digitalWrite(F2, LOW);
    digitalWrite(R1, LOW);
    digitalWrite(R2, LOW);
    F1Var = false;
    F2Var = false;
    R1Var = false;
    R2Var = false;
  }
  Serial.println("Method writeReverse");
  writeMotorVab();
}

bool stopMotor(void) {
  digitalWrite(F1, LOW);
  digitalWrite(F2, LOW);
  digitalWrite(R1, LOW);
  digitalWrite(R2, LOW);
  F1Var = false;
  F2Var = false;
  R1Var = false;
  R2Var = false;
  Serial.println("Method stop");
  writeMotorVab();
}

bool setPWM(uint8_t channel, int level) {
  if (level < 0) level = 0;
  if (channel == 1) {
    analogWrite(PWM1, level);
    PWM1Var = level;
  }
  else if (channel == 2) {
    analogWrite(PWM2, level);
    PWM2Var = level;
  }
  else {
    analogWrite(PWM1, 0);
    analogWrite(PWM2, 0);
    PWM1Var = 0;
    PWM2Var = 0;
  }
  Serial.println("Method setPWM:");
  writeMotorVab();
}

void setPwmFrequency(int pin, int divisor) {
  byte mode;
  if (pin == 5 || pin == 6 || pin == 9 || pin == 10) {
    switch (divisor) {
      case 1:
        mode = 0x01;
        break;
      case 8:
        mode = 0x02;
        break;
      case 64:
        mode = 0x03;
        break;
      case 256:
        mode = 0x04;
        break;
      case 1024:
        mode = 0x05;
        break;
      default:
        return;
    }
    if (pin == 5 || pin == 6) {
      TCCR0B = TCCR0B & 0b11111000 | mode;
    }
    else {
      TCCR1B = TCCR1B & 0b11111000 | mode;
    }
  }
  else if (pin == 3 || pin == 11) {
    switch (divisor) {
      case 1:
        mode = 0x01;
        break;
      case 8:
        mode = 0x02;
        break;
      case 32:
        mode = 0x03;
        break;
      case 64:
        mode = 0x04;
        break;
      case 128:
        mode = 0x05;
        break;
      case 256:
        mode = 0x06;
        break;
      case 1024:
        mode = 0x07;
        break;
      default:
        return;
    }
    TCCR2B = TCCR2B & 0b11111000 | mode;
    TCCR2B = TCCR2B & B11111000 | B00000011;
  }
}

void writeMotorVab(void) {
  Serial.print("F1=");
  Serial.print(F1Var);
  Serial.print(" F2=");
  Serial.print(F2Var);
  Serial.print(" R1=");
  Serial.print(R1Var);
  Serial.print(" R2=");
  Serial.print(R2Var);
  Serial.print(" PWM1=");
  Serial.print(PWM1Var);
  Serial.print(" PWM2=");
  Serial.println(PWM2Var);
}
