from rest_framework.generics import CreateAPIView
from .models import Contact
from .serializers import ContactSerializer

class ContactCreateView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        print("===> Contact data:", serializer.validated_data)  
        contact = serializer.save()
        print("===> Contact saved:", contact)
