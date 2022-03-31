from website import app

BASE = "https://rocky-escarpment-76791.herokuapp.com"

if __name__ == "__main__":
    app.run(host=BASE,port=5000,debug=True)
