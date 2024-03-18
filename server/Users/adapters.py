from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def populate_username(self, request, user):
        # You don't need to do anything here
        pass
