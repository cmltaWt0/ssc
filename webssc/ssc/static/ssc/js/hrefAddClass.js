window.onload = function() {
    var path = location.pathname;
    var links = document.querySelectorAll('.nav > li > a');

    for (var i=0; i < links.length; i++) {
        if (path == links[i].pathname) {
            links[i].parentNode.className='active';
        }
    }
};

