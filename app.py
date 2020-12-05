import mariadb
from flask import Flask, request, Response
import json
import dbcreds
from flask_cors import CORS
import jwt
import datetime

   
app = Flask(__name__)
app.config['SECRET_KEY'] = 'youarelogedin'
CORS(app)



@app.route("/api/users",methods=['GET','POST','PATCH','DELETE'])
def userendpoint():
    if request.method == 'GET':
        conn = None
        cursor = None
        users = None
        user_id = request.args.get("userId")
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            if user_id:
                cursor.execute("SELECT id,email,username,bio,birthdate FROM user WHERE id=?",[user_id])
                user = cursor.fetchone()
            
            else:    
                cursor.execute("SELECT *FROM user")
                users = cursor.fetchall()
                allUser = []
            
                for user in users:
                    allUser.append({
                        "userId":user[0],
                        "email":user[1],
                        "username":user[3],
                        "bio":user[4],
                        "birthdate":user[5]


                    })


        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(users != None):
                
                return Response(json.dumps(allUser, default=str),mimetype="application/json", status=200) 
            else:
                return Response("something went wrong!",mimetype="application/json", status=500)
    elif request.method == 'POST':
        conn = None
        cursor = None
        user_email = request.json.get("email")
        user_username = request.json.get("username")
        user_password = request.json.get("password")
        user_bio = request.json.get("bio")
        user_birthdate = request.json.get("birthdate")
        if user_username == user_password:
            return Response("password shouldnt match with username",mimetype="text/html", status=501) 
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE email=?",[user_email])
            user = cursor.fetchone()
            print(user)
            if user:
                return Response("user with that email already exist",mimetype="text/html", status=501) 
        
        except Exception as error:
            print("something went wrong: ")
            print(error)    
        
        
        
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user(email,username,password,bio,birthdate) VALUES(?,?,?,?,?)",[user_email,user_username,user_password,user_bio,user_birthdate])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("you have created a user",mimetype="text/html", status=201) 
            else:
                return Response("we are not able to create a user for u",mimetype="text/html", status=501) 

    elif request.method == 'PATCH':
        conn = None
        cursor = None
        user_loginToken = request.json.get("loginToken")
        user_email = request.json.get("email")
        user_username = request.json.get("username")
        user_password = request.json.get("password")
        user_bio = request.json.get("bio")
        user_birthdate = request.json.get("birthdate")

        decoded = jwt.decode(user_loginToken,app.config['SECRET_KEY'])
        user_id= decoded['userId']

        
        
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            if user_bio !="" and user_bio != None:
                cursor.execute("UPDATE user SET bio=? WHERE id=?",[user_bio,user_id])
            conn.commit()    
            if user_email !="" and user_email != None:
                cursor.execute("UPDATE user SET email=? WHERE id=?",[user_email,user_id])
            conn.commit()
            if user_username !="" and user_username != None:
                cursor.execute("UPDATE user SET username=? WHERE id=?",[user_username,user_id])
            conn.commit()
            if user_bio !="" and user_password != None:
                cursor.execute("UPDATE user SET password=? WHERE id=?",[user_password,user_id])
            conn.commit()
            if user_bio !="" and user_birthdate != None:
                cursor.execute("UPDATE user SET birthdate=? WHERE id=?",[user_birthdate,user_id])
            conn.commit()               

            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("user has been updated",mimetype="text/html", status=204) 
            else:
                return Response("you have no permission to update this user",mimetype="text/html", status=500) 

    elif request.method == 'DELETE':
        conn = None
        cursor = None
        
        user_loginToken = request.json.get("loginToken")
        user_password = request.json.get("password")
        decoded = jwt.decode(user_loginToken,app.config['SECRET_KEY'])
        user_id = decoded["userId"]

        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM user WHERE id=? AND password=?",[user_id,user_password])
            conn.commit()    

            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("user DELETED",mimetype="text/html", status=204) 
            else:
                return Response("no permission to delete this user",mimetype="text/html", status=500)


