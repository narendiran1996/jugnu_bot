class ultra_sonic
{
  int tp,ep;
  float duration;
  
  public:
  ultra_sonic(int epa,int tpa)
  {
    tp=tpa;
    ep=epa;
    duration=0;

    pinMode(tp,INPUT);
    pinMode(ep,OUTPUT);
  }
  void Update()
  {
    digitalWrite(ep, LOW);
    delayMicroseconds(2);
    digitalWrite(ep, HIGH);
    delayMicroseconds(5);
    digitalWrite(ep, LOW);

    duration = pulseIn(tp, HIGH);    
  }
  float get_dist_mm()
  {
    Update();
    return duration/28.0/2.0*10.0;
  }
};

