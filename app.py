import requests
from flask import Flask, request, render_template
import json

app=Flask(__name__)

@app.route('/')
def index():
	with open('data.json','r') as f:
		data=json.load(f)
	if data['recent']!='':
		return render_template('index.html', preset=data['recent'])	
	return render_template('index.html')

@app.route('/',methods=['POST'])
def submit():
	if request.form.get('form_name')=='form-1':
		town=request.form.get('town')
		with open('data.json','r') as file:
			json_data=json.load(file)
		json_data['recent']=town
		if town not in json_data['visited']:
			json_data['visited'].update({town: 1})
		else:
			val=json_data['visited'].get(town)
			json_data['visited'][town]=val+1
		with open('data.json', 'w') as file:
			json.dump(json_data, file)
		api=requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={town}').json()
		longitude=api['results'][0]['longitude']
		latitude=api['results'][0]['latitude']
		req=requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true')
		data=req.json()
		description={
			0: 'Ясно', 1: 'Переменная облачность', 2: 'Переменная облачность', 3: 'Переменная облачность', 45: 'Туман', 48: 'Туман',
			61: 'Дождь', 63: 'Дождь', 65: 'Дождь', 95: 'Гроза', 96: 'Гроза', 99: 'Гроза', 51: 'Изморось', 53: 'Изморось', 55: 'Изморось'
		}
		return render_template(
			'index.html',
			temperature=data['current_weather']['temperature'], temp_unit=data['current_weather_units']['temperature'],
			windspeed=data['current_weather']['windspeed'], wind_unit=data['current_weather_units']['windspeed'], preset=town,
			description=description.get(data['current_weather']['weathercode'],'Другое')
		)
	else:
		with open('data.json','r') as file:
			records=(json.load(file))['visited']
		return render_template(	'history.html', history=records )

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int('5000'), debug=True)
