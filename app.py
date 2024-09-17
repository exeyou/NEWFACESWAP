from flask import Flask, request, redirect, url_for, render_template
import requests
import time

app = Flask(__name__)

API_KEY = "cm15ia7rv0008mn03pg2jdro6"
UPLOAD_URL = "https://api.magicapi.dev/api/v1/capix/faceswap/faceswap/v1/image"
RESULT_URL = "https://api.magicapi.dev/api/v1/capix/faceswap/result/"

@app.route('/')
def upload_form():
    return render_template('upload_form.html')

@app.route('/swap', methods=['POST'])
def face_swap():
    target_url = request.form.get('target_url')
    swap_url = request.form.get('swap_url')

    if not target_url or not swap_url:
        return 'Both target_url and swap_url are required.'

    payload = f"target_url={target_url}&swap_url={swap_url}"

    headers = {
        'x-magicapi-key': API_KEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(UPLOAD_URL, data=payload, headers=headers)

    if response.status_code == 200:
        json_response = response.json()

        request_id = json_response.get('image_process_response', {}).get('request_id')

        if request_id:
            return redirect(url_for('check_result', request_id=request_id))
        else:
            return 'Failed to get request_id from the API response.'
    else:
        return f'Failed! Status Code: {response.status_code}, Response: {response.text}'

@app.route('/result/<request_id>')
def check_result(request_id):

    payload = f"request_id={request_id}"

    headers = {
        'x-magicapi-key': API_KEY,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    time.sleep(3)  # Consider using a more robust approach for waiting, like polling

    response = requests.post(RESULT_URL, data=payload, headers=headers)

    if response.status_code == 200:
        result_response = response.json()
        result_url = result_response.get('image_process_response', {}).get('result_url')

        if result_url:
            return render_template('result.html', result_url=result_url)
        else:
            return 'Failed to get result_url from the API response.'
    else:
        return f'Failed! Status Code: {response.status_code}, Response: {response.text}'

if __name__ == '__main__':
    app.run(debug=True)
