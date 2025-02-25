from app import application, socketio

if __name__ == '__main__':    
    socketio.run(application, host='0.0.0.0', port=5000, debug=True,allow_unsafe_werkzeug=True)