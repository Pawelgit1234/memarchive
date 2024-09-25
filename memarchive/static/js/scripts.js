function enableInfiniteScroll(triggerDistance, callback) {
    let isThrottled = false;

    $(window).on('scroll', function() {
        if (isThrottled) return;

        if ($(window).scrollTop() + $(window).height() >= $(document).height() - triggerDistance) {
            isThrottled = true;
            setTimeout(function() {
                callback();
                isThrottled = false;
            }, 200); // wait 0.2 second
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function fetchData(url, method='GET', data = {}, onSuccess, onError) {
    $.ajax({
        url: url,
        type: method,
        data: data,
        headers: {
            'X-CSRFToken': csrftoken
        },
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

function formatDuration(duration) {
    const minutes = Math.floor(duration / 60);
    const seconds = Math.floor(duration % 60);
    const milliseconds = Math.floor((duration % 1) * 1000);

    if (duration < 1)
        return `${milliseconds}ms`;

    return `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
}

function drawWaveform(audioUrl, id) {
    const wavesurfer = WaveSurfer.create({
            container: `#${id}`,
            waveColor: '#109412',
            progressColor: '#109412',
            url: audioUrl,
            interact: false,
            hideScrollbar: true,
            cursorWidth: 0
        })

    return wavesurfer;
}