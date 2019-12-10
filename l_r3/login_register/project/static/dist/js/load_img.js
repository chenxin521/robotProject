var SohoExamle = {
        Message: {
            add: function (message,username,time,type) {
                var chat_body = $('.layout .content .chat .chat-body');

                if (chat_body.length > 0) {
                    console.log(message);

                    type = type ? type : '';
                    message = message ? message : '收到（假的）';

                    $('.layout .content .chat .chat-body .messages').append(
                    `<div class="message-item ` + type + `">
                        <div class="message-avatar">
                            <figure class="avatar">
                                <img src="/static/dist/media/img/` + (type == 'outgoing-message' ? 'women_avatar5.jpg' : 'man_avatar3.jpg') + `" class="rounded-circle">
                            </figure>
                            <div>
                                <h5>` + (type == 'outgoing-message' ?username:'小软棉') + `</h5>
                                <div class="time">`+time+ ` ` + (type == 'outgoing-message' ? '<i class="ti-check"></i>' : '') + `</div>
                            </div>
                        </div>
                        <div class="message-content1">
                        <img id="img_size" src="`+message+`">
                           </div>
                        
                    </div>`);

                    setTimeout(function () {
                        chat_body.scrollTop(chat_body.get(0).scrollHeight, -1).niceScroll({
                            cursorcolor: 'rgba(66, 66, 66, 0.20)',
                            cursorwidth: "4px",
                            cursorborder: '0px'
                        }).resize();
                    }, 200);
                }
            }
        }
    };



function showImg(input) {
    var file = input.files[0];
    console.log(file)
    console.log(input)
    var reader = new FileReader()
    console.log(reader)
    // 图片读取成功回调函数
    reader.onload = function (e) {
        // document.getElementById('upload').src = e.target.result
        SohoExamle.Message.add(e.target.result, '传图片','2019-12-10 16:05:03 ','outgoing-message');
        a = e.target.result.substring( e.target.result.indexOf(",")+1);
        socket.emit('tran_img_event', {data: a});
    }

    reader.readAsDataURL(file)
}

// function showImg(input) {
//     var file = input.files[0];
//     var url = window.URL.createObjectURL(file)
//     document.getElemtById('upload').src = url
// }