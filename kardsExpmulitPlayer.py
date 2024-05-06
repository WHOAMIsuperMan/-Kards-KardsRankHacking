import requests
import json
import time
import threading
import random
import urllib3
import sys
#import curses

#is that new account?
isNewACount = False
matchesID=()
Ownside=()
#填写替换你的玩家ID
playerID="Put your Player ID in Here"
#填写替换你的卡组ID
deckID="put your deckID in Here"
#填写替换你的Cookie
cookie="[Put your Cookie In Here]"
urllib3.disable_warnings()

def keep_alive(keepAliveUrl,headers):
    while True:
        try:
            response = requests.put(keepAliveUrl,headers=headers,verify=False)
            if response.status_code == 200:
                #print("请求成功！")
                pass
                #print("响应内容：", response.text)
                #return response.text
            else:
                #print("请求失败！")
                pass
                #print("状态码：", response.status_code)
            time.sleep(30)
        except requests.exceptions.RequestException as e:
            pass

def getMatcheID(getMatchesInfoUrl,headers):
    #获取比赛信息
    global matchesID
    global Ownside
    #print(r2.text)
    while True:
        r2=requests.get(getMatchesInfoUrl,headers=headers,verify=False,timeout=3)
        if "match_id" in r2.text:
            #sys.stdout.flush()
            print("已找到比赛")
            res=json.loads(r2.text)
            matchdata=res['match_and_starting_data']
            currentMatch=matchdata['match']
            matchesID=currentMatch.get('match_id')
            #在哪边
            Ownside=currentMatch.get('action_side')
            time.sleep(1)
            break
        else:
            sys.stdout.flush()
            sys.stdout.write("\r正在查找比赛...")
            time.sleep(1)

#一些随机的游玩动作
def pingUpload(actionURL,headers,n):
    ping = random.randint(610,650)
    data = {
        "min_action_id": n, 
        "opponent_id": -2140, #-2120
        "time_since_opponent_ping": ping
    }
    response = requests.post(actionURL,headers=headers,json=data,verify=False)
    #print("响应内容：", response.text)
    if response.status_code == 200:
        #print("请求成功！")
        pass
        #print("响应内容：", response.text)
        #return response.text
    else:
        #print("请求失败！")
        pass
        #print("状态码：", response.status_code)
    time.sleep(1)

def XStartOfGame(actionURL,headers):
    
    data = {
        "action_id": 1, 
        "action_type": "XStartOfGame", 
        "player_id": playerID, 
        "action_data": {"playerID": playerID}
    }
    response = requests.post(actionURL,headers=headers,json=data,verify=False)
    if response.status_code == 200:
        #print("请求成功！")
        pass
        #print("响应内容：", response.text)
        #return response.text
    else:
        #print("请求失败！")
        pass
        #print("状态码：", response.status_code)
    time.sleep(1)

#choiseCardStart
def XActionStartOfTurn(actionURL,headers):
    #n+=1
    
    data = {
        "action_id": 2, 
        "action_type": "XActionStartOfTurn", 
        "player_id": playerID, 
        "action_data": {"side": f"{Ownside}"}, 
        "sub_actions": [{"name": "ZActionChangeKredits","side": f"{Ownside}","oldKredits": 0,"newKredits": 1,"oldMaxKredits": 0,"newMaxKredits": 1,"triggerCardID": 0}] 
    }
    response = requests.post(actionURL,headers=headers,json=data,verify=False)
    if response.status_code == 200:
        #print("请求成功！")
        pass
        #print("响应内容：", response.text)
        #return response.text
    else:
        #print("请求失败！")
        pass
        #print("状态码：", response.status_code)
    time.sleep(1)

def uploadPlayerPCInfo(headers):
    logPlayerURL = f"https://kards.live.1939api.com/players/{playerID}"
    data = {
	"action": "log-player-event",
	"value": "event.player.stats.fps;{\"fps\": 60, \"fullscreenMode\": \"Windowed\", \"resolution\": \"2465x1406\", \"scalabilityLevel\": 3}"
}
    response = requests.put(logPlayerURL,headers=headers,json=data,verify=False,timeout=3)
    if response.status_code == 200:
        #print("请求成功！")
        pass
        #print("响应内容：", response.text)
        #return response.text
    else:
        #print("请求失败！")
        pass
        #print("状态码：", response.status_code)
    time.sleep(1)

