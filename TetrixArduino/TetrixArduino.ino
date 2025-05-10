 #include <PRIZM.h> // include the PRIZM library in the sketch
 PRIZM prizm; // instantiate a PRIZM object “prizm” so we can use its functions
 float incoming = 0;

 void setup() {
  prizm.PrizmBegin(); // initialize the PRIZM controller
  Serial.begin(9600);
  prizm.resetEncoder(1);

 }
 
 void loop()
 {
  Serial.println(prizm.readEncoderDegrees(1));
  /*if (abs(prizm.readEncoderDegrees(1)) >= abs(incoming)) {
    prizm.resetEncoder(1);
    incoming = 0;
  }*/
  if (Serial.available() > 0) {
    // read the incoming byte:
    incoming = Serial.readStringUntil('d').toFloat();
    //Serial.println("before");
    //prizm.setMotorDegree(1, 180, -1*incoming);
    prizm.setMotorTarget(1, 720, incoming);
    //Serial.println(incoming);
    //Serial.println(incomingByte);
    /*if (incoming == 'y'){
      parallelSetMotorPower(25);
    } else if (incoming == 'n'){
      parallelSetMotorPower(-25);
    } else if (incoming == 's'){
      parallelSetMotorPower(0);
    } else if (incoming == 't'){
      prizm.setMotorDegree(1, 90, 180);
    }*/
  }
 }