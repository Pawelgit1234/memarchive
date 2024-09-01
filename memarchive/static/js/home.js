$(document).ready(function() {
    let nextUrl;

    function loadData(url) {
        fetchData(url, 'GET', {}, function(data) {
            addMedias(data);
            nextUrl = data["next"];
        });
    }

    loadData(medias_url);
    enableInfiniteScroll(200, function() {
        if (nextUrl) {
            loadData(nextUrl);
        }
    });
});

function addMedias(data) {
    data = data["results"];
    data.forEach(media => {
        if (Object.keys(media).length === 0) return;

        let title = media.title;
        if (title.length > 18) title = title.slice(0, 18) + "...";

        let mediaElement;
        if (media.media.slice(-4) === '.mp3' || media.media.slice(-4) === '.wav') {
            mediaElement = `
                <div class="audio-container">
                    <div id="waveform-${media.id}" class="card-img-top" style="width: 100%; height: 100%; margin-top: 40px;"></div>
                    <span id="audio-duration-${media.id}" class="duration"></span>
                </div>`;
        } else if (media.media.slice(-4) === '.mp4') {
            mediaElement = `
                <div class="video-container">
                    <video class="card-img-top" autoplay="" muted="" loop="" id="video-${media.id}">
                        <source src="${media.media}" type="video/mp4">
                    </video>
                    <span id="duration-${media.id}" class="duration"></span>
                </div>`;
        } else {
            mediaElement = `<img src="${media.media}" class="card-img-top" alt="${media.title}">`;
        }

        $('.medias').append(
            `<div class="card media m-2" style="width: 18rem;">
                <a href="${media.slug}" class="media-link">
                    ${mediaElement}
                </a>
                <div class="card-body d-flex align-items-start">
                    <img src="${media.avatar_url}" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 10px;">
                    <div>
                        <p class="card-text mb-0"><b>${title}</b></p>
                        <p class="card-text text-muted" style="font-size: 12px;">${media.username}</p>
                        <p class="card-text text-muted" style="font-size: 12px;">${media.views_count} · ${media.timestamp}</p>
                    </div>
                </div>
            </div>`
        );

        if (media.media.slice(-4) === '.mp3' || media.media.slice(-4) === '.wav') {
            setTimeout(() => {
                const wavesurfer = drawWaveform(media.media, `waveform-${media.id}`);
                wavesurfer.on('ready', function() {
                    const duration = wavesurfer.getDuration();
                    const durationText = formatDuration(duration);
                    $(`#audio-duration-${media.id}`).text(durationText);
                });
            }, 0);
        } else if (media.media.slice(-4) === '.mp4') {
            const videoElement = $(`#video-${media.id}`).get(0);
            videoElement.addEventListener('loadedmetadata', function() {
                const duration = videoElement.duration;
                const durationText = formatDuration(duration);
                $(`#duration-${media.id}`).text(durationText);
            });
        }
    });
}


