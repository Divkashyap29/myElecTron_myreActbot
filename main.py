import sys 
from agent.react_loop import run_agent



if '--message' in sys.argv: 
    idx = sys.argv.index('--message')
    msg = sys.argv[idx+1]
    print(run_agent(msg))

else :
    print('kaashvi is ready. PLease type your msg here')
    print('(Type quit to exist)\n')

    while True:
        user_input = input('You: ').strip()
        if user_input.lower()=='quit':
            break
        repsonse = run_agent(user_input)
        print(f'\nkaashvi : {repsonse}\n')
        

