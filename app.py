from flask import Flask, request, jsonify
import requests 
import json

app = Flask(__name__)



def update(path, data, url, tock = ""):
    #database_url = "https://motorwaymavericks-23929-default-rtdb.firebaseio.com/"
    url = f"{url}{path}.json"

    # Add authentication token (if required)
    headers = {}
    # if auth_token:
    headers["Authorization"] = f"Bearer {tock}"

    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Data updated successfully!")
        return "Data updated successfully!"
    else:
        print(f"Failed to update data. Status code: {response.status_code}")
        return f"Failed to update data. Status code: {response.status_code}"

def getapi():
    database_url = "https://motorwaymavericks-23929-default-rtdb.firebaseio.com/"
    url = f"{database_url}APIKEYS/.json"
    res = requests.get(url).text
    json_data = json.loads(res)
    return json_data
     
def getdata(path):
    try:
        database_url = "https://motorwaymavericks-23929-default-rtdb.firebaseio.com/"
        url = f"{database_url}{path}.json"
        res = requests.get(url).text
        if res != 'null':
            json_data = json.loads(res)
            return json_data
        else:
            return "Provided Car Id Does Not Exists!!"
    except Exception as e:
        print("some error occured!!")
        return "some error occured!!"



@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api', methods=['POST'])
def api():
    print("new client")
    if request.method == 'POST':
            try:
                json_data = request.get_json()
                print(json_data)

                id = json_data.get("key")
                
                if id == "mystery":
                    toc = json_data.get('toc')
                    path = json_data.get('path')
                    data = json_data.get('data')
                    url = json_data.get("url")

                    update(path,data, url,toc)
                    return "success"
                else:
                    print("invalid key")
                    return "invalid key"


            except Exception as e:
                return jsonify({'error': 'Invalid JSON data'}), 400

@app.route('/fetch', methods=['POST'])
def fetch():
    if request.method == 'POST':
        try:
            json_data = request.get_json()
            id = json_data.get("id")
            vec_id = json_data.get("vechicle_id")
            key = json_data.get("key")
            data_type = json_data.get("data")
            all_keys = getapi()
            print(key, all_keys[id])

            if str(key) == str(all_keys[id]):
                print("authendicated")
                if data_type == "all":
                    return getdata("/VECHICLES/")
                elif data_type == "single":
                    return getdata("/VECHICLES/"+vec_id)
            
                return "success"
            else:
                print("invalid key")
                return "invalid key"


        except Exception as e:
            return jsonify({'error': 'Invalid JSON data'}), 400

    # res = update("test",{"key":1})


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
