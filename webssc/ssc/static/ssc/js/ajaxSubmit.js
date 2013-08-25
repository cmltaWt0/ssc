function getForm () {
	var name = document.getElementsByTagName('input')[2].name;
	var value = document.getElementsByTagName('input')[2].text;
	var data = [];
	name = encodeURIComponent(name.replace("%20", "+"));
	value = encodeURIComponent(value.replace("%20", "+"));
	data.push(name + "=" + value);
	return data.join("&");
}

function ajax_submit () {
	var request = new XMLHttpRequest();
	request.open("POST", "/ssc/ajax/");
	request.setRequestHeader("Content-Type",
		                     "application/x-www-form-urlencoded");
	request.send(getForm());
	var response = request.response.text;
	return false;
}