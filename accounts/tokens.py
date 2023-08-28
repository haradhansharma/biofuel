from django.contrib.auth.tokens import PasswordResetTokenGenerator  
import six



from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for generating tokens used in email validation during user signup.

    This class extends Django's PasswordResetTokenGenerator to generate tokens with additional user activation information.

    Attributes:
        None

    Methods:
        _make_hash_value(user, timestamp): Generate a hash value for the token.
    """

    def _make_hash_value(self, user, timestamp):
        """
        Generate a hash value for the token.

        Args:
            user (User): The user for whom the token is being generated.
            timestamp (int): The timestamp when the token is generated.

        Returns:
            str: A string representing the hash value for the token.
        """
        return (
            six.text_type(user.pk) +
            six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

# Create an instance of the custom token generator for account activation.
account_activation_token = AccountActivationTokenGenerator()
