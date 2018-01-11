import twitch
from twitch.api import helix

twitch.queries.CLIENT_ID = "uq0whcvbh75kuy1g9xvu7i2n1xa9gr"
idu = helix.users.get_users(user_login=["yogscast"])
print(idu)
stream = helix.streams.get_streams(user_id=idu)

print(type(stream))
