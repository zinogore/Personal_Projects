import random

class BotCommands:
    def __init__(self, **kwargs):
        self.poll_options = kwargs.get("poll_options")
        self.num_options = kwargs.get("num_options")
        self.num_shuffle = kwargs.get("num_shuffle")
        self.non_rude = kwargs.get("non_rude")
        self.dict_chat_id = kwargs.get("dict_chat_id")
        self.dict_poll_id = kwargs.get("dict_poll_id")
        self.repoll_options = kwargs.get("repoll_options")
        self.logger = kwargs.get("logger")
        self.logger.info(self.poll_options)
        self.logger.info(self.num_options)
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

    def store_ids(self, chat_id, message_id, poll_id):
        # store poll message id and chat id in dict of stack
        if chat_id in self.dict_chat_id:
            self.dict_chat_id[chat_id].append(message_id)
        else: self.dict_chat_id[chat_id] = [message_id]
        self.dict_poll_id[poll_id] = chat_id
        self.logger.info(f"dict_chat_id: {self.dict_chat_id}")
        self.logger.info(f"dict_poll_id: {self.dict_poll_id}")
        
    # Commands
    async def help_command(self, update, context):
        """
        Reply to /help command with list of help commands
        """
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
        Store message id in dictionary stack
        """
        chat_id = update.effective_chat.id
        message = await context.bot.send_poll(
            chat_id = chat_id,
            question = 'POLL - climb where la sial',
            options = self.get_options(),
            is_anonymous = False,
            allows_multiple_answers = True
        )
        self.store_ids(chat_id=chat_id, message_id=message.id, poll_id=message.poll.id)

    async def close_poll_command(self, update, context):
        """
        Check if any message id is in dictionary stack
        Pop stored poll and close it
        """
        chat_id = update.effective_chat.id
        # check chat_id exist
        if chat_id not in self.dict_chat_id:
            await update.message.reply_text('Check your eyes, there is no poll to close!')
            return
        # check for empty list
        elif not self.dict_chat_id[chat_id]:
            await update.message.reply_text('Wear your glasses, there is no poll to close!')
            return
        # pop last poll message id and chat id
        message_id = self.dict_chat_id[chat_id].pop()
        self.logger.info(f'Stopping poll - chat_id: {chat_id}, message_id: {message_id}')
        await context.bot.stop_poll(chat_id = chat_id, message_id = message_id)
        
    # print poll results after closing poll
    async def get_poll_results(self, update, context):
        """
        Get poll updates
        Store results and sort by descending votes
        Send poll results to chat
        """
        poll = update.poll
        if poll.is_closed:
            self.logger.info(f'Poll: {poll.question} (ID: {poll.id}) is closed.')
            res = [(o.text,o.voter_count) for o in poll.options]
            sorted_res = sorted(res, key = lambda item: item[1], reverse = True)
            # global repoll_options
            # repoll_options = []
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
            self.logger.info(f"Bot sent: {self.repoll_options}")
            chat_id = self.dict_poll_id.pop(poll.id)
            await context.bot.send_message(chat_id = chat_id, text = message)

    # re-poll top 3 from previous closed poll
    async def repoll_command(self, update, context):
        """
        Repoll based on previously closed poll podium results
        """
        # get re-poll options
        options = [ele[0] for ele in self.repoll_options]
        # generate single choice poll with options
        chat_id = update.effective_chat.id
        message = await context.bot.send_poll(
            chat_id = chat_id,
            question = 'REPOLL - want to poll how many times la sial',
            options = options,
            is_anonymous = False,
            allows_multiple_answers = False
        )
        self.store_ids(chat_id=chat_id, message_id=message.id, poll_id=message.poll.id)
