from pymongo import MongoClient

records = None


def initialize_db():
	client = MongoClient('mongodb+srv://user:pass@cluster0-rftu5.mongodb.net/test?retryWrites=true&w=majority')
	database_name = 'whatsapp_bot'
	db = client.get_database(database_name)
	records = db.movie_records
	return records
	# print(records.count_documents({}))


def insert_db(data):
	records = initialize_db()
	dicts = {}
	dicts['title'] = data['title']
	dicts['year'] = data['year']
	dicts['genre'] = data['genre']
	dicts['actors'] = data['actors']
	records.insert_one(dicts)


def get_favorite_movie(characteristics):
	records = initialize_db()
	max_count = 0
	for item in list(records.find()):
		name = item[characteristics]
		count = records.count_documents({characteristics: name})
		if count > max_count:
			max_count = count
			max_title = name
	if(max_count == 0):
		return "not yet searched!"
	else:
		return max_title
