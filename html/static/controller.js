$(document).ready(function() {

    $('#minfo').hover(
        function() { $('#minfo').clearQueue() },
        function() { $('#minfo').delay(1000).hide(1) }
    )

    showinfo = function(tt) {
        $('#minfo').clearQueue()
        $('#minfo').load('info/'+tt)
        $('#minfo').show()
    }

    hideinfo = function() {
        $('#minfo').delay(1000).hide(1)
    }


})

// vim: foldmethod=marker:expandtab:shiftwidth=4:tabstop=4:softtabstop=4:encoding=utf-8:textwidth=80
