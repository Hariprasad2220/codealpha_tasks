// Mini Social Media Platform - client-side interactivity
// Handles like/unlike and follow/unfollow without a full page reload.

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', () => {
    // Like / unlike buttons
    document.querySelectorAll('.like-btn').forEach((btn) => {
        btn.addEventListener('click', async () => {
            const url = btn.dataset.url;
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });
                if (!response.ok) throw new Error('Request failed');
                const data = await response.json();
                btn.classList.toggle('liked', data.liked);
                btn.querySelector('.like-count').textContent = data.like_count;
                btn.dataset.liked = data.liked;
            } catch (err) {
                console.error('Like toggle failed', err);
            }
        });
    });

    // Follow / unfollow button
    document.querySelectorAll('.follow-btn').forEach((btn) => {
        btn.addEventListener('click', async () => {
            const url = btn.dataset.url;
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });
                if (!response.ok) throw new Error('Request failed');
                const data = await response.json();
                btn.textContent = data.following ? 'Following' : 'Follow';
                btn.classList.toggle('following', data.following);
                btn.classList.toggle('primary', !data.following);
                const counter = document.querySelector('.follower-count strong');
                if (counter) counter.textContent = data.follower_count;
            } catch (err) {
                console.error('Follow toggle failed', err);
            }
        });
    });
});
