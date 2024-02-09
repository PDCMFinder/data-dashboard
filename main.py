from src.app import app

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8050')
    #app.run_server(debug=True)