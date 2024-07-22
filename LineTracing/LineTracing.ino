#define black 100
#define red 39
#define white 30

void setup() {
  Serial.begin(115200);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
}

int Avalue0 = 0;
int Avalue1 = 0;
int Avalue2 = 0;

int A0_color = 0;
int A1_color = 0;
int A2_color = 0;

void loop() {
  Avalue0 = analogRead(A0);
  Avalue1 = analogRead(A1);
  Avalue2 = analogRead(A2);

  // 디버그용 센서 값 출력
  Serial.print("A0 value: ");
  Serial.print(Avalue0);
  Serial.print(", A1 value: ");
  Serial.print(Avalue1);
  Serial.print(", A2 value: ");
  Serial.print(Avalue2);

  // 0 = black / 1 = red / 2 = white //
  A0_color = getColor(Avalue0);
  A1_color = getColor(Avalue1);
  A2_color = getColor(Avalue2);

  // 센서 값과 색상 정보를 시리얼 포트로 전송
  Serial.print("Colors: ");
  Serial.print(A0_color);
  Serial.print(",");
  Serial.print(A1_color);
  Serial.print(",");
  Serial.print(A2_color);
  Serial.print(",");

  delay(500);
}

int getColor(int sensorValue) {
  if (sensorValue > black) {
    return 0;
  } else if (sensorValue > red) {
    return 1;
  } else {
    return 2;
  }
}



