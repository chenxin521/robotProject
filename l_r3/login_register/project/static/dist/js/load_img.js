//向HTML添加元素（图片类型）
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

//显示图片
function showImg(input) {
    var file = input.files[0];
    console.log(file)
    console.log(input)
    var reader = new FileReader()
    time = get_time()
    reader.onload = function (e) {
        // document.getElementById('upload').src = e.target.result
        if($("#logout_username").text()=="")
            SohoExamle.Message.add(e.target.result, '匿名用户',time,'outgoing-message');
        else
            SohoExamle.Message.add(e.target.result, $("#logout_username").text(),time,'outgoing-message');
        a = e.target.result.substring( e.target.result.indexOf(",")+1);
        socket.emit('tran_img_event', {data: a,userId :'123',check:$("#logout_username").text()});
    }
    reader.readAsDataURL(file)
}

//以后可能会用到的一个函数
// function showImg(input) {
//     var file = input.files[0];
//     var url = window.URL.createObjectURL(file)
//     document.getElemtById('upload').src = url
// }

//获取当前时间函数
function get_time() {
    var now = new Date();
    var year = now.getFullYear(); //得到年份
    var month = now.getMonth();//得到月份
    var date = now.getDate();//得到日期
    var hour = now.getHours();//得到小时
    var minu = now.getMinutes();//得到分钟
    var sec = now.getSeconds();//得到秒
    month = month + 1;
    if (month < 10) month = "0" + month;
    if (date < 10) date = "0" + date;
    if (hour < 10) hour = "0" + hour;
    if (minu < 10) minu = "0" + minu;
    if (sec < 10) sec = "0" + sec;
    var time = "";
    time = year + "-" + month + "-" + date + "" + " " + hour + ":" + minu + ":" + sec;
    return time;
}