(function() {
    check_wrapper = function(el_num) {
        function wrapped() {
	    var el = document.getElementsByTagName('input')[el_num];
	    el.checked = true;
        }
        return wrapped
    }

    document.getElementById('login_name').onfocus = check_wrapper(1);
    for (var i=4; i<11; i++) {
        document.getElementsByTagName('input')[i].onfocus = check_wrapper(3);
    }

    next_wrapper = function(char_count) {
        function wrapped() {
            var value = String(parseInt(this.value));
            if (value != 0 && value.length == char_count) {
                document.getElementsByName('opt'+
                         (parseInt(this.name.slice(-1))+1))[0].focus();
            }
        }
        return wrapped
    }

    document.getElementsByTagName('input')[4].onfocus = next_wrapper(1);
    document.getElementsByTagName('input')[5].onfocus = next_wrapper(1);
    document.getElementsByTagName('input')[6].oninput = next_wrapper(2);
    document.getElementsByTagName('input')[7].oninput = next_wrapper(1);
    document.getElementsByTagName('input')[8].oninput = next_wrapper(2);
    document.getElementsByTagName('input')[9].onfocus = next_wrapper(1);
    document.getElementsByTagName('input')[10].oninput = next_wrapper(1);
}());
