import falcon
import json
from .sensors import Waterlevel, Soilsensor

app = application = falcon.App()


class Resource(object):
    def on_get(self, req, resp):
        w = Waterlevel()
        soil1 = Soilsensor(1)
        soil2 = Soilsensor(2)
        
        soil1idnumber, soil1id, soil1value = soil1.readSensor()
        soil2idnumber, soil2id, soil2value = soil2.readSensor()
        response = {"waterlevel": str(w.read()), 
                    f"soilsensor {soil1id}": str(soil1value),
                    f"soilsensor {soil2id}": str(soil2value),
                    }
        
        resp.text = json.dumps(response, ensure_ascii=False)
        


app.add_route('/read', Resource())