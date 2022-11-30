let hostUrl = 'http://127.0.0.1:5000/';
let loading = $('.container.loading');
let sign_in = $('.container.sign-in');
let content = $('.container.content');


document.addEventListener('DOMContentLoaded', async () => {
    console.log('popup DOMContentLoaded done');
    let url = hostUrl + 'profile';

    // $.post(url, function(data,status){
    //     if(status === 'success' && data['code'] === 0){
    //         loading.css('display', 'none');
    //         content.css('display', 'flex');
    //         renderContent(data);
    //     }else{
    //         loading.css('display', 'none');
    //         sign_in.css('display', 'flex');
    //     }
    // });

    $.ajax({
        url: url,
        type: 'POST',
        xhrFields: {withCredentials: true},
        crossDomain: true,
        success: function(data,status){
            if(status === 'success' && data['code'] === 0){
                loading.css('display', 'none');
                content.css('display', 'flex');
                renderContent(data);
            }else{
                loading.css('display', 'none');
                sign_in.css('display', 'flex');
            }
        }
    });
});


$('#sign-in').click(() => {
    let url = hostUrl + 'login';
    window.open(url);
})

$('#sign-in-test').click(() => {
    let url = hostUrl + 'test';

    $.post(url, function(data,status){
        alert(JSON.stringify(data))
    });
})


$('#sign-out').click(() => {
    let url = hostUrl + 'logout';
    $.post(url, function(data,status){
        if(status === 'success' && data['code'] === 0){
            loading.css('display', 'none');
            content.css('display', 'none');
            sign_in.css('display', 'flex');
        }
    });
})


function renderContent(data){
    let nickname = data['data']['nickname'];
    $('.container.content .profile .user-name').text(nickname);
}