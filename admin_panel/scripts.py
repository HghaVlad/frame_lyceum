from main.models import User, Activations


def give_addition_points(min_activations, new_points):
    for user in User.objects.all():
        if len(Activations.objects.filter(user=user).count()) >=min_activations:
            user.points += new_points
            user.save()

