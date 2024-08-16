function enableInfiniteScroll(triggerDistance, callback) {
    let isThrottled = false;

    $(window).on('scroll', function() {
        if (isThrottled) return;

        if ($(window).scrollTop() + $(window).height() >= $(document).height() - triggerDistance) {
            isThrottled = true;
            setTimeout(function() {
                callback();
                isThrottled = false;
            }, 1000); // wait 1 second
        }
    });
}


function fetchData(url, method='GET', data = {}, onSuccess, onError) {
    $.ajax({
        url: url,
        type: method,
        data: data,
        success: function(response) {
            if (typeof onSuccess === 'function') {
                onSuccess(response);
            }
        },
        error: function(xhr, status, error) {
            if (typeof onError === 'function') {
                onError(xhr, status, error);
            }
        }
    });
}