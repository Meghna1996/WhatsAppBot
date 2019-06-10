import omdb
import os
import dialogflow_v2 as dialogflow
import database
import requests
import urllib


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "moviesbot-secret.json"

dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "moviesbot-uasafb"
API_KEY = '9c1e8a8b'
client = omdb.OMDBClient(apikey=API_KEY)


def get_new_movie(parameters):
	print(parameters)
	# print('dshgddhajk')
	movie_title = parameters.get('movie_title')
	year = parameters.get('year')
	# language = parameters.get('language')
	news = dict(client.get(title=movie_title, year=year, tomatoes=True))
	if(news != {}):
		print("inside if")
		type1 = news['type']
		poster_url = news['poster']
		str1 = f"\n\nPlot:\n{news['plot']}\n\nThis {type1} has its release in " \
		f"{news['year']} directed by {news['director']} with actors {news['actors']}" \
		f" and got {news['awards']} It has a imdb rating of {news['imdb_rating']}."
		# print(type1, poster_url, str1)
		try:
			resp = urllib.request.urlopen(poster_url)
			resp.getcode()
		except urllib.error.HTTPError:
			return news,type1,str1,""
	else:
		print("inside else")
		type1 = None
		poster_url = None
		str1 = ""
	return news, type1, str1, poster_url


# def get_new_series(parameters):
# 	print(parameters)
# 	series_title = parameters['series_title']
# 	news = client.search_series(series_title)
# 	if(news != []):
# 		type1 = news[0]['type']
# 		poster_url = news[0]['poster']
# 		str1 = f"\n\nThis series {news[0]['title']} has its release "
# 		f"in {news[0]['year']} "
# 	else:
# 		type1 = None
# 		poster_url = None
# 		str1 = ""
# 	return news, type1, str1, poster_url


def get_favorite_movie(parameters):
	characteristics = parameters['characteristics']
	favorite = database.get_favorite_movie(characteristics)
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
		# print(response.parameters)
		return get_new_movie(dict(response.parameters))

	elif response.intent.display_name == 'favorite':
		return get_favorite_movie(response.parameters)

	else:
		return response.fulfillment_text
