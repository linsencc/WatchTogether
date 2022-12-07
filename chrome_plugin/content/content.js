// var roomPanel = document.createElement("div");
// roomPanel.setAttribute("id", "roomPanel");
// roomPanel.innerHTML = "<div class='roomPanelTitle'> 房间号: 11111 </div> <hr/>\
//                        <div class='roomPanelUser'> linsen </div>";
// document.body.parentNode.appendChild(roomPanel);





let HostUrl = 'http://127.0.0.1:5000/';
let Socket = "";
let RoomId = "";
let Video = "";


// 先加载 再暂停 再一起播放
// 先暂停 等就绪 再一起播放 ✔


// todo 看看整个事件同步有没有必要改成单例模式
function createRoom(event){
    RoomId = event['data']['roomId'];
    Socket = io.connect(HostUrl + 'room');
    Video = $(".bpx-player-video-area video")[0]; // bilibili

    console.log('Socket', Socket);
    console.log('Video', Video);
    console.log('RoomId', RoomId);
}



class Manage {
    static instance;
    static socketNameSpace = 'Room';
    static cursor = 0;

    static socket;
    static roomId;
    static video;

    constructor(roomId) {
    }

    static getInstance() {
        return Manage.instance
    }

    static createInstance(roomId) {
        Manage.roomId = roomId;
        Manage.socket = io.connect(HostUrl + Manage.socketNameSpace);
        Manage.video = $(".bpx-player-video-area video")[0];            // bilibili

        Manage.instance = new Manage(roomId);
    }

    sendVideoProgress(){
        Manage.video.pause();

        let data = {
            curTime: Manage.video.currentTime,
            cursor: Manage.cursor,
        }

        Manage.socket.emit(data);
    }

    setVideoProgress(videoTime, cursor){
        Manage.video.currentTime = videoTime;
        Manage.video.pause();
        Manage.cursor = cursor;
    }

    playVideo(){
        Manage.video.play();
    }
}




chrome.runtime.onMessage.addListener((event, sender, callable) => {
    // Socket.emit('my_event', {data: "content tests"});
    // Video.currentTime = 60 * 5;
    // Video.pause();
    // callable('content => popup')

    console.log('event:', event);

    let action = event['action'];
    if(action === 'createRoom'){
        createRoom(event);
    }

    callable('content => popup')
})



$(document).ready(function () {

    $(Video).on('play', function () {
        console.log("this video on play", Video.currentTime)
    });

    $(Video).on('canplay', function () {
        console.log('this video can play');

    });

    $(Video).on('playing', function () {
        console.log('this video playing');
    });

    $(Video).on('pause', function () {
        console.log('this video pause');
    });
})




