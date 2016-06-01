'''
    Copyright 2016 Debayan Banerjee, Shreyank Gupta    

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

import urllib2,json
from random import randint

class WeekendModel(object):
    dc = {}
    def __init__(self, logger):
        self.logger = logger
        self.restaurant_name = None
        self.restaurant_address = None
        self.movie_name = None
        self.zomatokey = '39e91731af08d26261adf655948d9daa'
    
    def ifintentclear(self, stt, text=None, reply=[]):
        if 'movie' in text.lower() or 'restaurant' in text.lower():
            return True
        else:
            return False

    def ifintentmovie(self, stt, text=None, reply=[]):
        if 'movie' in text.lower():
            req = urllib2.Request("http://www.omdbapi.com/?s=bot")
            contents = urllib2.urlopen(req).read()
            d = json.loads(str(contents))
            sub = randint(0,9)
            self.movie_name = d['Search'][sub]['Title']
            return True
        else:
            return False

    def ifintentrestaurant(self, stt, text=None, reply=[]):
        if 'restaurant' in text.lower():
            return True
        else:
            return False

    def ifvalidcity(self, stt, text=None, reply=[]):
        req = urllib2.Request("https://developers.zomato.com/api/v2.1/locations?query=%s"%text, headers={'user-key': '39e91731af08d26261adf655948d9daa','Accept':'application/json'})
        contents = urllib2.urlopen(req).read()
        d = json.loads(contents)
        if len(d['location_suggestions']) == 0:
            return False
        else:
           entity_id = d['location_suggestions'][0]['entity_id']
           entity_type = d['location_suggestions'][0]['entity_type']
           d = {}
           req = urllib2.Request("https://developers.zomato.com/api/v2.1/location_details?entity_id=%s&entity_type=%s"%(entity_id, entity_type), headers={'user-key': '39e91731af08d26261adf655948d9daa','Accept':'application/json'})
           contents = urllib2.urlopen(req).read()
           d = json.loads(contents)
           self.restaurant_name = d['best_rated_restaurant'][0]['restaurant']['name']
           self.restaurant_address = d['best_rated_restaurant'][0]['restaurant']['location']['address']
           return True 
