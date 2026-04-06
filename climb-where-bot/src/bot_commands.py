import random
from src.data_handler import get_list_of_gym_names

POLL_OPTIONS = get_list_of_gym_names()
NUM_OPTIONS = 7
NUM_SHUFFLE = 3
dict_chat_id = {}
global_chat_id = None
repoll_options = []

# Helpers
def get_options(poll_options=POLL_OPTIONS, n_options=NUM_OPTIONS, n_shuffle=NUM_SHUFFLE):
    """
    Shuffle Poll options n times
    
    Choose n unique options and append to list
    """
    for _ in range(n_shuffle):
        random.shuffle(poll_options)
    options = []
    for i in random.sample(range(len(poll_options)),n_options):
        options.append(poll_options[i])
    return options

# Commands
async def help_command(update, context):
    """
    Reply to /help command with list of help commands
    """
    await update.message.reply_text(f"""
Hello!
/help - get bot commands for climbers without eyes
/generate_poll - generate climb where poll with {NUM_OPTIONS} options
/close_poll - close previously generated poll and print podium results - podium means top 3 you crayon eater
/re_poll - re-poll (single choice) with podium results

How to use:
1. Generate a climb where poll with /generate_poll command
2. Cast your pathetic vote
3. Wait for voting to finish amongst awesome climbers
4. Close the poll with /close_poll command - you cannot vote on a closed poll, read step 3 you idiot
5. The poll podium results will be shown - again, podium means top 3 you birdbrain
6. Use /re_poll to re-poll with podium results - this poll will be single choice
7. Enjoy the gym of NOT your choice sucker""")

async def generate_poll_command(update, context):
    """
    Reply to /generate_poll command with generated poll
    Store message id in dictionary stack
    """
    chat_id = update.effective_chat.id
    message = await context.bot.send_poll(
        chat_id = chat_id,
        question = 'POLL - climb where la sial',
        options = get_options(),
        is_anonymous = False,
        allows_multiple_answers = True
    )
    # store poll message id and chat id in dict of stack
    if chat_id in dict_chat_id:
        dict_chat_id[chat_id].append(message.message_id)
    else: dict_chat_id[chat_id] = [message.message_id]
    print('dict_chat_id:',dict_chat_id)

async def close_poll_command(update, context):
    """
    Check if any message id is in dictionary stack
    Pop stored poll and close it
    """
    chat_id = update.effective_chat.id
    # check chat_id exist
    if chat_id not in dict_chat_id:
        await update.message.reply_text('Check your eyes, there is no poll to close!')
        return
    # check for empty list
    elif not dict_chat_id[chat_id]:
        await update.message.reply_text('Wear your glasses, there is no poll to close!')
        return
    # pop last poll message id and chat id
    message_id = dict_chat_id[chat_id].pop()
    # bot.stop_poll(message_id, chat_id)
    print(f'Stopping poll - chat_id: {chat_id}, message_id: {message_id}')
    global global_chat_id
    global_chat_id = chat_id
    await context.bot.stop_poll(chat_id = chat_id, message_id = message_id)
    
# print poll results after closing poll
async def get_poll_results(update, context):
    """
    Get poll updates
    Store results and sort by descending votes
    Send poll results to chat
    """
    poll = update.poll
    if poll.is_closed:
        print(f'Poll: {poll.question} (ID: {poll.id} is closed.)')
        res = [(o.text,o.voter_count) for o in poll.options]
        sorted_res = sorted(res, key = lambda item: item[1], reverse = True)
        global repoll_options
        repoll_options = []
        message = 'Poll results:'
        highest_vote = sorted_res[0][1]
        for i,v in enumerate(sorted_res):
            # append podium regardless
            if i < 3:
                repoll_options.append(v)
                message += f'\n{i+1}. {v[0]} - Votes: {v[1]}'
            # check if votes after podium = highest vote, if true, append to list for printing
            elif v[1] == highest_vote:
                repoll_options.append(v)
                message += f'\n{i+1}. {v[0]} - Votes: {v[1]}'
            else: break
        print('Bot:',message)
        await context.bot.send_message(chat_id = global_chat_id, text = message)

# re-poll top 3 from previous closed poll
async def repoll_command(update, context):
    """
    Repoll based on previously closed poll podium results
    """
    # get re-poll options
    options = [ele[0] for ele in repoll_options]
    # generate single choice poll with options
    chat_id = update.effective_chat.id
    message = await context.bot.send_poll(
        chat_id = chat_id,
        question = 'REPOLL - want to poll how many times la sial',
        options = options,
        is_anonymous = False,
        allows_multiple_answers = False
    )
    # store poll message id and chat id in dict of stack
    if chat_id in dict_chat_id:
        dict_chat_id[chat_id].append(message.message_id)
    else: dict_chat_id[chat_id] = [message.message_id]
    print('dict_chat_id:',dict_chat_id)
