import pandas as pd
import json
import requests
from flask import Flask, request, Response  # flask é o pacote, Flask é a classe

# constants
TOKEN='5457388815:AAEwlvy4YvcnFMq0q0AfaRiDdgVbLbbGbqM'  # será usado para se comunicar com o telegram 

# info about the bot
# https://api.telegram.org/bot5457388815:AAEwlvy4YvcnFMq0q0AfaRiDdgVbLbbGbqM/getMe #getme é um método para fornecer informação sobre o bot

# # get updates
# https://api.telegram.org/bot5457388815:AAEwlvy4YvcnFMq0q0AfaRiDdgVbLbbGbqM/getUpdates

# Local host run web hook for local tests 
# ssh -R 80:localhost:5000 localhost.run
# https://api.telegram.org/bot5457388815:AAEwlvy4YvcnFMq0q0AfaRiDdgVbLbbGbqM/setWebhook?url=https://f57917b8baf5a3.lhr.life

# # Webhook Render
# https://api.telegram.org/bot5457388815:AAEwlvy4YvcnFMq0q0AfaRiDdgVbLbbGbqM/setWebhook?url=https://rossmann-telegram-bot-ma4l.onrender.com

# # send message #interrogação depois do método é p/ sinalizar ao browser a entrada de parâmetros, & concatena os métodos
# https://api.telegram.org/bot5457388815:AAEwlvy4YvcnFMq0q0AfaRiDdgVbLbbGbqM/sendMessage?chat_id=1455983881&text=Hi Eduardo, im good    
 
 
def send_message(chat_id,text):
	url='https://api.telegram.org/bot{}/'.format(TOKEN)
	url=url+'sendMessage?chat_id={}'.format(chat_id)

	# requisição na api com o post, método de envio de dados, url é o endpoint
	r=requests.post(url,json={'text':text})  # text é o input da função send message
	print('Status Code {}'.format(r.status_code))

	return None


# o telegram vai mandar mensagem para o endpoint criado c/ flask, e aí no endpoint a mensagem será trabalhada



def load_dataset(store_id):
	# loading test dataset
	df10=pd.read_csv('test.csv') 
	df_store_raw=pd.read_csv('store.csv')
	# df10=pd.read_csv('test.csv') 
	# df_store_raw=pd.read_csv('store.csv')  


	# merge test dataset + store
	df_test=pd.merge(df10,df_store_raw,how='left',on='Store')

	# choose store for prediction               
	# df_test=df_test[df_test['Store']==22]
	df_test=df_test[df_test['Store']== store_id]

	if not df_test.empty:

		# remove closed days
		df_test=df_test[df_test['Open'] !=0]
		df_test=df_test[~df_test['Open'].isnull()] 
		df_test=df_test.drop('Id',axis=1)

		# convert dataframe to json
		data=json.dumps(df_test.to_dict(orient='records'))

	else:
		data='error'


	return data


def predict(data):

	# API Call
	url='https://rossmann-webapp-86pb.onrender.com/rossmann/predict'
	header={'Content-type':'application/json'}
	data=data	
	
	r=requests.post(url,data=data,headers=header)
	
	print('Status Code {}'.format(r.status_code))

	d1=pd.DataFrame(r.json(),columns=r.json()[0].keys())  # d1=df com coluna de predição

	return d1



def parse_message(message):
	chat_id = message['message']['chat']['id']            #entra dentro do json
	store_id=message['message']['text']

	store_id=store_id.replace('/','')

	try:
		store_id = int(store_id)

	except ValueError:
		# send_message(chat_id,'Store ID is wrong')   ñ pode ser usado aqui pq na função n tem o store_id
		store_id='error'

	return chat_id,store_id


# API initialize
app=Flask(__name__)   # instanciar o flask  
 
#  criar a rota/endpoint, pra onde a mensagem vai chegar
@app.route('/',methods=['GET','POST'])	# @app.route é um decorador, / = endpoint na raiz, get e post métodos permitidos nesse endpoint
def index(): # essa função vai rodar toda vez que o endpoint / 'root' for acionado passando um dado
	if request.method =='POST':   # se sim recebeu uma mensagem
		message=request.get_json()

		chat_id,store_id=parse_message(message)

		if store_id != 'error':
			# loading data
			data=load_dataset(store_id)
					
			if data != 'error':

				# prediction                               # tarefas q serão realisadas
				d1=predict(data)
				
				# calculation
				d2=d1[['store','prediction']].groupby('store').sum().reset_index()
				
				# send message
				msg='Store number {} will sell R${:,.2f} in the next 6 weeks'.format(
				           d2['store'].values[0],
				           d2['prediction'].values[0])
				
				send_message(chat_id, msg)
				return Response('Ok',status=200)
				
			else:
				send_message(chat_id,'Store not available')
				return Response('Ok',status=200)

		else:
			send_message(chat_id,'Store ID is wrong')
			return Response('Ok',status=200)      # sem a mensagem de status 200 a api fica rodando indefinidamente

	else:  # se for um get
		return '<h1> Rossmann Telegram BOT </h1>' # cabeçalho de html no caso do usuário ñ passar dado/ñ acessar o endpoint



if __name__ == '__main__':	
	app.run(host='0.0.0.0',port=5000)  # método run, rodar o app no host, 5000  porta padrão do flask (deploy local)

