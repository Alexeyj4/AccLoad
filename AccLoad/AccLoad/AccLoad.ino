int numOfSlots=3;
const int Upin[]={14,16,18};
const int Ipin[]={15,17,19};


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  for(int i=0;i<numOfSlots;i++)  
  {
    pinMode(Upin[i],INPUT);
    pinMode(Ipin[i],INPUT);
  }

analogReference(INTERNAL);
}


float toVolts(int Umeas)
{
  return Umeas/32.7;
}

float toAmperes(int Imeas)
{
  return Imeas/229.1;
}

void loop() {
  // put your main code here, to run repeatedly:
  for(int i=0;i<numOfSlots;i++)
  {
    int Umeas=analogRead(Upin[i]);
    int Imeas=analogRead(Ipin[i]);
    Serial.println("slot");
    Serial.println(i);
    Serial.println(toVolts(Umeas));
    Serial.println(toAmperes(Imeas));
  }
  delay(50);
}
