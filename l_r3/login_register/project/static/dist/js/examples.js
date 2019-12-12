(function () {
    //动态添加聊天内容函数
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
    setTimeout(function () {
        $('#pageTour').modal('show');
    }, 1000);
    //聊天对话
    $(document).ready(function () {
        namespace = '/test';
        var socket = io(namespace);
        userId = '123';
        time = get_time()
        $('.time').text(time);
        //提交聊天内容触发函数
        $('form#broadcast').submit(function (event) {
            time = get_time()
            //触发图灵回复
            socket.emit('my_broadcast_event', {
                data: $('#broadcast_data').val(),
                userId: '123',
                check: $("#logout_username").text()
            });
            //HTML添加聊天内容
            if ($("#logout_username").text() == "")
                SohoExamle.Message.add($('#broadcast_data').val(), "匿名用户", time, 'outgoing-message');
            else
                SohoExamle.Message.add($('#broadcast_data').val(), $("#logout_username").text(), time, 'outgoing-message');
            $('#broadcast_data').val('');
            // SohoExamle.Message.add(userId, 'outgoing-message');
            //     input.val('');
            // } else {
            //     input.focus();
            // }
            return false;
        });
        //获取图灵回复内容后将内容添加到HTML
        socket.on('my_response', function(msg, cb) {
            SohoExamle.Message.add(msg.data,msg.username,msg.time2, '');//回答
            if (cb)
                cb();
        });

    });
// outgoing-message'
    // $(document).on('submit', '.layout .content .chat .chat-footer form', function (e) {
    //     e.preventDefault();
    //     var input = $(this).find('input[type=text]');
    //     var message = input.val();
    //     message = $.trim(message);
    //     if (message) {
    //         SohoExamle.Message.add(message, '');
    //         input.val('');
    //         SohoExamle.Message.add();
    //     } else {
    //         input.focus();
    //     }
    // });
    $(document).on('click', '.layout .content .sidebar-group .sidebar .list-group-item', function () {
        if (jQuery.browser.mobile) {
            $(this).closest('.sidebar-group').removeClass('mobile-open');
        }
    });
    $(document).on('click', '.layout .content .sidebar-group .sidebar .list-group-item', function () {
        if (jQuery.browser.mobile) {
            $(this).closest('.sidebar-group').removeClass('mobile-open');
        }
    });
})();

namespace = '/test';
var socket = io(namespace);

//登录按钮触发函数（向python提交数据）
$(".my_btn_login").click(function () {
        socket.emit('my_login_event', {username: $('#login_name').val(),password :$('#login_pass').val()});

});

//登录成功状态函数
socket.on('login_success_event', function(msg, cb) {
    $("#login_backtip").text(msg.data);
    setTimeout(function () {
        $(huikuang).css("display","none");
    }, 1000);
    var name = $('#login_name').val();
    $("#cross4_out").text(name.slice(0,1));
    $("#cross4_out").css("display","block");
    $("#cross3").css("display","none");
    $("#logout_username").text(name);
    if (cb)
    cb();
});

//登录失败提醒
socket.on('login_backtips_event', function(msg, cb) {
    $("#login_backtip").text(msg.data);
    if (cb)
    cb();
});

//注册按钮触发函数（向python提交数据）
$('#my_btn_register').click(function () {
    socket.emit('my_register_event', {username: $('#register_name').val(),studentid: $('#register_id').val(),
            email: $('#register_email').val(),password :$('#register_pass').val(),lastpass: $('#last_pass').val()});
});

//注册成功触发函数
socket.on('register_success_event', function(msg, cb) {
    $("#register_tip").text(msg.data);
    setTimeout(function () {
        $(register).css("display","none");
    }, 1000);
    if (cb)
    cb();
});

//注册失败触发函数
socket.on('register_tips_event', function(msg, cb) {
    $("#register_tip").text(msg.data);
    if (cb)
    cb();
});

//退出登录触发函数
$("#my_btn_out").click(function () {
        $(logout).css("display","none");
        $("#login_backtip").text("");
        $("#cross3").css("display","block");
        $("#cross4_out").text("");
        $("#cross4_out").css("display","none");
        time=get_time()
        $('.layout .content .chat .chat-body .messages').html(
                    `<div class="message-item ">
                        <div class="message-avatar">
                            <figure class="avatar">
                                <img src="/static/dist/media/img/man_avatar3.jpg" class="rounded-circle" alt="image">
                            </figure>
                            <div>
                                <h5>小软棉</h5>
                                <div class="time">`+time+ `</div>
                            </div>
                        </div>
                        <div class="message-content">
                                欢迎来到你的私人小空间！小软棉已经等候您好久啦，快来和我聊天吧~ 😃
                        </div>                       
                    </div>`);
});

