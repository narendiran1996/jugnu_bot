class my_servo
{
  Servo s;
  int cang;
  public:
  
  my_servo()
  {
    cang=0;
   }
  my_servo(int pno)
  {
    cang=0;
    att(pno);
   }
  
   void att(int pno)
   {
    s.attach(pno);
   }
   void dett()
   {
    s.detach();
   }
  void servo_write(int ang)
  {
    cang=ang;
    s.write(ang);
  }
  int get_cang()
  {
    return cang;
  }
  void move_in_steps(int ang,int delay_=10)
  {
    if(ang>=cang)
    {
      for(int i=cang;i<=ang;i++)
      {
        s.write(i);
        delay(delay_);
      }
      cang=ang;
    }
    else if(ang<cang)
    {
      for(int i=cang;i>=ang;i--)
      {
        s.write(i);
        delay(delay_);
      }
      cang=ang;
    }
  }
  
};

