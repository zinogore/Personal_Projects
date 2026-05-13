import random
import json
from src.app.repositories.repository import store_ids_to_polls, fetch_message_ids_from_polls, delete_poll, fetch_chat_ids_from_polls, store_repoll_options, fetch_repoll_options, update_repoll_options

class BotCommands:
    def __init__(self, **kwargs):
        self.poll_options = kwargs["poll_options"]
        self.num_options = kwargs.get("num_options")
        self.num_shuffle = kwargs.get("num_shuffle")
        self.non_rude = kwargs.get("non_rude")
        self.repoll_options = []
        self.logger = kwargs.get("logger")
    
    # Helpers
    def get_options(self):
        """
        Shuffle Poll options n times
        
        Choose n unique options and append to list
        """
        options = []
        len_poll_options = len(self.poll_options)
        for _ in range(self.num_shuffle):
            random.shuffle(self.poll_options)
        for i in random.sample(range(len_poll_options),self.num_options):
            options.append(self.poll_options[i])
        return options
        
    # Commands
    async def help_command(self, update, context):
        """
        Reply to /help command with list of help commands
        """
        self.logger.info("help_command started")
        if self.non_rude:
            help_text = "get useful bot commands with how to use guide"
            close_text = "close previously generated poll and print podium results - podium means top 3"
            step_2 = "Cast your vote"
            step_4 = "Close the poll with /close_poll command - you cannot vote on a closed poll"
            step_5 = "The poll podium results will be shown"
            step_7 = "Enjoy the results and climbing!"
        else:
            help_text = "get bot commands for climbers without eyes"
            close_text = "close previously generated poll and print podium results - podium means top 3 you crayon eater"
            step_2 = "Cast your pathetic vote"
            step_4 = "Close the poll with /close_poll command - you cannot vote on a closed poll, read step 3 you idiot"
            step_5 = "The poll podium results will be shown - again, podium means top 3 you birdbrain"
            step_7 = "Enjoy the gym of NOT your choice sucker"
        await update.message.reply_text(f"""
    Hello!
    /help - {help_text}
    /generate_poll - generate climb where poll with {self.num_options} options
    /close_poll - {close_text}
    /re_poll - re-poll (single choice) with podium results

    How to use:
    1. Generate a climb where poll with /generate_poll command
    2. {step_2}
    3. Wait for voting to finish amongst awesome climbers
    4. {step_4}
    5. {step_5}
    6. Use /re_poll to re-poll with podium results - this poll will be single choice
    7. {step_7}""")

    async def generate_poll_command(self, update, context):
        """
        Reply to /generate_poll command with generated poll
        Store chat_id, poll_id and message_id in db
        """
        self.logger.info("generate_poll_command started")
        chat_id = update.effective_chat.id
        message = await context.bot.send_poll(
            chat_id = chat_id,
            question = 'POLL - climb where la sial',
            options = self.get_options(),
            is_anonymous = False,
            allows_multiple_answers = True
        )
        self.logger.info(f"store_ids_to_polls: chat_id{chat_id}, message_id:{message.id}, poll_id:{message.poll.id}")
        store_ids_to_polls(chat_id=chat_id, message_id=message.id, poll_id=message.poll.id)
        return

    async def close_poll_command(self, update, context):
        """
        Check if any message_id is present in chat using chat_id
        Close poll using message_id
        """
        self.logger.info("close_poll_command started")
        chat_id = update.effective_chat.id
        message_ids = fetch_message_ids_from_polls(chat_id=chat_id)
        self.logger.info(f"Polls message_ids: {message_ids}")
        if not message_ids:
            if self.non_rude:
                reply = "There are no polls to close!"
            else: reply = "Check your eyes, there are no polls to close!"
            await update.message.reply_text(reply)
            return
        # reverse sort to get latest message_id
        message_ids.sort(reverse=True)
        last_message_id = message_ids[0]
        self.logger.info(f'Stopping poll - chat_id: {chat_id}, message_id: {last_message_id}')
        await context.bot.stop_poll(chat_id=chat_id, message_id=last_message_id)
        
    # print poll results after closing poll
    async def get_poll_results(self, update, context):
        """
        Get poll updates
        Store results and sort by descending votes
        Send poll results to chat
        """
        self.logger.info("get_poll_results started")
        poll = update.poll
        if poll.is_closed:
            poll_id = poll.id
            self.logger.info(f'Poll: {poll.question} (ID: {poll_id}) is closed.')
            res = [(o.text,o.voter_count) for o in poll.options]
            sorted_res = sorted(res, key = lambda item: item[1], reverse = True)
            self.repoll_options = []
            message = 'Poll results:'
            highest_vote = sorted_res[0][1]
            for i,v in enumerate(sorted_res):
                # append podium regardless
                if i < 3:
                    self.repoll_options.append(v)
                    message += f'\n{i+1}. {v[0]} - Votes: {v[1]}'
                # check if votes after podium = highest vote, if true, append to list for printing
                elif v[1] == highest_vote:
                    self.repoll_options.append(v)
                    message += f'\n{i+1}. {v[0]} - Votes: {v[1]}'
                else: break
            self.logger.info(f"repoll_options: {self.repoll_options}")
            chat_id = fetch_chat_ids_from_polls(poll_id=poll_id)
            if not fetch_repoll_options(chat_id=chat_id):
                store_repoll_options(chat_id=chat_id, repoll_options=json.dumps(dict(self.repoll_options)))
            else: update_repoll_options(chat_id=chat_id, repoll_options=json.dumps(dict(self.repoll_options)))
            delete_poll(poll_id=poll_id)
            await context.bot.send_message(chat_id=chat_id, text=message)

    # re-poll top 3 from previous closed poll
    async def repoll_command(self, update, context):
        """
        Repoll based on previously closed poll podium results
        """
        self.logger.info("repoll_command started")
        # generate single choice poll with options
        chat_id = update.effective_chat.id
        result = fetch_repoll_options(chat_id=chat_id)
        if result:
            result = json.loads(result)
            options = [k for k,v in result.items()]
            self.logger.info(f"options: {options}")
        else:
            if self.non_rude:
                reply = "Please close a poll before repolling!"
            else: reply = "Wear your glasses, how to repoll if you did not close any poll?"
            await update.message.reply_text(reply)
            return
        message = await context.bot.send_poll(
            chat_id = chat_id,
            question = 'REPOLL - want to poll how many times la sial',
            options = options,
            is_anonymous = False,
            allows_multiple_answers = False
        )
        store_ids_to_polls(chat_id=chat_id, message_id=message.id, poll_id=message.poll.id)
