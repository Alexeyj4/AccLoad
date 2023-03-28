#define numOfSlots 1
#define array_len 20 //array length for measure filter
#define valid_threshold 230 //not valid measure filter value
const int Upin[]={14,16,18,14,16,18,14,16};
const int Ipin[]={15,17,19,15,17,19,15,17};

int Umeas;
int Imeas;
int u[numOfSlots][array_len];
int i[numOfSlots][array_len];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  for(int s=0;s<numOfSlots;s++)  
  {
    pinMode(Upin[s],INPUT);
    pinMode(Ipin[s],INPUT);
  }

analogReference(INTERNAL);
}


float toVolts(int s) //count average and converting
{ 
  float sum=0;
  for(int a=0;a<array_len;a++){
    sum+=u[s][a];
  }
  return sum/array_len/32.7;
}

float toAmperes(int s) //count average and converting
{
  float sum=0;
  for(int a=0;a<array_len;a++){
    sum+=i[s][a];
  }
  return sum/array_len/229.1;
}

int valid(int s){  //s=slot number 
  int umin=1024;
  int umax=0;
  int imin=1024;
  int imax=0;
  for(int a=0;a<array_len;a++){
    if(umin>u[s][a])umin=u[s][a];
    if(umax<u[s][a])umax=u[s][a];
    if(imin>i[s][a])imin=i[s][a];
    if(imax<i[s][a])imax=i[s][a];
  }
  if((umax-umin)>valid_threshold)return 0;
  if((imax-imin)>valid_threshold)return 0;
  return 1;
}

void loop() {
  // put your main code here, to run repeatedly:
    
  for(int a=0;a<array_len;a++){
    for(int s=0;s<numOfSlots;s++){
      u[s][a]=analogRead(Upin[s]);
      i[s][a]=analogRead(Ipin[s]);      
    }
  }
   for(int s=0;s<numOfSlots;s++){
      if(valid(s)==1){
        Serial.println("slot");
        Serial.println(s);
        Serial.println(toVolts(s));
        Serial.println(toAmperes(s));       
      }      
   }
 
  delay(100);
}
