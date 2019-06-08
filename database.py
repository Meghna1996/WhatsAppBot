from pymongo import MongoClient

records = None


def initialize_db():
	client = MongoClient('mongodb+srv://user:pass@cluster0-rftu5.mongodb.net/test?retryWrites=true&w=majority')
	db = client.get_database('whatsapp_bot')
	records = db.preferences
	return records
	# print(records.count_documents({}))


def insert_db(data):
	records = initialize_db()
	dicts = {}
	dicts['title'] = data['title']
	dicts['year'] = data['year']
	dicts['genre'] = data['genre']
	records.insert_one(dicts)


def get_favorite(characteristics):
	records = initialize_db()
	max_count = 0
	if characteristics == 'title' or characteristics == 'name' or characteristics == 'movie':
		characteristics = 'title'
	if characteristics == 'genre' or type == 'type':
		characteristics = 'genre'
	for item in list(records.find()):
		name = item[characteristics]
		count = records.count_documents({characteristics: name})
		if count > max_count:
			max_count = count
			max_title = name
	return max_title
