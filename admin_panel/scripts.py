from main.models import User, Activation


def give_addition_points(min_activations: int, new_points: int):
    users_list = []
    for user in User.objects.all():
        if Activation.objects.filter(User=user).count() >= int(min_activations):
            user.points += int(new_points)
            user.save()
            users_list.append(user)
    return users_list
