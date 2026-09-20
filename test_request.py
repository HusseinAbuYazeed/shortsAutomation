import requests

story = """
Anything that was once harmless, now has become a monster, trying to harness. A mound is now a creature. It looks and looms over the lunar surface. Its neck is long, like a champagne glass. Its eyes are large, watching afar, and its skin is as pale as a dead body. Its arms stretch down to its toes, which connect to its legs that tower over those. Its skin is just like shrink-wrap on a box of chocolates. The thing seems to not notice the group, until their brains tells it to. Its head snaps in their direction, tweaking and twitching to their heartbeat. They panic, and trample, and run the other way, only for it to disappear.

A few hours passed and nothing had changed. Their hunger and thirst only made everything worse. They wonder and wonder, finding their ship, lost in the darkness biting their lips. They found something, it resembled their rusty ol' ship. They got closer and closer, until it faded away. The ship was now an obelisk. It was unusual. It had small, long hairs on the east and west sides, waving in the lunar wind. It was tall, twice the size of the ship. Its eye opened, watching them each, as they scrambled away, finding their ship.

For once, they had their ship, lighting up the surroundings. They entered the rusty craft, with little of their sanity left. They start up the engines and switch on the systems taking off from the moon. They hope to never return. The surface grows smaller and smaller, drifting away from the capsule. Their sanity makes them believe that they are headed for earth. But belief was all that remained. Them and their capsule drifts into the black, never to be seen ever again.
"""

response = requests.post(
    "http://127.0.0.1:8000/generate",
    json={"story_text": story},
)

print("Status code:", response.status_code)
print(response.json())