//退出登录时点击空白处弹框消失
var cross4_out=document.getElementById("cross4_out");
var logout=document.getElementsByClassName("logout")[0];
cross4_out.onclick=function(){
    $(logout).css("z-index",0);
    $(logout).css("display","block");
}
$('.logout').on('click',function(event){
    //取消事件冒泡
    event.stopPropagation();
    $(logout).css("display","none");
});
$('.logout .form-membership2').click(function(event){
         event.stopPropagation();
  });

//登录时点击空白处弹框消失
var cross3=document.getElementById("cross3");
var huikuang=document.getElementsByClassName("huikuang")[0];
cross3.onclick=function(){
    $(huikuang).css("z-index",0);
    $(huikuang).css("display","block");
}
$('.huikuang').on('click',function(event){
    //取消事件冒泡
    event.stopPropagation();
    $(huikuang).css("display","none");
});
$('.huikuang .form-membership2').click(function(event){
         event.stopPropagation();
  });

//注册时点击空白处弹框消失
var toregister=document.getElementById("toregister");
console.log(toregister)
var register=document.getElementsByClassName("register")[0];
toregister.onclick=function(){
    $(register).css("z-index",0);
    $(register).css("display","block");
}
$('.register').on('click',function(event){
    //取消事件冒泡
    event.stopPropagation();
    $(register).css("display","none");
});
$('.register .form-membership0').click(function(event){
         event.stopPropagation();
  });

//register-backto-sign
var backsign=document.getElementById("backsign");
var huikuang=document.getElementsByClassName("huikuang")[0];
backsign.onclick=function(){
    $(register).css("display","none");
    $(huikuang).css("z-index",0);
    $(huikuang).css("display","block");
}
$('.huikuang').on('click',function(event){
    //取消事件冒泡
    event.stopPropagation();
    $(huikuang).css("display","none");
});
$('.huikuang .form-membership2').click(function(event){
         event.stopPropagation();
  });

//手机版点击出现简介框
var ins = document.getElementsByClassName("ins")[0];
var intr  = document.getElementsByClassName("introduction")[0];
var tag=1
ins.onclick=function (){
    if(tag==1){
        intr.style.display="block";
        tag=0
    }
}
intr.onclick=function(){
    if(tag==0){
        intr.style.display="none";
        tag=1
    }
}

//内容滚动
var ul = document.getElementsByClassName("roll-content");
function show() {
    for(var i=0;i<ul.length;i++)
    {
        var top = ul[i].offsetTop - 1; //获取left值
        ul[i].style.top = top + "px"; //设置left值

        //走完一半再返回
        if (-1 * ul[i].offsetTop >= ul[i].offsetHeight / 2) {
            ul[i].style.top = 0;
        }
    }

}
var t = setInterval(show, 20);

// li添加鼠标移入移出事件
 var li = document.getElementsByClassName("roll-content");
 var lis=li[1].children
for (var i = 0; i < lis.length; i++) {
        //移出事件
    lis[i].onmouseout = function () {
        t = setInterval(show, 20);
    };
        //移入事件
    lis[i].onmouseover = function () {
        clearInterval(t);
    };
}
/*********简介框******结束*****/

//回调聊天记录（向HTML添加元素）
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

//登录后向聊天界面添加信息
socket.on('add_histiry_event', function(msg, cb) {
        SohoExamle1.Message.add(msg.username,msg.one_time,msg.one1, 'outgoing-message');
        SohoExamle1.Message.add(msg.username,msg.one_re_time,msg.one1_re, '');
        SohoExamle1.Message.add(msg.username,msg.two_time,msg.two, 'outgoing-message');
        SohoExamle1.Message.add(msg.username,msg.two_re_time,msg.two_re, '');
        SohoExamle1.Message.add(msg.username,msg.three_time,msg.three, 'outgoing-message');
        SohoExamle1.Message.add(msg.username,msg.three_re_time,msg.three_re, '');
    if (cb)
    cb();
});