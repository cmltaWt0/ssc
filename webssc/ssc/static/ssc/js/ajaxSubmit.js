function getForm() {
    var name = document.getElementById('login_name').name;
    var value = document.getElementById('login_name').value;
    var data = [];
    name = encodeURIComponent(name);
    value = encodeURIComponent(value);
    data.push(name + "=" + value);
    return data.join("&");
}


function getCSRFToken(name) {
    var cookie = null;
    if (document.cookie && document.cookie != '') {
        var allcookies = document.cookie.split('; ');
        for (i in allcookies) {
            data = $.trim(decodeURIComponent(allcookies[i]));
            if (data.split('=')[0] == name) {
                cookie = data.split('=')[1];
                break;
            }
        }
    }
    return cookie;
}


function ajaxRequest(xml) {
    var request = new XMLHttpRequest();
    xml = xml || false;
    xml ? request.open("POST", "/ssc/ajax/xml/")
        : request.open("POST", "/ssc/ajax/");
    request.setRequestHeader("Content-Type",
                             "application/x-www-form-urlencoded");
    request.setRequestHeader("X-CSRFToken", getCSRFToken('csrftoken'))
    
    request.onreadystatechange = function() {
        if (request.readyState === 4 && request.status === 200) {
	    document.getElementById('login_name').
                                    value = request.responseText;
        }
    };
    
    request.send(getForm());
}


document.getElementById('ajax_submit').onclick = function () {
    ajaxRequest();
    return false;
}


document.getElementById('ajax_xml_submit').onclick = function () {
    ajaxRequest(true);
    return false;
}
