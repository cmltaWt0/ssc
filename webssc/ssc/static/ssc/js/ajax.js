SSC_AJAX = {

    setup: function () {
        $("input[name='submit'][value='list']").click(
            function () {
                SSC_AJAX.ajaxRequest();
                return false;
            });
    },


    getForm: function () {
        var data = [];
        var name = 'login_name';
        name = encodeURIComponent(name);

        var value = document.getElementById('id_login_name').value;
        value = encodeURIComponent(value);
        data.push(name + "=" + value);
        return data.join("&");
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
        del = del || 'list';
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
                    result += '<input type="submit" value="del" name="submit" onclick="SSC_AJAX.ajaxRequest(\'del\');return false;"> '
                    result += '<input type="submit" value="back" name="submit" onclick="$(\'.output\').hide(\'slow\');return false;">'
                }

                $(".output").children().remove();
                $(".output").hide().
                prepend('<br>'+result).
                show('slow');
            }
        };

        request.send(SSC_AJAX.getForm()+'&submit='+del);
    }

};

$(SSC_AJAX.setup);
