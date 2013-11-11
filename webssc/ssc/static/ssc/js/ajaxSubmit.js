SSC_AJAX = {

    setup: function () {
        $('#submit').click(
            function () {
                SSC_AJAX.ajaxRequest();
                return false;
            });

        $('<div id="result"></div>').
            hide().
            insertAfter($('#submit'));
    },


    getForm: function () {
        var data = [];
        var name = 'login_name';
        name = encodeURIComponent(name);

        if ($('#raw')[0].checked) {
            var value = document.getElementById('login_name').value;
            value = encodeURIComponent(value);
            data.push(name + "=" + value);
            return data.join("&");
        } else {
            var city = document.getElementById('city').value;
            var point = document.getElementById('point').value;
            var opt3 = String(Number($('#opt3').val()));
            if (opt3.length == 1) opt3 = '0' +opt3;
            var opt4 = String(Number($('#opt4').val()));
            if (opt4.length == 1) opt4 = '0' +opt4;
            var opt5 = String(Number($('#opt5').val()));
            var opt7 = String(Number($('#opt7').val()));
            value = city+ '-' + point + ' PON 1/1/' + opt3 + '/' + opt4 + ':' + opt5 + '.1.' + opt7;
            value = encodeURIComponent(value);
            data.push(name + "=" + value);
            return data.join("&");
        }
    },


    getCSRFToken: function (name) {
        var cookie = null;
        if (document.cookie && document.cookie != '') {
            var allcookies = document.cookie.split('; ');
            for (var i in allcookies) {
                var data = decodeURIComponent(allcookies[i]).
                                        replace(/^\s+|\s+$/g, '');
                if (data.split('=')[0] == name) {
                    cookie = data.split('=')[1];
                    break;
                }
            }
        }
        return cookie;
    },


    ajaxRequest: function (del) {
        var request = new XMLHttpRequest();
        del = del || false;
        request.open("POST", "/ssc/");
        request.setRequestHeader("Content-Type",
                                 "application/x-www-form-urlencoded");
        request.setRequestHeader("X-CSRFToken", SSC_AJAX.getCSRFToken('csrftoken'));
        request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    
        request.onreadystatechange = function() {
            if (request.readyState === 4 && request.status === 200) {
                var result = '';
                var response = JSON.parse(request.responseText);

                if (response[1] == false) {
                    result += '<li>'+response[0]+'</li>';
                } else {
                    result += '<p><b>Session information.</b></p>'

                    for (var key in response[0]) {
                        result += '<ul><b>' + key + '</b>';
                        for (var i in response[0][key]) {
                            result += '<li>' + response[0][key][i] + '</li>';
                        }
                        result += '<br></ul>'
                    }
                    result += '<p><b>Are you want to delete this session(s)</b></p>'
                    result += '<input type="submit" value="Delete" name="submit" id="delete" onclick="SSC_AJAX.ajaxRequest(\'del\');return false;"> '
                    result += '<input type="submit" value="No" name="submit" id="cancel_delete" onclick="$(\'#result\').hide(\'slow\');return false;">'
                }

                $('#result').children().remove();
                $('#result').hide().
                prepend('<br>'+result).
                show('slow');
            }
        };
        request.send(SSC_AJAX.getForm()+'&method='+del);
    }

};

$(SSC_AJAX.setup);