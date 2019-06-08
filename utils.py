import omdb
import os
import dialogflow_v2 as dialogflow
import database


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "moviesbot-secret.json"

dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "moviesbot-uasafb"
API_KEY = '9c1e8a8b'
client = omdb.OMDBClient(apikey=API_KEY)


def get_new_movie(parameters):
	print(parameters)
	print('dshgddhajk')
	movie_title = parameters.get('movie_title')
	news = dict(client.get(title=movie_title, tomatoes=True))
	type1 = news['type']
	poster_url = news['poster']
	str1 = f"\n\nPlot:\n{news['plot']}\n\nThis movie has its release in {news['year']} directed by {news['director']} with actors {news['actors']} and got {news['awards']} "
	return news, type1, str1, poster_url


def get_new_series(parameters):
	print(parameters)
	series_title = parameters['series_title']
	news = client.search_series(series_title)
	type1 = news[0]['type']
	poster_url = news[0]['poster']
	str1 = f"\n\nThis series {news[0]['title']} has its release in {news[0]['year']} "
	return news, type1, str1, poster_url


def get_favorite_movie(parameters):
	characteristics = parameters['characteristics']
	favorite = database.get_favorite(characteristics)
	str1 = f"Your favorite {characteristics} is/are {favorite}!"
	type1 = 'favorite'
	news = None
	poster_url = None
	return news, type1, str1, poster_url


def detect_intent_from_text(text, session_id, language_code='en'):
	session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
	text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
	query_input = dialogflow.types.QueryInput(text=text_input)
	response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
	return response.query_result


def fetch_reply(msg, session_id):
	response = detect_intent_from_text(msg, session_id)
	if response.intent.display_name == 'movie':
		return get_new_movie(dict(response.parameters))

	elif response.intent.display_name == 'series':
		return get_new_series(response.parameters)

	elif response.intent.display_name == 'favorite':
		return get_favorite(response.parameters)

	else:
		return response.fulfillment_text
