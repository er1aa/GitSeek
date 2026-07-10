import requests,json,shutil,os
from user_agent import generate_user_agent
from colorama import Fore as F1,init
from pathlib import Path

init(autoreset=True)
green=F1.LIGHTGREEN_EX
blue=F1.LIGHTBLUE_EX
cyan=F1.LIGHTCYAN_EX
magenta=F1.LIGHTMAGENTA_EX
red=F1.LIGHTRED_EX
reset=F1.RESET
yellow=F1.LIGHTYELLOW_EX
def github_profile(username:str):

    information={}

    url=f"https://api.github.com/users/{username}"
    head={
        "user-agent" : generate_user_agent()
    }
    req=requests.get(url=url,headers=head,timeout=5)
    if req.status_code!=200:

        information["🌐 Status Code"]=f"{req.status_code}"

        information['[x] Error'] = f"Error: Either username is wrong or something Happend"
    else:

        response=req.json()

        information["[→] Username"] = response.get("login")

        information["[→] ID"] = response.get("id")

        information["[→] Name"] = response.get("name")

        information["[→] Profile Picture"] = response.get("avatar_url")

        information["[→] Profile URL"] = response.get("html_url")

        information["[→] Company"] = response.get("company")

        information["[→] Bio"] = response.get("bio")

        information["[→] Location"] = response.get("location")

        information["[→] Email"] = response.get("email")

        information["[→] Blog"] = response.get("blog")

        information["[→] Followers"] = response.get("followers")

        information["[→] Following"] = response.get("following")

        information["[→] Twitter Username"] = response.get("twitter_username")

        information["[→] Public Repositories"] = response.get("public_repos")

        information["[→] Public Gists"] = response.get("public_gists")

        information["[→] Account Created"] = response.get("created_at")

        information["[→] Last Updated"] = response.get("updated_at")

    return information

def get_followers(userame):

    url=f"https://api.github.com/users/{userame}/followers"
    head={
        "user-agent" : generate_user_agent()
    }
    req=requests.get(url=url,headers=head)
    # print(req.status_code)
    # print(req.json())
    if req.status_code!=200:
        return f"[-] {red}Error to get followers{reset}"
    else:
        resp=req.json()
        tt=f'Top Followers of user: {userame}\n'
        filename = Path(f"{userame}_followers.txt")

        with filename.open("w", encoding="utf-8") as f:
            f.write(tt+'\n')
            for i, j in enumerate(resp, start=1):
                f.write(f"{i} = {j['login']}\n")

        return f"[+] {green}Followers fetched and saved at:{reset} {filename.resolve()}"
    

def get_repos(username):
    text=''
    url=f"https://api.github.com/users/{username}/repos"
    head={
        "user-agent" : generate_user_agent()
    }
    req=requests.get(url=url,headers=head)

    if req.status_code!=200:
        text= f"[-]{red}Error to fetch Repos{reset}"
    else:
        resp=req.json()
        if len(resp)==0:
            text=f"[=]{yellow}No repo found"

        else:
            filename = Path(f"{username}_repos.json")
            repo_list={}


            for i, j in enumerate(resp, start=1):
                repo_list[f'repository: {i}'] ={
                    f"Repository Name" : j["name"],
                    f"Full Repo Naame": j['full_name'],
                    "Repository Link": j['html_url'],
                    "Total Watches Count": j['watchers_count'],
                    "Total Stars" : j['stargazers_count']
                }
            with filename.open("w", encoding="utf-8") as f:
                json.dump(repo_list,f,indent=3)

            text= f"[+] {green}Repository fetched and saved at:{reset} {filename.resolve()}"
        
    return text


def main():
    os.system('cls' if os.name=='nt' else 'clear')
    while True:
        text_input=input(f'{yellow}Enter Github Username:{reset} ').strip().lower()
        # print(text_input)
        if len(text_input)==0:
            print(f'[x]{red}Error input username')
            continue
        else:
            if"@" in  text_input[0]:
                username=text_input.split('@')[1]

            else:
                username= text_input

        print(f'[+]{magenta}Github info for: {reset}{username}')
        try:
            info=github_profile(username)
            for x,y in info.items():
                value_color= red if 'error' in x.lower() else green
                # print(f'{value_color}jdhdhdh')
                print(f"{cyan}{x:<18}{reset}:{reset}{value_color}{y}{reset} ")
        except Exception as e:
            print(f'[=]{red} Unknown Error: {reset}{e}')
        print(f"{reset}=" * shutil.get_terminal_size().columns)

        git_cli=(
            f"""{cyan}[+]{reset} {magenta}Please choose an operation:{reset}

    {green}[1]{reset} --> Fetch Top Followers
    {green}[2]{reset} --> Fetch All Repositories
    {green}[3]{reset} --> Restart / again check 
    {red}[4]{reset} --> Exit
        """)
        
        while True:
            print(git_cli)

            choice=input(f'{yellow}➜ Enter your choice (1/2/3/4): {reset}').strip()
            if choice not in ["1", "2", "3","4"]:
                print(f"❌{red}Invalid choice!{reset}")
                print(git_cli)

            else:
                if choice=='1':
                    print(get_followers(username))
                    continue
                elif choice =='2':
                    print(get_repos(username))
                    continue
                elif choice=='3':
                    break
                elif choice=='4':
                    print(f'{green} Thanks for using\n{reset} Please Join: {cyan} https://t.me/ankubyte{reset}')
                    exit()

                else:
                    break
        
main()