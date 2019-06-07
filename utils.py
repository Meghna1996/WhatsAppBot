import omdb, os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "moviesbot-secret.json"
import dialogflow_v2 as dialogflow


dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "moviesbot-uasafb"		

API_KEY = '9c1e8a8b'
client = omdb.OMDBClient(apikey=API_KEY)

def get_new_movie(parameters):
	print(parameters)
	movie_title = parameters.get('movie_title')
	return client.get(title=movie_title,tomatoes=True)
def get_new_series(parameters):
	print(parameters)
	series_title = parameters['series_title']
	return client.search_series(series_title)

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result


def fetch_reply(msg, session_id):
	response = detect_intent_from_text(msg, session_id)
	if response.intent.display_name == 'movie':
		news = get_new_movie(dict(response.parameters))
		type1 = news['type']
		str1 = f"\n\nPlot:\n{news['plot']}\n\nThis movie has its release in {news['year']} directed by {news['director']} with actors {news['actors']} and got {news['awards']} "
		return str1,news['poster']
	elif response.intent.display_name == 'series':
		news = get_new_series(response.parameters)
		type1 = news[0]['type']
		str1 = f"\n\nThis series {news[0]['title']} has its release in {news[0]['year']} "
		return str1,news[0]['poster']
	else:
		return response.fulfillment_text
 
