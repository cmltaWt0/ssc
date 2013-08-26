function getForm() {
	var name = document.getElementById('login_name').name;
	var value = document.getElementById('login_name').value;
	var data = [];
	name = encodeURIComponent(name.replace("%20", "+"));
	value = encodeURIComponent(value.replace("%20", "+"));
	data.push(name + "=" + value);
	return data.join("&");
}


function ajaxRequest() {
	var request = new XMLHttpRequest();
	request.open("GET", "/ssc/ajax/");
	request.onreadystatechange = function() {
		if (request.readyState === 4 && request.status === 200) {
			document.getElementById('login_name').value = request.responseText;
		}
	};
	request.send(null);
}


document.getElementById('ajax_submit').onclick = function () {
	ajaxRequest(getForm());
	return false;
}