@app.route("/api/login",methods=['POST','DELETE'])
def login():
    auth = request.authorization
    if request.method == 'POST':
    
    
        conn = None
        cursor = None
        rows = None
        user_email = request.json.get("email")
        user_password = request.json.get("password")
        
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE email=? AND password=?",[user_email,user_password])
            user = cursor.fetchone()
            print(user)
        
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        loginToken = jwt.encode({'username':user[3],'user_email':user_email,'userId':user[0], 'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=30)}, app.config['SECRET_KEY']).decode("UTF-8")
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user_session(user_id,loginToken) VALUES(?,?)",[user[0],loginToken])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return_data = {
                    "userId": user[0],
                    "email": user_email,
                    "username":user[3],
                    "bio":user[4],
                    "birthdate":user[5],
                    "loginToken": loginToken
                }
                return Response(json.dumps(return_data, default=str),mimetype="text/html", status=201) 
                
            else:
                return Response("we are not able to save the token",mimetype="text/html", status=501) 



        
            
         
    if request.method == 'DELETE':
    
    
        conn = None
        cursor = None
        user_loginToken = request.json.get("loginToken")
    
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_session WHERE loginToken=?",[user_loginToken])
            conn.commit()
            rows = cursor.rowcount
        
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows != None):
    
                return Response("you are signed out",mimetype="text/html", status=201) 
            else:
                return Response("something went wrong",mimetype="text/html", status=501)


@app.route("/api/follows",methods=['GET','POST','DELETE'])
def follow():
    if request.method == 'GET':
        conn = None
        cursor = None
        follows = None
        user_id = request.args.get("userId")
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            cursor.execute("SELECT user.id, email, username, bio, birthdate FROM follow INNER JOIN `user` ON followed_user_id=user.id  WHERE user_id=?",[user_id])
            follows = cursor.fetchall()
            allFollows = []
            for follow in follows:
                allFollows.append({
                     "userId":follow[0],
                     "email":follow[1],
                     "username":follow[2],
                     "bio":follow[3],
                     "birthdate":follow[4]
                })

        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(follows != None):
                return Response(json.dumps(allFollows, default=str),mimetype="application/json", status=200) 
            else:
                return Response("you dont follow anyone!",mimetype="application/json", status=500)
    elif request.method == 'POST':
        conn = None
        cursor = None
        user_loginToken = request.json.get("loginToken")
        follow_followed_user_id = request.json.get("followId")
        decoded = jwt.decode(user_loginToken,app.config['SECRET_KEY'])
        user_id = decoded['userId']
        print(decoded)
    
        
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO follow(user_id,followed_user_id) VALUES(?,?)",[user_id,follow_followed_user_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("you strated to follow a user",mimetype="text/html", status=201) 
            else:
                return Response("couldnt establish a fellow relationship",mimetype="text/html", status=501) 

    
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        
        user_loginToken = request.json.get("loginToken")
        follow_followed_user_id = request.json.get("followId")
        decoded = jwt.decode(user_loginToken,app.config['SECRET_KEY'])
        user_id = decoded['userId']
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM follow WHERE user_id=? AND followed_user_id=?",[user_id,follow_followed_user_id])
            conn.commit()    

            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("stoped following a user",mimetype="text/html", status=204) 
            else:
                return Response("couldnt stop following this user",mimetype="text/html", status=500) 
@app.route("/api/followers",methods=['GET'])
def followers():
    if request.method == 'GET':
        conn = None
        cursor = None
        followers = None
        
        user_id = request.args.get('userId')
        
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            cursor.execute("SELECT user.id, email, username, bio, birthdate FROM follow INNER JOIN user ON user_id=user.id  WHERE followed_user_id=?",[user_id])
            followers = cursor.fetchall()
            allFollowers = []
            for follower in followers:
                allFollowers.append({
                     "userId":follower[0],
                     "email":follower[1],
                     "username":follower[2],
                     "bio":follower[3],
                     "birthdate":follower[4]
                })

        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(followers != None):
                return Response(json.dumps(allFollowers, default=str),mimetype="application/json", status=200) 
            else:
                return Response("you dont have any follower!",mimetype="application/json", status=500)








