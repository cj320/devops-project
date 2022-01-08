# ⚡ Report Instructions

## 💡 Overview

For your portfolio project, you will design and implement the back end for a web-based application with a database component.

**The final web-based application will:**

1. Implement a 2-tier architecture that includes a Postgres database and the web-based application that interacts with the database.
2. Use Docker Compose to define and manage the tiers.
3. Be pushed to an online repository on GitHub.
4. Be deployed to the cloud.

* We recommend you use either the Django or Flask frameworks to build your application.
* You can re-purpose your Flask-based portfolio project from the SQL course, or start a new project.
* If using Django, the application built during this week's workshop can serve as a starting point.
* It will not be required to develop a working front-end UI for your application unless you wish to do so, as front-end development is outside the scope of this course. You can use Insomnia or a similar application (such as Postman) to interact with the endpoints instead of a browser.

## 📝 Questions

1. What are the various features you would like your project to offer?

    <span style="color:forestgreen">One of the features of my project will be extracting posts from reddit via Reddit's PRAW Python library, then running queries to find the post with the highest vote count, and also displaying posts to end users via the project's API.</span>

2. What are the API endpoints that you would need to set up for each feature? List them along with the respective HTTP verb, endpoint URL, and any special details (query parameters, request bodies, headers).

    | HTTP VERB | END POINT URL                                    | DETAILS                                              |
    |-----------|--------------------------------------------------|------------------------------------------------------|
    | GET       | http://localhost/reddit-data:8000/users          | Display's all users from the DB                      |
    | GET       | http://localhost/reddit-data:8000/users:<id:int> | Display's username for a user in the DB              |
    | GET       | http://localhost/reddit-data:8000/posts:<id:int> | Displays all post from a user int the DB             |
    | GET       | http://localhost/reddit-data:8000/topscore       | Display's username of the user with the most upvotes |
    | GET       | http://localhost/reddit-data:8000/comments:<id:int>  | Displays all comments for post                   |

3. Provide a description of the database tables required for your application, including column names, data types, constraints, and foreign keys. Include your database name. You can optionally include an ER diagram.

**Database Tables:**

* Users Table

    ```python
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        user = db.Column(db.String(128), unique=True, nullable=False)
        # Get all posts for a given user
        posts = db.relationship('Post', backref='user', cascade="all,delete")
    ```

* Posts Table

    ```python
    class Post(db.Model):
        __tablename__ = 'posts'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        post_id = db.Column(db.String(6), nullable=False)
        title = db.Column(db.String, nullable=False)
        body = db.Column(db.String)
        url = db.Column(db.String)
        score = db.Column(db.Integer, nullable=False)
            subreddit = db.Column(db.String(20), nullable=False)
        total_comments = db.Column(db.Integer, nullable=False)
        created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
        )
        ser_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        user_data = db.relationship(
            'User', secondary=user_post_table,
            lazy='subquery',
            backref=db.backref('user_posts', lazy=True)
        )
        comments = db.relationship('Comment', backref='post', cascade="all,delete,delete-orphan
    ```

* Comments Table

    ```python
    class Comment(db.Model):
        __tablename__ = 'comments'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        comment = db.Column(db.String, nullable=True)
        p_id = db.Column(db.Integer, db.ForeignKey('posts.id'),nullable=False)
        comment_data = db.relationship(
            'Comment', secondary=post_comment_table,
            backref=db.backref('post_comments', lazy=True, cascade="all,delete")
        )
    ```

* Association Tables

    ```python
        user_post_table = db.Table(
        'user_posts',
        db.Column(
            'user_id', db.Integer,
            db.ForeignKey('users.id'),
            primary_key=True
        ),

        db.Column(
            'post_id',db.Integer,
            db.ForeignKey('posts.id'),
            primary_key=True
        ),

        db.Column(
            'created_at', db.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False
        )
    )

    post_comment_table = db.Table(
        'post_comments',
        db.Column(
            'post_id', db.Integer,
            db.ForeignKey('posts.id'),
            primary_key=True
        ),

        db.Column(
            'comment_id',db.Integer,
            db.ForeignKey('comments.id'),
            primary_key=True
        ),

        db.Column(
            'created_at', db.DateTime,
            default=datetime.datetime.utcnow,
            nullable=False
            )
        )
    ```

### 💡 Starter Code

**Get Content Function:**

```python
    def creds():
        global reddit
        credentials = '.secrets.json'

        with open(credentials, 'r') as f:
        creds = json.load(f)
        reddit = praw.Reddit(client_id=creds['client_id'],
                    client_secret=creds['client_secret'],
                    user_agent=creds['user_agent'],
                    redirect_uri=creds['redirect_uri'],
                    refresh_token=creds['refresh_token'])
        return reddit

    def get_stats(sub):
        creds()
        sub = reddit.subreddit(sub).hot(limit=15)
        stats = {
            "subreddit": [],
            "user": [],
            "id": [],
            "title": [],
            "body": [],
            "url": [],
            "score": [],
            "comments": [],
            "created": [],
            "comment_data": []
        }
        for post in sub:
            post_comments = []
            com = reddit.submission(id=post.id)

            for top_level_comment in com.comments:
                com.comments.replace_more(limit=16, threshold=10)
                post_comments.append(top_level_comment.body)

            stats['subreddit'].append(str(post.subreddit))
            stats["user"].append(str(post.author))
            stats["id"].append(post.id)
            stats["title"].append(str(post.title))
            stats["body"].append(str(post.selftext))
            stats["url"].append(str(post.url))
            stats["score"].append(int(post.score))
            stats["comments"].append(int(post.num_comments))
            stats["created"].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(post.created_utc)))
            stats["comment_data"].append(post_comments)
        return stats
```

**Seeding the Database:**

```python
    def main():
        """Main driver function"""
        app = create_app()
        app.app_context().push()

        while True:
            sub = input("Please enter the name of a subreddit: ")
            if content.val_subreddit(sub):
                break
        data = content.get_stats(sub)
        df =  pd.DataFrame(data)
        data_list = df.to_dict('records')
        data = []

        for dic in data_list:
            name_validation = User.query.filter_by(user=dic['user']).first()
            if not name_validation:
                user_table = {
                    "user": dic['user']
                }
                user = User(**user_table)
                db.session.add(user)
                db.session.commit()
            uid = User.query.filter_by(user=dic['user']).first()

            post_table = {
                "post_id": dic['id'],
                "title": dic['title'],
                "body": dic['body'],
                "url": dic['url'],
                "score": dic['score'],
                "subreddit": dic['subreddit'],
                "total_comments": dic['comments'],
                "created_at": dic['created'],
                "user_id": uid.id
            }
            post = Post(**post_table)
            db.session.add(post)
            db.session.commit()

            pid = Post.query.filter_by(post_id=dic['id']).first()
            for comment in dic['comment_data']:
                comment_table = { "comment": comment, "p_id": pid.id}
                c = Comment(**comment_table)
                db.session.add(c)
            db.session.commit()

    if __name__ == '__main__':
        main()
```
