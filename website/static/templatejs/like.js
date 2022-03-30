function like(post_id){
    let likeCount = document.getElementById('like-count-' + post_id);
    let likebutton = document.getElementById('like-button-'  + post_id);

    fetch('/like-post/' + post_id, {method:"POST"}).then((res) => res.json()).then((data) => likeCount.innerHTML = data['likes']);
}