#比赛数据记录获取
def GetMatchData(actionURL,headers,n):
    data = {
        "min_action_id": n, 
        "opponent_id": -2140, #-2120
        "time_since_opponent_ping": 0
    }
    response = requests.put(actionURL,headers=headers,json=data,verify=False,timeout=3)
    #print("响应内容：", response.text)
    if response.status_code == 200:
        #print("请求成功！")
        pass
        #print("响应内容：", response.text)
        #return response.text
    else:
        #print("请求失败！")
        pass
        #print("状态码：", response.status_code)
    time.sleep(1)

#计时器
def countdown(seconds):
    for i in range(seconds, 0, -1):
        sys.stdout.write("\r{:2d} seconds remaining...".format(i))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rCountdown complete!   \n")

#每日任务，暂未完成
def dailyMission(headers):
    dailyMissionURL = f"https://kards.live.1939api.com/players/{playerID}/dailymissions"

#新手任务自动完成，暂时做到第三个，可以继续完善
def NewPlayerMission(headers):
    NewPlayerMissionURL = f"https://kards.live.1939api.com/players/{playerID}"
    dataGerMan1 = {
	"action": "log-player-event",
	"value": "event.player.firebase;{\"event_name\": \"e_2020_select_german\"}"
    }

    dataGerMan2 = {
	"action": "log-player-event",
	"value": "event.player.firebase;{\"event_name\": \"e_2021_german_training_lobby\"}"
    }

    dataGerMan3_1 = {
	"item_id": "item_lugerinn",
	"slot": "item_1",
	"faction": "NotAvailable"
    }

    dataGerMan3 = {
	"item_id": "item_lugerinn",
	"slot": "item_1",
	"faction": "Germany"
    }

    dataGerMan4 = {
	"action": "log-player-event",
	"value": "event.player.firebase;{\"event_name\": \"event.player.9_first_tutorial_match_start\"}"
    }

    dataGerMan5 = {
	"action": "set-tutorials-seen",
	"value": "unlocking_germany_1"
    }

    dataGerMan6 = {
	"action": "log-player-event",
	"value": "event.player.firebase;{\"event_name\": \"e_2023_first_german_training_match_finish\"}"
    }

    dataGerMan7 = {
	"action": "log-player-event",
	"value": "event.player.firebase;{\"event_name\": \"event.player.11_second_tutorial_match_start\"}"
    }

    dataGerMan8 = {
	"action": "set-tutorials-seen",
	"value": "unlocking_germany_2"
    }

    dataGerMan9 = {
	"action": "log-player-event",
	"value": "event.player.firebase;{\"event_name\": \"e_2024_second_german_training_match_finish\"}"
    }

    NewPlayerUItemURL = f"https://kards.live.1939api.com/players/{playerID}/item"

    r1 = requests.put(NewPlayerMissionURL,headers=headers,json=dataGerMan1,verify=False)
    r2 = requests.put(NewPlayerMissionURL,headers=headers,json=dataGerMan2,verify=False)
    r3_1 = requests.post(NewPlayerUItemURL,headers=headers,json=dataGerMan3_1,verify=False)
    r3 = requests.post(NewPlayerUItemURL,headers=headers,json=dataGerMan3,verify=False)
    r4 = requests.put(NewPlayerMissionURL,headers=headers,json=dataGerMan4,verify=False)
    r5 = requests.put(NewPlayerMissionURL,headers=headers,json=dataGerMan5,verify=False)
    r6 = requests.put(NewPlayerMissionURL,headers=headers,json=dataGerMan6,verify=False)
    r7 = requests.put(NewPlayerMissionURL,headers=headers,json=dataGerMan7,verify=False)
    r8 = requests.put(NewPlayerMissionURL,headers=headers,json=dataGerMan8,verify=False)
    r9 = requests.put(NewPlayerMissionURL,headers=headers,json=dataGerMan9,verify=False)

    NewPlayerLobby = "https://kards.live.1939api.com/singleplayerlobby"


    dataGerMan10 = { "player_id": f"{playerID}", "deck_id": 0, "extra_data": { "match_type": "","category":"basic","faction":"britain","difficulty":"basic","match_type":"unlocking","my_deck":{"main_faction": "Germany","ally_faction":"Italy", "cards": [{"card_type":"card_location_berlin_unlock3_tut", "count":1},{"card_type":"card_unit_4_pioneer", "count":1},{"card_type":"card_event_combined_arms", "count":1},{"card_type":"card_unit_pak_36", "count":1},{"card_type":"card_unit_me_bf_109_g", "count":1},{"card_type":"card_unit_stug_iii", "count":1},{"card_type":"card_unit_grenadier_245", "count":1},{"card_type":"card_unit_panzergrenadier", "count":1},{"card_type":"card_unit_stug_iii", "count":1},{"card_type":"card_unit_4_pioneer", "count":1},{"card_type":"card_unit_panzergrenadier", "count":1},{"card_type":"card_event_combined_arms", "count":1},{"card_type":"card_unit_grenadier_245", "count":1},{"card_type":"card_event_eagle_claws", "count":1},{"card_type":"card_unit_me_bf_109_g", "count":1},{"card_type":"card_unit_panzer_iv_g", "count":1},{"card_type":"card_unit_81_infanterie_regiment", "count":1},{"card_type":"card_unit_panzer_38_t", "count":1},{"card_type":"card_unit_4_pioneer", "count":1},{"card_type":"card_unit_panzer_iv_g", "count":1},{"card_type":"card_unit_panzer_38_t", "count":1},{"card_type":"card_unit_italian_cavalry", "count":1},{"card_type":"card_unit_italian_cavalry", "count":1},{"card_type":"card_unit_pak_36", "count":1},{"card_type":"card_event_eagle_claws", "count":1},{"card_type":"card_unit_list_regiment", "count":1},{"card_type":"card_unit_panzer_35_t", "count":1},{"card_type":"card_unit_ju_87_b2", "count":1},{"card_type":"card_unit_ju_87_b2", "count":1},{"card_type":"card_unit_wespe_desert", "count":1},{"card_type":"card_event_gathering_storm", "count":1},{"card_type":"card_unit_me_bf_109_v2", "count":1},{"card_type":"card_unit_me_bf_109_v2", "count":1}]},"ai_deck":{"main_faction": "Soviet","ally_faction":"Soviet", "cards": [{"card_type":"card_location_ai_german_unlock3_tut", "count":1},{"card_type":"card_unit_554th_rifles", "count":1},{"card_type":"card_unit_95th_rifles_blank", "count":1},{"card_type":"card_unit_6th_naval_brigade", "count":1},{"card_type":"card_unit_bt_7", "count":1},{"card_type":"card_unit_554th_rifles", "count":1},{"card_type":"card_event_burning_sky", "count":1},{"card_type":"card_unit_i_16_ishak", "count":1},{"card_type":"card_unit_bt_7", "count":1},{"card_type":"card_unit_95th_rifles_blank", "count":1},{"card_type":"card_event_bloody_sickle", "count":1},{"card_type":"card_unit_321st_rifles", "count":1},{"card_type":"card_unit_89th_infantry", "count":1},{"card_type":"card_unit_t_34", "count":1},{"card_type":"card_unit_i_16_ishak", "count":1},{"card_type":"card_unit_t_70", "count":1},{"card_type":"card_unit_t_70", "count":1},{"card_type":"card_unit_84th_infantry", "count":1},{"card_type":"card_event_burning_sky", "count":1},{"card_type":"card_event_from_the_people", "count":1},{"card_type":"card_unit_2nd_motor", "count":1},{"card_type":"card_unit_2nd_motor", "count":1},{"card_type":"card_unit_t_34", "count":1},{"card_type":"card_event_bloody_sickle", "count":1},{"card_type":"card_event_from_the_people", "count":1},{"card_type":"card_unit_321st_rifles", "count":1},{"card_type":"card_unit_89th_infantry", "count":1},{"card_type":"card_unit_bt_7", "count":1},{"card_type":"card_event_critical_hit", "count":1},{"card_type":"card_unit_sturmovik", "count":1}]},"starting_side":"right","my_hand_count":"0","enemy_hand_count":"1","skip_mulligan":"true","player_hq":"card_location_berlin_unlock3_tut","ai_hq":"card_location_ai_german_unlock3_tut"}}

    r10 = requests.post(NewPlayerLobby,headers=headers,json=dataGerMan10,verify=False)

    NewPlayerMatchURL = "https://kards.live.1939api.com/matches/v2/"

    r11 = requests.get(NewPlayerMatchURL,headers=headers,verify=False)

    res=json.loads(r11.text)
    matchdata=res['match_and_starting_data']
    currentMatch=matchdata['match']
    NewPlayerMatchesID=currentMatch.get('match_id')
    #在哪边
    Ownside=currentMatch.get('action_side')

    NewPlayerMatchWinData = { "side": "", "action": "end-match", "value": {"winner_id": f"{playerID}","winner_side": f"{Ownside}","result": "Victory_DestroyHQ"}}

    r12 = requests.put(NewPlayerMatchesID,headers=headers,json=NewPlayerMatchWinData,verify=False)

    dataGerMan11 = {
	"action": "log-player-event",
	"value": "event.player.firebase;{\"event_name\": \"e_2025_third_german_training_match_finish\"}"
    }

    r13 = requests.put(NewPlayerMissionURL,headers=headers,json=dataGerMan11,verify=False)

    time.sleep(1)
    r1()
    time.sleep(1)
    r2()
    time.sleep(1)
    r3_1()
    time.sleep(1)
    r3()
    time.sleep(1)
    r4()
    time.sleep(1)
    r5()
    time.sleep(1)
    r6()
    time.sleep(1)
    r7()
    time.sleep(1)
    r8()
    time.sleep(1)
    r9()
    time.sleep(1)
    r10()
    time.sleep(1)
    r11()
    time.sleep(1)
    r12()
    time.sleep(1)
    r13()
    time.sleep(1)