@app.route("/api/tweets",methods=['GET','POST','PATCH','DELETE'])
def tweets():
    if request.method == 'GET':
        conn = None
        cursor = None
        tweets = None
        user_id = request.args.get("userId")
        
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            if user_id != None:  
                #get tweets for a specific user
                cursor.execute("SELECT tweets.id,user_id,username,content,created_at FROM tweets INNER JOIN user ON tweets.user_id=user.id WHERE tweets.user_id=?",[user_id])

            else:
                #all tweets
                cursor.execute("SELECT tweets.id,user_id,username,content,created_at FROM tweets INNER JOIN user ON tweets.user_id=user.id")
            tweets = cursor.fetchall()
            allTweets = []
            
            
            for tweet in tweets:
                allTweets.append({
                "tweetId":tweet[0],
                "userId":tweet[1],
                "username":tweet[2],
                "content":tweet[3],
                "createdAt":tweet[4]
                })
            
            
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(tweets != None):
                return Response(json.dumps(allTweets, default=str),mimetype="application/json", status=200) 
                

            else:
                return Response("something went wrong!",mimetype="application/json", status=500)
    elif request.method == 'POST':
        conn = None
        cursor = None
        tweets_content = request.json.get("content")
        user_loginToken = request.json.get("loginToken")
        decoded = jwt.decode(user_loginToken, app.config["SECRET_KEY"])
        user_id = decoded['userId']
        username = decoded["username"] 
        
        
        
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tweets(user_id,content) VALUES(?,?)",[user_id,tweets_content])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("you made a tweet",mimetype="text/html", status=201) 
            else:
                return Response("couldnt make a tweet for u",mimetype="text/html", status=501) 

    elif request.method == 'PATCH':
        conn = None
        cursor = None
        tweets_content = request.json.get("content")
        user_loginToken = request.json.get("loginToken")
        decoded = jwt.decode(user_loginToken, app.config["SECRET_KEY"])
        user_id = decoded['userId']
        tweet_id = request.json.get("tweetId")
        
        
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            if tweets_content !="" and tweets_content != None:
                cursor.execute("UPDATE tweets SET content=? WHERE id=? AND user_id=?",[tweets_content,tweet_id,user_id])
            conn.commit()    

            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("tweet has been updated",mimetype="text/html", status=204) 
            else:
                return Response("you have no permission to update this post",mimetype="text/html", status=500) 

    elif request.method == 'DELETE':
        conn = None
        cursor = None
        
        user_loginToken = request.json.get("loginToken")
        decoded = jwt.decode(user_loginToken, app.config["SECRET_KEY"])
        user_id = decoded['userId']
        tweet_id = request.json.get("tweetId")
        
        
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM tweets WHERE id=? AND user_id=?",[tweet_id,user_id])
            conn.commit()    

            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("tweet DELETED",mimetype="text/html", status=204) 
            else:
                return Response("something went wrong",mimetype="text/html", status=500)



@app.route("/api/tweet-likes",methods=['GET','POST','DELETE'])
def tweet_like():
    if request.method == 'GET':
        conn = None
        cursor = None
        tweet_likes = None
        tweet_like_tweet_id = request.args.get("tweetId")
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            if tweet_like_tweet_id:
                #get tweets for a specific user
                cursor.execute("SELECT user_id, tweet_id, username FROM tweet_like INNER JOIN user ON user.id = tweet_like.user_id WHERE tweet_id=? ",[tweet_like_tweet_id])

            else:
                
                cursor.execute("SELECT user_id, tweet_id, username FROM tweet_like INNER JOIN user ON user.id = tweet_like.user_id")
            
            
            tweet_likes = cursor.fetchall()
            allTweetLikes = []
            for tweet_like in tweet_likes:
                allTweetLikes.append({
                    "userId":tweet_like[0],
                    "tweetId":tweet_like[1],
                    "username":tweet_like[2]



                })
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(tweet_likes != None):
                return Response(json.dumps(allTweetLikes, default=str),mimetype="application/json", status=200) 
            else:
                return Response("this tweets has no likes!",mimetype="application/json", status=500)
    elif request.method == 'POST':
        conn = None
        cursor = None
        user_loginToken = request.json.get("loginToken")
        tweet_id = request.json.get("tweetId")
        decoded = jwt.decode(user_loginToken,app.config['SECRET_KEY'])
        user_id = decoded['userId']
        
        print(decoded)
        
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tweet_like(user_id,tweet_id) VALUES(?,?)",[user_id,tweet_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("you yave liked a tweet",mimetype="text/html", status=201) 
            else:
                return Response("couldnt like this tweet",mimetype="text/html", status=501) 

    
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        
        user_loginToken = request.json.get("loginToken")
        tweet_like_tweet_id = request.json.get("tweetId")
        decoded = jwt.decode(user_loginToken,app.config['SECRET_KEY'])
        user_id = decoded['userId']
        
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM tweet_like WHERE user_id=? AND tweet_id=?",[user_id,tweet_like_tweet_id])
            conn.commit()    

            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("dont like this tweet anymore",mimetype="text/html", status=204) 
            else:
                return Response("couldnt unlike this tweet",mimetype="text/html", status=500) 





