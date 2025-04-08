from rest_framework import serializers
from userauths.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # When specifying fields or exclude in the Meta class, you must use square brackets because DRF expects a list of field names
        model = User
        fieds = ['__all__']   # you can add the field you want to add like full_name, email and so on but with this i want to make use of all field in the User modelalready created

    # if you don't ant to include some field u can use exclude
   #exclude = ['full_name']

#    serializing the profile 

class ProfileSterilizer(serializers.ModelSterilizer):
    # user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['__all__']

    def to_representation(self,instance):  # takes the two arguments that's instance and self 
        # the self argument reps the current instance of the class i created (profile class)
        #  instance argument represent the object being sterialized (profile object)
        # convert instance object into dictionary
#defining a method within a class
        response = super().to_representation(instance)   #Purpose: Calls the parent class's to_representation() method to get the default serialized data (as a Python dictionary) for the instance.
        response['user'] = UserSerializer(instance.user).data  # Purpose: Adds a nested user field to the serialized data by:


        return response
    # Returns the modified dictionary (now including the nested user data) as the final serialized output.