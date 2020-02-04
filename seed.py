from models.base_model import db
from models.user import User
from models.post import Post

user_data = [
    {'username': 'liren', 'email': 'liren@email.com', 'first_name': 'Liren', 'last_name': 'Yeo',
        'password': 'qwe123', 'password_confirm': 'qwe123', 'description': 'Sometimes I enjoy spicy food'},
    {'username': 'jinqwen', 'email': 'jinqwen@email.com', 'first_name': 'Jinq Wen', 'last_name': 'Leong',
        'password': 'qwe123', 'password_confirm': 'qwe123', 'description': 'Hong Kong Egg Rolls is pretty good'},
    {'username': 'sandra', 'email': 'sandra@email.com', 'first_name': 'Sandra', 'password': 'qwe123',
        'password_confirm': 'qwe123', 'description': 'Ramuan: kulit popiah, serunding ayam & air'},
    {'username': 'matt', 'email': 'matt@email.com', 'first_name': 'Matt',
        'password': 'qwe123', 'password_confirm': 'qwe123'}
]

liren_posts = [
    "FPd8hahzBcA.jpg",
    "xOigCUcFdA8.jpg",
    "pXKiLKbaN90.jpg",
    "expMk3K5v_c.jpg",
    "NrAv3Vnyw48.jpg",
    "Fte3PHcIysk.jpg",
    "Yh6K2eTr_FY.jpg",
    "vcafGFqUH10.jpg"
]

jinqwen_posts = [
    "mmVa1ctda18.jpg",
    "tn85IH-sbhw.jpg",
    "Z2tvIDNtTqg.jpg",
    "MPOwVcXSVAI.jpg",
    "uNOJbxYF5LY.jpg",
    "MPCgyyIYwng.jpg"
]

sandra_posts = [
    "quyBQA6-6Ds.jpg",
    "VRB1LJoTZ6w.jpg",
    "O-rlY0RW9vU.jpg",
    "0jOarn3abtg.jpg",
    "SjNGSdZ5Og8.jpg",
    "Jy4-xk34q0s.jpg"
]

post_data = [
    [{'user_id': 1, 'image_path': f'liren/{img}'} for img in liren_posts],
    [{'user_id': 2, 'image_path': f'jinqwen/{img}'} for img in jinqwen_posts],
    [{'user_id': 3, 'image_path': f'sandra/{img}'} for img in sandra_posts]
]


def seed_users():
    try:
        for row in db.batch_commit(user_data, 100):
            User.create(**row)
    except:
        print('User Seed failed. Please check.')

    print('User Seed completed!')

def seed_posts():
    try:
        for post in post_data:
            for row in db.batch_commit(post, 100):
                Post.create(**row)
    except:
        print('Post Seed failed. Please check.')

    print('Post Seed completed!')
