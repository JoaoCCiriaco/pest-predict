echo "SELECT name FROM songs;" > 1.sql
echo "SELECT name FROM songs ORDER BY tempo;" > 2.sql
echo "SELECT name FROM songs ORDER BY duration_ms DESC LIMIT 5;" > 3.sql
echo "SELECT name FROM songs WHERE danceability > 0.75 AND energy > 0.75 AND valence > 0.75;" > 4.sql
echo "SELECT AVG(energy) FROM songs;" > 5.sql
echo "SELECT songs.name FROM songs JOIN artists ON songs.artist_id = artists.id WHERE artists.name = 'Post Malone';" > 6.sql
echo "SELECT AVG(energy) FROM songs JOIN artists ON songs.artist_id = artists.id WHERE artists.name = 'Drake';" > 7.sql
echo "SELECT name FROM songs WHERE name LIKE '%feat.%';" > 8.sql
