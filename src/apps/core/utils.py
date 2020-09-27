from django.contrib.auth.models import User

from friendship.models import Friend, FriendshipRequest


def get_friendship(current_user):
    """
    Get all friends, current friendships and friendship requests sent
    for a user.

    Parameters
    ----------
    current_user : obj
        Current user instance.

    Returns
    -------
    context : dict
        All friends, frendship request sent, friendship request received.
    """
    friendship = FriendshipRequest.objects.filter(to_user=current_user)
    friends = Friend.objects.filter(to_user=current_user)
    friendship_request_sent = FriendshipRequest.objects.filter(
        from_user=current_user
    )
    context = {
        "friendship": [],
        "friends": [],
        "friendship_request_sent": []
    }
    # Get all friendships.
    for fs in friendship:
        user = User.objects.filter(id=fs.from_user_id)
        if user:
            context["friendship"].append({
                "id": fs.id,
                "message": fs.message,
                "user": {
                    "id": fs.from_user_id,
                    "username": user.first().username
                }
            })
    # Get all friends.
    for f in friends:
        user = User.objects.filter(id=f.from_user_id)
        if user:
            context["friends"].append({
                "id": user.first().id,
                "username": user.first().username
            })
    # Get all friendship requests sent.
    for frs in friendship_request_sent:
        user = User.objects.filter(id=frs.to_user_id)
        if user:
            context["friendship_request_sent"].append({
                "id": frs.id,
                "username": user.first().username,
                "date": frs.created
            })

    return context
