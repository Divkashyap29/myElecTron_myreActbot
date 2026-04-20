import sys, os, json
from agent.react_loop import run_agent
from integrations.reminder_tools import CheckRemindersTool


if '--message' in sys.argv:
    idx = sys.argv.index('--message')
    msg = sys.argv[idx+1]
    history_path = 'conversation_history.json'
    if os.path.exists(history_path):
        with open(history_path, 'r') as f:
            history = json.load(f)
    else:
        history = []
    response, history = run_agent(msg, history)
    print(response)
    with open(history_path, 'w') as f:
            json.dump(history, f)

else :
    # Check for due reminders at startup
    reminder_check = CheckRemindersTool()
    fired = reminder_check.execute()
    if 'fired' in fired:
        print(fired)
        print()

    print('kaashvi is ready. Please type your msg here')
    print('(Type quit to exit)\n')
    history =[]
    while True:
        user_input = input('You: ').strip()
        if user_input.lower()=='quit':
            break
        response, history = run_agent(user_input, conversation_history=history, stream=True)
        print(f'\nkaashvi : {response}\n')
