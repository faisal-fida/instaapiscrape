import httpx
from rich import print
from statistics import mean

def human_format(num):
    if num > 5000:
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num = round(num / 1000.0, 2)
        return '{:.{}f}{}'.format(num, 2, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
    else:
        return num

async def get_userDetail(username):
    headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}
    base_url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    comments,likes = [],[]
    try:
        proxy = {"http://": "http://tyson.sproxy.pro:5555","https://": "http://tyson.sproxy.pro:5555",}
        async with httpx.AsyncClient(headers=headers,proxies=proxy) as client:
            res = await client.get(base_url)
            if res.status_code == 200:
                user_info = res.json()
                data = user_info['data']['user']
                profile_pic_url = data['profile_pic_url']
                followers = data['edge_followed_by']['count']
                posts = data['edge_owner_to_timeline_media']['edges']
                num = 1
                like = 0
                coment = 0 
                for x in posts[4:13]:
                    comments_c = x['node']['edge_media_to_comment']['count']
                    likes_c = x['node']['edge_liked_by']['count']
                    coment += comments_c
                    like += likes_c
                    num += 1
                    comments.append(comments_c)
                    likes.append(likes_c)

                total = like + coment
                if total>0:
                    try:
                        total = int(total/9)
                        total = float((total/followers)*95)
                        total = str(round(total,2)) + '%'
                    except:
                        pass
                else:
                    total = 0
                comments = human_format(round(mean(comments)))
                likes = human_format(round(mean(likes)))
        return {'Total Reach':total,'Followers':human_format(followers),'Comments':comments,'Likes':likes,'Profile':profile_pic_url,'Logic':'OK'}
        
    except Exception as e:
        return {'Total Reach':f'{e} User Not Found!','Followers':0,'Comments':0,'Likes':0,'Profile':'https://i.ibb.co/C9TV9rZ/a.png'}
        
