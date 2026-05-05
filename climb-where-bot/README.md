**Problem:**
   * My climbing group likes to meet up weekly to climb in our favourite gyms in Singapore. We will always struggle to decide on the gym for that week due to our easy-going and accomodating vibe. The polling process on telegram is very manual and requires consistent effort to track which gyms have been visited before (to avoid revisiting the following week).

**Solution:**
   * My telegram polling bot helps with this problem by automating the polling process.
   * Manual effort is reduced when:
        - Typing out each individual gym name
        - Closing the poll to get podium results (Top 3 voted gyms)
        - Repolling if there are ties
   * Additional benefits include:
        - Available 24/7 when hosted on your own server (e.g. RaspberryPi)
   * WIP:
        - Weighted options to generate least visited gyms
   * Future works:
        - LLM chatbot trained on conversations within the chat group for fun conversations
        - Weather information near gym location to prepare user
        - Restuarants near gym location for easy meal options after workout 

|Command|Description|Visualization|
|-|-|-|
|```/help```|List helpful commands with step by step guide (strong language is just for bot personality)|![alt_text](https://github.com/zinogore/Personal_Projects/blob/main/climb-where-bot/assets/help_command.jpg)|
|```/generate_poll```|Generate poll with randomized options|![alt_text](https://github.com/zinogore/Personal_Projects/blob/main/climb-where-bot/assets/generate_command.jpg)|
|```/close_poll```|Close latest poll and return podium results|![alt_text](https://github.com/zinogore/Personal_Projects/blob/main/climb-where-bot/assets/close_command.jpg)|
|```/re_poll```|Re-poll with previous closed poll results|![alt_text](https://github.com/zinogore/Personal_Projects/blob/main/climb-where-bot/assets/repoll_command.jpg)|

|File|Description|
|-|-|
|[main.py](main.py)|main entry point to run the bot|
|[bot_responses.py](src/bot_responses.py)|handles messages with specific keywords|
|[bot_commands.py](src/bot_commands.py)|handles bot commands|
|[db_handler.py](src/db_handler.py)|handles database actions|
|[database.db](instance/database.db)|database file|
|[db.drawio](climb_where_bot_db.drawio)|drawio file for db architecture|
|[utilities](utilities/)|utilities functions|