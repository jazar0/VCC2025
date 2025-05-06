 /* PRIZM controller example program
 * Spin DC Motor Channel 1 for 5 seconds and then coast to a stop.
 * After stopping, wait for 2 seconds and then spin in opposite direction.
 * Continue to repeat until red Reset button is pressed.
 * author PWU on 08/05/2016
 */
 #include <PRIZM.h> // include the PRIZM library in the sketch
 PRIZM prizm; // instantiate a PRIZM object “prizm” so we can use its functions
 int incoming = 0;
 void setup() {
  prizm.PrizmBegin(); // initialize the PRIZM controller
  Serial.begin(9600);
 }
 void parallelSetMotorPower(int power){
  prizm.setMotorPower(2,power); // spin Motor 2 CW at power
  prizm.setMotorPower(1,-1*power); // spin Motor 1 CW at power
 }
 void loop()
 {
  /*if (prizm.readSonicSensorCM(3) < 10){
    Serial.println("Those who know");
  }*/
  //if (Serial.availableForWrite()){
  //  Serial.print(prizm.readSonicSensorCM(3));
  // Serial.println(" cm");
  //}
  Serial.println(prizm.readEncoderCount(1));
  if (abs(prizm.readEncoderDegrees(1)) >= abs(incoming)) {
    prizm.resetEncoder(1);
  }
  if (Serial.available() > 0) {
    // read the incoming byte:
    incoming = Serial.readString().toInt();
    prizm.setMotorDegree(1, 120, -1*incoming);
    Serial.println(incoming);
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