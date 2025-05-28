# my-first-python
#my first Python crawler
import  re
import requests
import urllib.request
def all_hero():
    url='https://lol.qq.com/biz/hero/champion.js'
    html=urllib.request.urlopen(url).read().decode('gbk')
    res=re.findall(r'"keys":(.*?),"data"',html,re.S|re.M)
    #print(res)
    dic_hero=eval(res[0])
    print(dic_hero)
    return dic_hero
def get_every_hero(dic):
    every_hero=[]       #此处dic代表装有所有英雄的字典
    url1='https://ossweb-img.qq.com/images/lol/web201310/skin/big'
    for key in dic:
        for i in range(20): #假设，每个英雄先抓取20个皮肤
            xuhao=str(i)
            if len(xuhao)==1:
                url=url1+key+'00'+xuhao+'.jpg'
            elif len(xuhao)==2:
                url = url1 + key + '0' + xuhao + '.jpg'
            #res=requests.get(url)
            #if res.status_code==200:
            every_hero.append(url)
            continue
    print(every_hero)#此列表还包含多余项（因为有的英雄没那么多皮肤）
    return  every_hero
def effectable_url(every_hero):  #真正有效的URL，没用到。。。。。  此处待修改
    effect_url=[]
    for u in range(len(every_hero)):
        url=every_hero[u]
        res=requests.get(url)
        if res.status_code!=200:
            continue
        else:
           effect_url.append(url)
    #print(effect_url)
    return effect_url
def heros_name(dic,every_hero):
    hero_name=[]  #存放英雄图片和皮肤文件名字的列表
    for value in dic.values():
        for i in range(20):
            hero_name.append(value+str(i+1)+'.jpg')
    #print(hero_name)
    return hero_name
def save_file(every_hero,hero_name,path):
    for i in range(len(every_hero)):
        res=requests.get(every_hero[i])
        if res.status_code==200:
            res=res.content
            file_name=hero_name[i]
            file_path=path+hero_name[i]
        else:
            continue
        with open(file_path,'wb') as f:
            f.write(res)
if __name__ == '__main__':
    dic=all_hero()
    every=get_every_hero(dic)
    #effectable_url(every)
    #heros_name(every,dic)
    hero_name=heros_name(dic,every)
    save_file(every,hero_name,'./lol_hero/')


