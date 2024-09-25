function handleLiking()
{
    let method = user_liked ? 'DELETE' : 'POST';

  fetchData(like_url, method, {'user': user_id}, function(response) {
        if (response.liked) {
            $('#like').attr('src', star_full);
        } else {
            $('#like').attr('src', star_empty);
        }

        $('span.likes-count').text(response.likes_count);
        user_liked = response.liked;
    }, function(xhr, status, error) {
        console.error('Error liking/unliking media:', error);
    });
}

function handleFollowing()
{
    let method = user_following ? 'DELETE' : 'POST';
    fetchData(follow_url, method, {'user': user_id}, function(response) {
        if (response.is_following) {
            $('#follow').attr('src', follow_full);
        } else {
            $('#follow').attr('src', follow_empty);
        }

        $('span.followers-count').text(response.followers_count);
        user_following = response.is_following;
    }, function(xhr, status, error) {
        console.error('Error following/unfollowing media:', error);
    });
}