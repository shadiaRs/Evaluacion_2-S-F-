import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
idioma = "es"
key = "0bdadd40-db41-4d41-a227-19fb30eb2528"

#localizacion
def geocoding(location, key):
    while location == "":
        location = input("Por favor, ingrese la ubicación nuevamente: ")
    
    if location.lower() in ["s", "salir", "quit", "q"]:
        return None, None, None, location

    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key, "locale": idioma})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    if json_status == 200 and len(json_data.get("hits", [])) > 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0].get("osm_value", "")
        
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        
        if len(state) != 0 and len(country) != 0:
            new_loc = f"{name}, {state}, {country}"
        elif len(country) != 0:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name
        
        print(f"\nURL Geocoding para {new_loc} (Tipo: {value}):\n{url}")
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        print(f"No se encontró la ubicación: {location}")
        
    return json_status, lat, lng, new_loc

while True:
    print("\n" + "="*50)
    loc1 = input("Ingrese Ubicación de Origen (o 's' / 'salir' para finalizar): ")
    if loc1.lower() in ["s", "salir", "quit", "q"]:
        print("Saliendo del programa...")
        break
        
    orig = geocoding(loc1, key)
    if orig[3].lower() in ["s", "salir", "quit", "q"]:
        print("Saliendo del programa...")
        break

    loc2 = input("Ingrese Ubicación de Destino (o 's' / 'salir' para finalizar): ")
    if loc2.lower() in ["s", "salir", "quit", "q"]:
        print("Saliendo del programa...")
        break
        
    dest = geocoding(loc2, key)
    if dest[3].lower() in ["s", "salir", "quit", "q"]:
        print("Saliendo del programa...")
        break
    
    print("="*50)
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "locale": idioma}) + op + dp
        
        paths_request = requests.get(paths_url)
        paths_status = paths_request.status_code
        paths_data = paths_request.json()
        
        print(f"Estado de la API de Enrutamiento: {paths_status}")
        print(f"URL de Enrutamiento:\n{paths_url}")

        print("="*50)
        print(f"Instrucciones de viaje desde '{orig[3]}' hasta '{dest[3]}':")
        print("="*50)
        
        if paths_status == 200:
            distancia_m = paths_data["paths"][0]["distance"]
            tiempo_ms = paths_data["paths"][0]["time"]
            
            miles = (distancia_m) / 1000 / 1.609
            km = (distancia_m) / 1000
            
            sec = int(tiempo_ms / 1000 % 60)
            min = int(tiempo_ms / 1000 / 60 % 60)
            hr = int(tiempo_ms / 1000 / 60 / 60)
            
            print(f"Distancia Recorrida: {miles:.2f} millas / {km:.2f} km")
            print(f"Duración del Viaje: {hr:02d}:{min:02d}:{sec:02d}")
            print("="*50)
            print("Narrativa del viaje (Paso a paso):")
            
            instrucciones = paths_data["paths"][0]["instructions"]
            for i, paso in enumerate(instrucciones, start=1):
                texto = paso["text"]
                dist_paso_km = paso["distance"] / 1000
                dist_paso_miles = dist_paso_km / 1.609
                print(f"{i}. {texto} ({dist_paso_km:.2f} km / {dist_paso_miles:.2f} millas)")
            print("="*50)