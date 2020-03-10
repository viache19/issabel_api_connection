import requests
import json
from python_variable import devolver_variables_globales
import numpy
       
class authenticate:
    # a function for get access token from issabel api.
    def __callauth__(self):
        dev = devolver_variables_globales()
        self.url = dev.url_vg
        self.username = dev.username_vg
        self.password = dev.password_vg

        d = {'user' : self.username, 'password' : self.password}

        response = requests.post("http://" + self.url + "/pbxapi/authenticate", data=d)
        if response.status_code == 200:

            datos_json = json.dumps(response.json())
            jsontoken_descodificar_a_string = json.loads(datos_json)
            numpy.save("temptoken.npy", jsontoken_descodificar_a_string)

        else:
            print("We had a problem with connection to the Issabel PBXAPI")

    # a funcion to make calls --> still working
    def __call__(self):
        try:
            dev = devolver_variables_globales()
            self.url = dev.url_vg
            self.username = dev.username_vg
            self.password = dev.password_vg

            token_data_load = numpy.load("temptoken.npy", allow_pickle=True)

            hed = {'Authorization': 'Bearer ' + token_data_load.item().get("access_token")}

            response = requests.get("http://"+ dev.url_vg +"/pbxapi/extensions", headers=hed)

            if response.status_code == 200:

                datos_json = json.dumps(response.json())
                extensions = json.loads(datos_json)

                if extensions["status"] == "success":

                    def jprint(parsed):
                        text = json.dumps(parsed, indent=4)
                        print(text)

                    jprint(response.json())

                elif extensions["status"] == "expired":
                    bearertokencall(autentificacion())

                else:
                    print("We had a problem with the access to Issabel PBXAPI")

            else:

                print("We had a problem with connection to the Issabel PBXAPI")
        except requests.exceptions.ConnectionError:
            print("Sorry, we have a connection error")


#SE SUPONE QUE ESTA FUNCION SE LLAMA LA PRIMERA
#authenticate().__callauth__()

authenticate().__call__()
