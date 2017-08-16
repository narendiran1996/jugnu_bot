
#define HMC5883L_ADDR 0x1E

bool haveHMC5883L = false;
float heading_in_degrees=0;
bool detectHMC5883L ()
{
  Wire.beginTransmission(HMC5883L_ADDR); //open communication with HMC5883
  Wire.write(10); //select Identification register A
  Wire.endTransmission();
  Wire.requestFrom(HMC5883L_ADDR, 3);
  if(3 == Wire.available()) {
    char a = Wire.read();
    char b = Wire.read();
    char c = Wire.read();
    if(a == 'H' && b == '4' && c == '3')
      return true;
  }

  return false;
}

void setup_mag()
{
  
  Wire.begin();

  TWBR = 78;  // 25 kHz 
  TWSR |= _BV (TWPS0);  // change prescaler  
bool detect = detectHMC5883L();

  if(!haveHMC5883L) 
  {
    if(detect) 
    {
      haveHMC5883L = true;
     
      
      Wire.beginTransmission(HMC5883L_ADDR); //open communication with HMC5883
      Wire.write(0x02); //select mode register
      Wire.write(0x00); //continuous measurement mode
      Wire.endTransmission();
    }
    else
    {  

      return;
    }
  }
  else
  {
    if(!detect)
    {
      haveHMC5883L = false;

      return;
    }
  }
}

void loop_mag()
{
  
  
  int x,y,z;


  Wire.beginTransmission(HMC5883L_ADDR);
  Wire.write(0x03); 
  Wire.endTransmission();


  Wire.requestFrom(HMC5883L_ADDR, 6);
  if(6<=Wire.available()){
    x = Wire.read()<<8; //X msb
    x |= Wire.read(); //X lsb
    z = Wire.read()<<8; //Z msb
    z |= Wire.read(); //Z lsb
    y = Wire.read()<<8; //Y msb
    y |= Wire.read(); //Y lsb
  }
  heading_in_degrees = 180*atan2(y,x)/PI + 180 ;


}
