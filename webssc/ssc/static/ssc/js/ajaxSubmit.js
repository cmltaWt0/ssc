SSC_AJAX = {

    setup: function () {
        $('#ajax_submit').click(
            function () {
                SSC_AJAX.ajaxRequest();
                return false;
            });

        $('#ajax_xml_submit').click(
            function () {
                SSC_AJAX.ajaxRequest(true);
                return false;
            });

        $('<div id="result"></div>').
            hide().
            insertAfter($('#ajax_xml_submit'));
    },

    getForm: function () {
        var name = document.getElementById('login_name').name;
        var value = document.getElementById('login_name').value;
        var data = [];
        name = encodeURIComponent(name);
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


    ajaxRequest: function (xml) {
        var request = new XMLHttpRequest();
        xml = xml || false;
        xml ? request.open("POST", "/ssc/ajax/xml/")
            : request.open("POST", "/ssc/ajax/");
        request.setRequestHeader("Content-Type",
                                 "application/x-www-form-urlencoded");
        request.setRequestHeader("X-CSRFToken", SSC_AJAX.getCSRFToken('csrftoken'));
    
        request.onreadystatechange = function() {
            if (request.readyState === 4 && request.status === 200) {
                var result = '';
                var response_split = request.responseText.split('\n');
                for (var i in response_split) {
                    result += '<li>'+response_split[i]+'</li>';
                }
                $('#result').children().remove();
                $('#result').hide().
                prepend('<br>'+result).
                show('slow');
            }
        };
        request.send(SSC_AJAX.getForm());
    }

};

$(SSC_AJAX.setup);