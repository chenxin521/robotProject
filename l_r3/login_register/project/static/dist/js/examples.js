(function () {
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
        // $('#disconnected').modal('show');
        // $('#call').modal('show');
        // $('#videoCall').modal('show');
        $('#pageTour').modal('show');
    }, 1000);


    $(document).ready(function() {
        namespace = '/test';
        var socket = io(namespace);
        userId = '123';
        $('form#broadcast').submit(function(event) {
            // if ($('#broadcast_data').val()) {
                socket.emit('my_broadcast_event', {data: $('#broadcast_data').val(),userId :'123',check:$("#logout_username").text()});
                console.log($("#logout_username").text());
                // SohoExamle.Message.add($('#broadcast_data').val(), 'outgoing-message');
                $('#broadcast_data').val('');
                // SohoExamle.Message.add(userId, 'outgoing-message');
            //     input.val('');
            // } else {
            //     input.focus();
            // }
            return false;
        });

        socket.on('my_response', function(msg, cb) {
            console.log(msg);
            $('#logout_username').val()

            SohoExamle.Message.add(msg.question,msg.username,msg.time1, 'outgoing-message');//问题
            // if (msg.count%2==1){
            SohoExamle.Message.add(msg.data,msg.username,msg.time2, '');//回答
            // SohoExamle.Message.add(userId, '');
            if (cb)
                cb();
        });

        //login in --submit

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

//login_in
$(".my_btn_login").click(function () {
        socket.emit('my_login_event', {username: $('#login_name').val(),password :$('#login_pass').val()});

});

//login_backtips_event
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

socket.on('login_backtips_event', function(msg, cb) {
    console.log(msg.data);
    console.log("shibai");
    $("#login_backtip").text(msg.data);
    if (cb)
    cb();
});

//register_in
$('#my_btn_register').click(function () {
    socket.emit('my_register_event', {username: $('#register_name').val(),studentid: $('#register_id').val(),
            email: $('#register_email').val(),password :$('#register_pass').val(),lastpass: $('#last_pass').val()});
});
//register_tips_event
socket.on('register_success_event', function(msg, cb) {
    $("#register_tip").text(msg.data);
    setTimeout(function () {
        $(register).css("display","none");
    }, 1000);
    // var name = $('#register_name').val();
    // $("#cross4_out").text(name.slice(0,1));
    // $("#cross4_out").css("display","block");
    // $("#cross3").css("display","none");
    // $("#logout_username").text(name);
    if (cb)
    cb();
});

socket.on('register_tips_event', function(msg, cb) {
    $("#register_tip").text(msg.data);
    if (cb)
    cb();
});

//logout
$("#my_btn_out").click(function () {
        $(logout).css("display","none");
        $("#login_backtip").text("");
        $("#cross3").css("display","block");
        $("#cross4_out").text("");
        $("#cross4_out").css("display","none");
        $('.layout .content .chat .chat-body .messages').html(
                    `<div class="message-item ">
                        <div class="message-avatar">
                            <figure class="avatar">
                                <img src="/static/dist/media/img/man_avatar3.jpg" class="rounded-circle" alt="image">
                            </figure>
                            <div>
                                <h5>小软棉</h5>
                                <div class="time"></div>
                            </div>
                        </div>
                        <div class="message-content">
                                欢迎来到你的私人小空间！小软棉已经等候您好久啦，快来和我聊天吧~ 😃
                        </div>
                        
                    </div>`);
});
var cross4_out=document.getElementById("cross4_out");
var logout=document.getElementsByClassName("logout")[0];
cross4_out.onclick=function(){
    console.log($(logout).css("display"))
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

//login
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


//register
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


/*********简介框******开始*****/
//手机版点击简介弹出介绍框
var ins = document.getElementsByClassName("ins")[0];
var intr  = document.getElementsByClassName("introduction")[0];
var chat=document.getElementsByClassName("chat-body")[0];
ins.onclick=function (){
    intr.style.display="block";
}
chat.onclick=function(){
    intr.style.display="none";
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
 // for (var j=0;j<li.length;j++){

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

var ban1=document.getElementsByClassName("class1")[0];
var grade=document.getElementsByClassName("grade")[0];
var point=document.getElementsByClassName("point")[0];
grade.onchange=function(){
    var text=grade.options[grade.selectedIndex].text;

    if(text=="大三"){
        point.style.display="block";
        ban1.style.display="none";
    }
    else{
        ban1.style.display="block";
        point.style.display="none";
    }
}

var ban2=document.getElementsByClassName("class2")[0];
var grade2=document.getElementsByClassName("grade2")[0];
var point2=document.getElementsByClassName("point2")[0];
grade2.onchange=function(){
    var text=grade2.options[grade2.selectedIndex].text;
    console.log(text)
    if(text=="大三"){
        point2.style.display="block";
        ban2.style.display="none";
    }
    else{
        ban2.style.display="block";
        point2.style.display="none";
    }
}



/*********简介框******结束*****/

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
        console.log(msg.two_re)
        console.log(msg.username);
        SohoExamle1.Message.add(msg.username,msg.one_time,msg.one1, 'outgoing-message');
        SohoExamle1.Message.add(msg.username,msg.one_re_time,msg.one1_re, '');
        SohoExamle1.Message.add(msg.username,msg.two_time,msg.two, 'outgoing-message');
        SohoExamle1.Message.add(msg.username,msg.two_re_time,msg.two_re, '');
        SohoExamle1.Message.add(msg.username,msg.three_time,msg.three, 'outgoing-message');
        SohoExamle1.Message.add(msg.username,msg.three_re_time,msg.three_re, '');
    if (cb)
    cb();
});

