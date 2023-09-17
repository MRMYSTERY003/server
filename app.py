from flask import Flask, request, jsonify
import requests

app = Flask(__name__)



def update(path, data):
    database_url = "https://motorwaymavericks-23929-default-rtdb.firebaseio.com/"
    url = f"{database_url}{path}.json"

    # Add authentication token (if required)
    headers = {}
    # if auth_token:
    #     headers["Authorization"] = f"Bearer {auth_token}"

    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Data updated successfully!")
        return "Data updated successfully!"
    else:
        print(f"Failed to update data. Status code: {response.status_code}")
        return f"Failed to update data. Status code: {response.status_code}"



@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api', methods=['POST'])
def api():
    if request.method == 'POST':
            try:
                json_data = request.get_json()

                id = json_data.get("key")
                
                if id == "mystery":

                    path = json_data.get('path')
                    data = json_data.get('data')

                    update(path,data)
                    return "success"
                else:
                    print("invalid key")
                    return "invalid key"


            except Exception as e:
                return jsonify({'error': 'Invalid JSON data'}), 400



    # res = update("test",{"key":1})


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
