class SocketManager{

  // https://socket.io/docs/client-api/#socket-on-eventName-callback
  reserved_events = [
    'connect', 
    'connect_error', 
    'connect_timeout',
    'error',
    'disconnect',
    'reconnect',
    'reconnect_attempt',
    'reconnecting',
    'reconnect_error',
    'reconnect_failed',
    'ping',
    'pong'
  ]

  constructor(url, token, handler){
    this.url = url;
    this.token = token;
    this.socket = io( url, {
      autoConnect: false,
      query:{token} 
    });
    handler(this);
  }

  connect(){
    this.socket.connect();
  }

  disconnect(){
    this.socket.disconnect();
  }

  addCustomEventHandler(event, cb){
    if(this.reserved_events.includes(event))throw 'RESERVED EVENT EXCEPTION'
    this.socket.on(event, cb);
  }

  addEventHandler(event, cb){
    if(!this.reserved_events.includes(event))throw 'UNKNOWN EVENT EXCEPTION';
    this.socket.on(event, cb)
  }

  emit(event, data){
    if(!this.socket.connected) throw 'SOCKET NOT CONNECTED EXCEPTION';
    return this.socket.emit(event, data);
  }

  //https://stackoverflow.com/questions/1479319/simplest-cleanest-way-to-implement-singleton-in-javascript
  static getInstance(url, token, handler){

    if(!SocketManager.instance){
      console.log('creating instance', url, token)
      SocketManager.instance = new SocketManager(url, token, handler);
    }

    return SocketManager.instance;
  }

}