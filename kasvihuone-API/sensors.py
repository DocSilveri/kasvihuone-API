from .config import WATERLEVELSENSOR_ACTIVE, SOILSENSORS_ACTIVE, WATERLEVELSENSOR_PIN, SOILSENSOR_PINS, SOILSENSOR_IDS


class Sensor:
    value = 0
    def __init__(self):
        pass
    
    def readSensor(self):
        return "Parent class, method should be redeclared in child classes"
    
   
    
    def read(self):
        return self.readSensor()
    
class Waterlevel(Sensor):
    
    def __init__(self):
        super().__init__()
        
    def readSensor(self):
        if not WATERLEVELSENSOR_ACTIVE:
            return "Water level sensor not active."
        value = 5
        return value
    
class Soilsensor(Sensor):
    idNumber = None
    
    def __init__(self, sensorNumber):
        super().__init__()
        self.idNumber = sensorNumber
        
    def readSensor(self):
        if not SOILSENSORS_ACTIVE:
            return "Soilsensors not active."
        if self.idNumber > len(SOILSENSOR_IDS):
            return f"Sensor {self.idNumber} is not defined."
        
        value = 10
        return self.idNumber, SOILSENSOR_IDS[self.idNumber - 1], value
        
    
    
if __name__ == "__main__":
    w = Waterlevel()
    soil1 = Soilsensor(1)
    soil2 = Soilsensor(2)
    print(w.read(), soil1.read(), soil2.read())