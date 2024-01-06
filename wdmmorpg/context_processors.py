from .models import UserProfile  # Import the UserProfile model

def user_profile_info(request):
    user_profile = {}  # Initialize an empty dictionary
    if request.user.is_authenticated:  # Check if the user is authenticated
        try:
            user_profile = UserProfile.objects.get(user=request.user)  # Retrieve the user's profile
        except UserProfile.DoesNotExist:
            user_profile = None  # Set to None if profile doesn't exist
    return {'user_profile': user_profile}  # Return the data in a dictionary
