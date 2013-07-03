(function() {
	check_wrapper = function(n) {
		function wrapped() {
			var el = document.getElementsByTagName('input')[n];
			el.checked = true;
		}
		return wrapped
	}

	document.getElementsByTagName('input')[2].onfocus = check_wrapper(1);
	for (var i=4; i<11; i++) {
		document.getElementsByTagName('input')[i].onfocus = check_wrapper(3);
	}


	next_wrapper = function(n) {
		function wrapped() {
			//if (this.value.length == 0 && event.keyIdentifier=="U+0008") {
			//	this.previousSibling.previousSibling.previousSibling.previousSibling.focus();
			//}
			if (this.value.length == n && this.name == "opt7") {
				document.getElementsByTagName('input')[11].focus();	
			}
			else if (parseInt(this.value) != 0 && this.value.length > 0 && this.name == "opt4") {
				this.nextSibling.nextSibling.nextSibling.nextSibling.focus();				
			}
			else if (this.value.length == n) {
				this.nextSibling.nextSibling.nextSibling.nextSibling.focus();
			}

		}
		return wrapped
	}
	document.getElementsByTagName('input')[4].onfocus = next_wrapper(1);
	document.getElementsByTagName('input')[5].onfocus = next_wrapper(1);
	document.getElementsByTagName('input')[6].onkeyup = next_wrapper(2);
	document.getElementsByTagName('input')[7].onkeyup = next_wrapper(2);
	document.getElementsByTagName('input')[8].onkeyup = next_wrapper(2);
	document.getElementsByTagName('input')[9].onfocus = next_wrapper(1);
	document.getElementsByTagName('input')[10].onkeyup = next_wrapper(1);
}());