@app.route("/api/comments",methods=['GET','POST','PATCH','DELETE'])
def comments():
    if request.method == 'GET':
        conn = None
        cursor = None
        comments = None
        tweet_id = request.args.get("tweetId")
        
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            if tweet_id:
                #get tweets for a specific user
                cursor.execute("SELECT comment.id,tweet_id,user_id,username,content,created_at FROM comment INNER JOIN user ON comment.user_id=user.id WHERE tweet_id=?",[tweet_id])

            else:
                #all tweets
                cursor.execute("SELECT comment.id,tweet_id,user_id,username,content,created_at FROM comment INNER JOIN user ON comment.user_id=user.id")
            comments = cursor.fetchall()
            allComments = []
            
            
            for comment in comments:
                allComments.append({
                "commentId":comment[0],
                "userId":comment[2],
                "tweetId":comment[1],
                "username":comment[3],
                "content":comment[4],
                "createdAt":comment[5]
                })
            
            
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(comments != None):
                return Response(json.dumps(allComments, default=str),mimetype="application/json", status=200) 
                

            else:
                return Response("something went wrong!",mimetype="application/json", status=500)
    elif request.method == 'POST':
        conn = None
        cursor = None
        comment_content = request.json.get("content")
        user_loginToken = request.json.get("loginToken")
        decoded = jwt.decode(user_loginToken, app.config["SECRET_KEY"])
        user_id = decoded['userId']
        username = decoded["username"]
        tweet_id = request.json.get("tweetId")
        print(user_id) 
        
        
        
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO comment(user_id,tweet_id,content) VALUES(?,?,?)",[user_id,tweet_id,comment_content])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("you made a comment",mimetype="text/html", status=201) 
            else:
                return Response("couldnt make a tweet for u",mimetype="text/html", status=501) 

    elif request.method == 'PATCH':
        conn = None
        cursor = None
        comment_content = request.json.get("content")
        user_loginToken = request.json.get("loginToken")
        decoded = jwt.decode(user_loginToken, app.config["SECRET_KEY"])
        user_id = decoded['userId']
        comment_id = request.json.get("commentId")
        
        
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            if comment_content !="" and comment_content != None:
                cursor.execute("UPDATE comment SET content=? WHERE id=? AND user_id=?",[comment_content,comment_id,user_id])
            conn.commit()    

            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("comment has been updated",mimetype="text/html", status=204) 
            else:
                return Response("you have no permission to update this post",mimetype="text/html", status=500) 

    elif request.method == 'DELETE':
        conn = None
        cursor = None
        
        user_loginToken = request.json.get("loginToken")
        decoded = jwt.decode(user_loginToken, app.config["SECRET_KEY"])
        user_id = decoded['userId']
        comment_id = request.json.get("commentId")
        
        
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM comment WHERE id=? AND user_id=?",[comment_id,user_id])
            conn.commit()    

            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("comment DELETED",mimetype="text/html", status=204) 
            else:
                return Response("something went wrong",mimetype="text/html", status=500)


@app.route("/api/comment-likes",methods=['GET','POST','DELETE'])
def comment_like():
    if request.method == 'GET':
        conn = None
        cursor = None
        comment_likes = None
        comment_id = request.args.get("commentId")
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            if comment_id:
                #get tweets for a specific user
                cursor.execute("SELECT user_id, comment_id, username FROM comment_like INNER JOIN user ON user.id = comment_like.user_id WHERE comment_id=? ",[comment_id])

            else:
                
                cursor.execute("SELECT user_id, comment_id, username FROM comment_like INNER JOIN user ON user.id = comment_like.user_id")
            
            
            comment_likes = cursor.fetchall()
            allCommentLikes =[]
            for comment_like in comment_likes:
                allCommentLikes.append({
                    "commentId":comment_like[0],
                    "userId":comment_like[1],
                    "username":comment_like[2]



                })
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(tweet_like != None):
                return Response(json.dumps(allCommentLikes, default=str),mimetype="application/json", status=200) 
            else:
                return Response("this comment has no likes!",mimetype="application/json", status=500)
    elif request.method == 'POST':
        conn = None
        cursor = None
        user_loginToken = request.json.get("loginToken")
        comment_id = request.json.get("commentId")
        decoded = jwt.decode(user_loginToken,app.config['SECRET_KEY'])
        user_id = decoded['userId']
        
        print(decoded)
        
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO comment_like(user_id,comment_id) VALUES(?,?)",[user_id,comment_id])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("you yave liked a comment",mimetype="text/html", status=201) 
            else:
                return Response("couldnt like this comment",mimetype="text/html", status=501) 

    
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        
        user_loginToken = request.json.get("loginToken")
        comment_id = request.json.get("commentId")
        decoded = jwt.decode(user_loginToken,app.config['SECRET_KEY'])
        user_id = decoded['userId']
        
        rows = None
        try:
            conn = mariadb.connect(user=dbcreds.user,password=dbcreds.password,host=dbcreds.host,database=dbcreds.database,port=dbcreds.port)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM comment_like WHERE user_id=? AND comment_id=?",[user_id,comment_id])
            conn.commit()    

            rows = cursor.rowcount
        except Exception as error:
            print("something went wrong: ")
            print(error)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("dont like this comment anymore",mimetype="text/html", status=204) 
            else:
                return Response("couldnt unlike this comment",mimetype="text/html", status=500)                 
