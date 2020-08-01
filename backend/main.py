import subprocess
import requests
import asyncio
import websockets

id = "" 
api = ""

names = [""]

async def time(websocket, path):

    async def info(name):
        id_fb = dict()
        id_ig = dict()
        id_github = dict()

        process = subprocess.Popen(["python", "dork-cli.py", "-m", "1", "-e", id, "-k", api, name], stdout=subprocess.PIPE)
        result = process.communicate()[0].decode("utf-8") 
        results = result.split('\n')
        
        usernames = set()
        for r in results:
            if not name in id_fb.keys() and 'facebook' in r:
                id_fb[name] = r.split('.com/')[-1].partition("/")[0].partition("?")[0]
                usernames.add(id_fb[name])
                to_print = f"FB: <a href='https://www.facebook.com/{id_fb[name]}'>{id_fb[name]}</a>"
                # print(to_print)
                await websocket.send(to_print)
            elif not name in id_ig.keys() and 'instagram' in r:
                id_ig[name] = r.split('.com/')[-1].partition("/")[0].partition("?")[0]
                usernames.add(id_ig[name])
                # to_print = "IG: " + id_ig[name]
                to_print = f"IG: <a href='https://www.instagram.com/{id_ig[name]}'>{id_ig[name]}</a>"
                # print(to_print)
                await websocket.send(to_print)
            elif not name in id_github.keys() and 'github' in r:
                id_github[name] = r.split('.com/')[-1].partition("/")[0].partition("?")[0]
                usernames.add(id_github[name])
                # to_print = "GitHub: " + id_github[name]
                to_print = f"GitHub: <a href='https://www.github.com/{id_github[name]}'>{id_github[name]}</a>"
                # print(to_print)
                await websocket.send(to_print)
            if len(usernames) == 3:
                break
    
        # print("-\nOther websites: (may take ~4 min to scan)")
        await websocket.send("-")
        await websocket.send("Other websites: (may take ~4 min to scan)")
        for name in usernames:
            with subprocess.Popen(["python3", "-u", "web_accounts_list_checker.py", "-u", name],
                                    stdout=subprocess.PIPE,
                                    bufsize=1,
                                    universal_newlines=True) as process:
                for line in process.stdout:
                    line = line.rstrip()
                    # print(f"line = {line}")
                    await websocket.send(f'<a href="{line}">{line}</a>')

    command = await websocket.recv()
    if command == "get_info":  
        name = await websocket.recv()      
        await info(name) # this is async 
        # await info(names[0]) # this is async 


start_server = websockets.serve(time, "0.0.0.0", 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()