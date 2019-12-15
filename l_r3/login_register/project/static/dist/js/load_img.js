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
    var reader = new FileReader();
    time = get_time();
    reader.onload = function (e) {

        if($("#logout_username").text()=="")
            SohoExamle.Message.add(e.target.result, '匿名用户',time,'outgoing-message');
        else
            SohoExamle.Message.add(e.target.result, $("#logout_username").text(),time,'outgoing-message');
        time2 = get_time();
        var special_ana = ["1.验证码识别 2.汉字识别(只能输入1或者2哦！)"];
        SohoExamle1.Message.add('小软棉',time2,special_ana[0], '');

        // $('form#broadcast').submit(function (event) {
        //     // time = get_time();
        //
        //     //HTML添加聊天内容
        //     if ($("#logout_username").text() == "")
        //         SohoExamle1.Message.add("匿名用户",time,$('#broadcast_data').val(),'outgoing-message');
        //     else
        //         SohoExamle1.Message.add($("#logout_username").text(),time,$('#broadcast_data').val(),'outgoing-message');
        //     $('#broadcast_data').val('');
        //     //获取人和机器人说的最后一句话
        //     var last_robot = "";
        //     var last_people = "";
        //     if($(".message-item:last").children('.message-content').length>0)
        //         last_robot=$(".message-item:last").children('.message-content').text();
        //     if($(".message-item, .outgoing-message").eq(-1).length>0) {
        //         last_people=$(".message-item, .outgoing-message").eq(-1).children('.message-content').text();
        //     }
        //     console.log(last_people);
        //     console.log(last_robot);
        //     //最后一句话肯定是人说的
        //     if(last_robot==last_people)
        //         last_robot=$(".message-item").eq(-2).children('.message-content').text();
        //     else if(last_people.replace(" ","")=="1" && special_ana.indexOf(last_robot) != -1)
        //         socket.emit('tran_img_event', {data: a, userId: '123', check: $("#logout_username").text()});
        //     else if(last_people.replace(" ","")=="2" && special_ana.indexOf(last_robot) != -1)
        //         socket.emit('hand_write_event', {data: a, userId: '123', check: $("#logout_username").text()});
        //     else
        //         SohoExamle1.Message.add('小软棉',time2,special_ana[0], '');
        //     // SohoExamle.Message.add(userId, 'outgoing-message');
        //     //     input.val('');
        //     // } else {
        //     //     input.focus();
        //     // }
        //     return false;
        // });



        // a = e.target.result.substring( e.target.result.indexOf(",")+1);
        // socket.emit('tran_img_event', {data: a,userId :'123',check:$("#logout_username").text()});
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

var SohoExamle1 = {
        Message: {
            add: function (username,time,message, type) {
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
                                <h5>` + (type == 'outgoing-message' ? username : '小软棉') + `</h5>
                                <div class="time">`+time+ ``+ (type == 'outgoing-message' ? '<i class="ti-check"></i>' : '') + `</div>
                            </div>
                        </div>
                        <div class="message-content">
                            ` + message + `
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