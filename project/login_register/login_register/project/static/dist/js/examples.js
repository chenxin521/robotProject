(function () {
    var SohoExamle = {
        Message: {
            add: function (message, type) {
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
                                <h5>` + (type == 'outgoing-message' ? 'Mirabelle Tow' : 'Byrom Guittet') + `</h5>
                                <div class="time">14:50 PM ` + (type == 'outgoing-message' ? '<i class="ti-check"></i>' : '') + `</div>
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
                socket.emit('my_broadcast_event', {data: $('#broadcast_data').val(),userId :'123'});
                SohoExamle.Message.add($('#broadcast_data').val(), 'outgoing-message');
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
            SohoExamle.Message.add(msg.data, '');
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
    console.log($('#last_pass').val())
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
        console.log("hahha");
        $(logout).css("display","none");
        $("#login_backtip").text("❀❀❀");
        $("#cross3").css("display","block");
        $("#cross4_out").css("display","none");

});
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
var btn=document.getElementById("btn");
var register=document.getElementsByClassName("register")[0];
btn.onclick=function(){
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
