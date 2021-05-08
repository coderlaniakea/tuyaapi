"""
    注册用户
    用户登录 + 1分
    用户评论 + 2分
    用户分享 + 3分
    实时获取用户的分数在所有用户中的排名
"""

# 所有的用户
users = {
    # 'id1': {'score': 0},
    # 'id2': {'score': 0},
    # 'id3': {'score': 0},
}

# 每个分数对应的排名
score2rank = {
    # score: rank
    0: 1

    # 4: 1,
    # 2: 3,
    # 0: 4

    # 4: 1,
    # 3: 3,
    # 2: 4,
    # 0: 5

    # 4: 1,
    # 2: 3,
    # 0: 5
}

def register_user(user_id):
    if user_id in users.keys():
        print('该用户已注册.')

    users[user_id] = {'score': 0}


# 获取score2rank中小于且最接近score的值，返回其排名rank
def get_expect_val(score):
    expect_val = 0
    i = 1
    while True:
        if (score - i) in score2rank.keys():
            expect_val = score2rank[score - i]
            break
        i += 1
    return expect_val


def add_score(score):
    def decrator(func):
        def make_decator(user_id):
            # 更新用户对应的score值，并获取更新前后的值
            pre_score = users[user_id]['score']
            users[user_id]['score'] += score
            new_score = users[user_id]['score']

            """
            更新分数对应的排名 score2rank
            更新策略：
                1.判断score2rank中是否存在new_score
                    1.1如果score2rank存在new_score，那么new_score的排名就是当前值，
                        不用做任何操作
                    1.2如果score2rank不存在new_score，那么新增new_score，并且值为
                        score2rank更新前小于且最接近new_score的值
                
                2.当分数不为0时，获取分数处于pre_score的人数，用小于且最接近pre_score的
                    分数排名减去pre_score的排名
                    如果人数=1，则删除score2rank中的pre_score键

                3.pre_score和 new_score 之间的所有分数排名要 + 1（含下区间不含上区间）
            """
            
            

            # 2.
            if new_score not in score2rank.keys():
                # 获取score2rank更新前小于且最接近new_score的值
                new_expect_val = get_expect_val(new_score)
                # i = 0
                # while True:
                #     if (new_score - i) in score2rank.keys():
                #         expect_val = score2rank[new_score - i]
                #         break
                #     i += 1
                
                # 新增new_score
                score2rank[new_score] = new_expect_val
                pass

            # 1.
            if pre_score != 0:
                pre_expect_val = get_expect_val(pre_score)
                pre_score_count = pre_expect_val - score2rank[pre_score]
                if pre_score_count == 1:
                    del score2rank[pre_score]


            # 3.
            for k,v in score2rank.items():
                if k >= pre_score and k < new_score:
                    score2rank[k] += score
            
            func(user_id)
        return make_decator
    return decrator
    

@add_score(1)
def login(user_id):
    print('{}已登陆，加1分'.format(user_id))
    pass

@add_score(2)
def comment(user_id):
    print('{}已评论，加2分'.format(user_id))

@add_score(3)
def share(user_id):
    print('{}已分享，加3分'.format(user_id))


def show_now():
    print('当前分数排名情况为：')
    for score in sorted(score2rank.keys(), reverse=True):
        print('{}: {}'.format(score, score2rank[score]))
    print('每个人对应的分值：', users)
    print('')


if __name__ == '__main__':
    register_user('id1')
    register_user('id2')
    register_user('id3')

    print('初始化排名情况：', score2rank)
    print('每个人对应的分值：', users)
    print('')

    login('id1')
    show_now()
    # {
    #     1: 1,
    #     0: 2
    # }

    login('id1')
    show_now()
    # {
    #     2: 1,
    #     0: 2
    # }

    comment('id2')
    show_now()
    # {
    #     2: 1,
    #     0: 3 / 4
    # }

    comment('id1')
    show_now()
    # {
    #     4: 1,
    #     2: 2,
    #     0: 3
    # }

    share('id3')
    show_now()
    # {
    #     4: 1,
    #     3: 2,
    #     2: 3,
    #     0: 4
    # }


    # show_now()
    
    
    # {
    #     4: 1,
    #     3: 2,
    #     2: 3,
    #     0: 4
    # }