def main():
    headers = {
        'Accept-Encoding': 'deflate, gzip',
        'Accept': 'application/json',
        'X-Api-Key': '1939-kards-5dcba429f:Kards 1.15.16724.Steam',
        'Drift-Api-Key': '1939-kards-5dcba429f:Kards 1.15.16724.Steam',
        'Authorization': cookie,
        'Content-Type': 'application/json',
        'User-Agent': 'kards/++UE5+Release-5.2-CL-26001984 Windows/10.0.19045.1.256.64bit'
        }
    #创建比赛地址
    #比赛ID
    CreateMatchesUrl="https://kards.live.1939api.com/lobbyplayers"
    data1 = { "player_id": playerID, "deck_id": deckID, "extra_data": "" }
    #获取比赛信息
    getMatchesInfoUrl="https://kards.live.1939api.com/matches/v2/"
    keepAliveUrl = f"https://kards.live.1939api.com/players/{playerID}/heartbeat"

    request_thread = threading.Thread(target=keep_alive, args=(keepAliveUrl,headers))
    request_thread.start()

    if isNewACount:
        NewPlayerMission(headers)
        print("新手任务已完成,请将isNewACount设置为False")
        sys.exit()
        


    while True:
        try:
            print("新一轮比赛已开始")
            #创建比赛
            r1=requests.post(CreateMatchesUrl,headers=headers,json=data1,verify=False,timeout=3)
            #print(r1.text)
            if "OK" in r1.text:
                #print(r1.text)
                time.sleep(1)
            #获取比赛信息
            getMatcheID(getMatchesInfoUrl,headers)
            #随机执行一些动作
            actionURL = f"https://kards.live.1939api.com/matches/v2/{matchesID}/actions"
            n = 1
            #pingUpload(actionURL,headers,n)

            XStartOfGame(actionURL,headers)

            #deckCollet(headers)

            XActionStartOfTurn(actionURL,headers)

            uploadPlayerPCInfo(headers)

            #for n in range(1,12):
            #    choiseCard(actionURL,headers,n)
            #choiseCard(actionURL,headers,n)

            GetMatchData(actionURL,headers,n)

            winOrLost = "win" if random.random() < 1 else "lost"
            if winOrLost == "win":
            #print("比赛中...")
            #Matchtime=random.randint(240,242)
            #自定义比赛进行时间，可直接秒赢，时间单位秒
                countdown(1)

            #time.sleep(600)

            #赢/输比赛
            #WinMatchesUrl=f"https://kards.live.1939api.com/matches/v2/{matchesID}"
            #otherSide = "left" if f"{Ownside}" == "right" else "right"
            #winSide = f"{Ownside}" if random.random() < 0.6 else f"{otherSide}"
                data2 = {
                    "side": "", 
                    "action": "end-match", 
                    "value": 
                            {
                    "winner_id": playerID,
                    "winner_side": f"{Ownside}",
                    "result": "Victory_DestroyHQ"
                            }
                }
                WinMatchesUrl=f"https://kards.live.1939api.com/matches/v2/{matchesID}"
                r3=requests.put(WinMatchesUrl,headers=headers,json=data2,verify=False)
                #print(r3.text)
                if "OK" in r3.text:
                    time.sleep(1)
                #查看比赛结果
                getMatchesEndInfoUrl=f"https://kards.live.1939api.com/matches/v2/{matchesID}/post"
                r4=requests.get(getMatchesEndInfoUrl,headers=headers,verify=False,timeout=3)
                #print(r4.text)
                if "winner" in r4.text:
                    print(r4.text)
                    print("比赛结束")
                    time.sleep(1)
            elif winOrLost == "lost":
                print("防检测输局[跳过]")
                time.sleep(1)

        except KeyboardInterrupt:
            #sys.exit(app.exec_())
            #driver.quit()
            #request_thread.join()
            print("程序已退出")
        except requests.exceptions.RequestException as e:
            #sys.exit(app.exec_())
            #driver.quit()
            #request_thread.join()
            print("发生错误:", e)
            time.sleep(1)
            pass

if __name__ == "__main__":
    main()