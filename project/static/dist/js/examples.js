(function () {

    /**
     * Some examples of how to use features.
     *
     **/

    var SohoExamle = {
        Message: {
            add: function (message, type) {
                var chat_body = $('.layout .content .chat .chat-body');

                if (chat_body.length > 0) {
                    console.log(message);

                    type = type ? type : '';
                    message = message ? message : '收到（假的）';

                    $('.layout .content .chat .chat-body .messages').append(`<div class="message-item ` + type + `">
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

        $('form#broadcast').submit(function(event) {

            // if ($('#broadcast_data').val()) {

                socket.emit('my_broadcast_event', {data: $('#broadcast_data').val()});

                SohoExamle.Message.add($('#broadcast_data').val(), 'outgoing-message');
            //     input.val('');

            // } else {
            //     input.focus();
            // }

            return false;
        });

        socket.on('my_response', function(msg, cb) {
            console.log(msg);
            SohoExamle.Message.add(msg.data, '');
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

})();