from artist.models import Artist
from venue.models import Venue
from django.contrib.auth.models import User
import csv
import os

def test():
    print('test')

def upload_artists(path, filename):
os.chdir(''/home/scratchy/Documents') # changes the directory
with open('users.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        obj = User.objects.create_user(username=row['username'], email=row['email'],
        password=row['password'], first_name=row['first_name'])
        obj.profile.account_type = row['account_type']
        obj.save()
        print('created user - ' + row['username'])
        if (row['account_type'] == 'artist'):
            obj = Artist.objects.create(artist_name=row['artist_name'], artist_id=row['id'],
            artist_owner=Users.objects.get(username=row['username']), artist_genres=row['genres'], artist_location = row['town'])
            obj.save()
            print('created artist - ' + row['artist_name'])
        elif (row['account_type'] == 'venue'):
            obj = Venue.objects.create(venue_name=row['venue_name'], venue_id=row['id'],
            venue_owner=obj, venue_genres=row['genres'])
            obj.save()
            print('created venue -  ' + row['artist_name'])

with open('users.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if (row['account_type'] == 'artist'):
            obj = Artist.objects.get(artist_name=row['artist_name'])
            obj.artist_id = row['id']
            obj.save()
            print('updated artist - ' + row['artist_name'])
        elif (row['account_type'] == 'venue'):
            obj = Venue.objects.get(venue_name=row['venue_name'])
            obj.venue_id = row['id']
            obj.save()
            print('updated venue -  ' + row['venue_name'])
