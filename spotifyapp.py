from flask import Flask,render_template,request,redirect,url_for
app = Flask(__name__)

SESSION_COOKIE_SECURE=False

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/create_playlist",methods=['GET','POST'])
def spo_playlist():
    if request.method=='POST':
        # print(request.method)
        import spotify
        spotify
        print('sss')
        return render_template('created_playlist.html'),'Creating Playlist'   
    else:
        return render_template('error.html')
    # return 

if __name__ == "__main__":
    app.run(debug=False)