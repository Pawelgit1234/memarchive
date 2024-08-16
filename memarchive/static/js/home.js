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
        $('.medias').append(
            `<div class="card media m-2" style="width: 18rem;">
                <img src="${media.media}" class="card-img-top" alt="${media.title}">
                <div class="card-body">
                    <p class="card-text">${media.description}</p>
                </div>
            </div>`
        );
    });
}
