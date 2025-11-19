import json
from igdb_client import wrapper

request = wrapper()
byte_array = request.api_request(
            'games',
            'fields name, total_rating, total_rating_count, first_release_date, slug, platforms.name; where total_rating != null & total_rating_count >= 100; sort total_rating desc; limit 50;'
          )

print(json.loads(byte_array.decode("utf-8")))
