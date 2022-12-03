// var roomPanel = document.createElement("div");
// roomPanel.setAttribute("id", "roomPanel");
// roomPanel.innerHTML = "<div class='roomPanelTitle'> 房间号: 11111 </div> <hr/>\
//                        <div class='roomPanelUser'> linsen </div>";
// document.body.parentNode.appendChild(roomPanel);


let hostUrl = 'http://127.0.0.1:5000/';
let socket = io.connect(hostUrl + 'dcenter');
let eleVideo = "";


// 先加载 再暂停
// 先暂停 等就绪 再一起播放


$(document).ready(function () {
    eleVideo = $(".bpx-player-video-area video")[0];

    $(eleVideo).on('play', function () {
        console.log("this video on play", eleVideo.currentTime)
    });

    $(eleVideo).on('canplay', function () {
        console.log('this video can play');
    });

    $(eleVideo).on('loadeddata', function () {
        console.log('this video loadeddata');
    });

    $(eleVideo).on('loadedmetadata', function () {
        console.log('this video loadedmetadata');
    });

    $(eleVideo).on('pause', function () {
        console.log('this video pause');
    });

    $(eleVideo).on('playing', function () {
        console.log('this video playing');
    });

    $(eleVideo).on('progress', function () {
        console.log('this video progress');
    });
})


chrome.runtime.onMessage.addListener((event, sender, callable) => {
    socket.emit('my_event', {data: "content tests"});
    eleVideo.currentTime = 60 * 5;
    eleVideo.pause();
    callable('content => popup')


    setTimeout(() => {
        eleVideo.play();
    }, 2000);
})

