from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.views import View
from .models import Inbox


class SendMessageView(View):
    template_name = "message/dm.html"

    def get(self, request, receiver_username, *args, **kwargs):
        # Retrieve previous messages between sender and receiver
        sender = request.user
        receiver = get_object_or_404(User, username=receiver_username)
        # key_pair = UserKeyPair.objects.filter(sender=sender, receiver=receiver).first()

        messages_history = Inbox.objects.filter(
            (Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender))
        ).order_by("timestamp")

        # Decrypt messages
        # decrypted_messages = []
        # for message in messages_history:
        #    decrypted_message = self.decrypt_message(
        #        #message.message, key_pair.encryption_key
        #    )
        #    decrypted_messages.append(
        #        (message.sender.username, decrypted_message, message.timestamp)
        #    )

        # Add logic for rendering the form
        context = {
            "receiver_username": receiver_username,
            "messages_history": messages_history,
        }
        return render(request, self.template_name, context)

    def post(self, request, receiver_username, *args, **kwargs):
        # Retrieve form data
        message_text = request.POST.get("message_text")
        message_image = request.FILES.get("message_image")
        receiver_user = get_object_or_404(User, username=receiver_username)

        # key_pair = UserKeyPair.objects.filter(sender=request.user, receiver=receiver_user).first()
        # Encrypt the message
        # If no UserKeyPair exists, create a new one with a generated encryption key
        # if not key_pair:encryption_key = Fernet.generate_key()key_pair = UserKeyPair(sender=request.user,receiver=receiver_user,encryption_key=encryption_key,key_pair.save()
        # encrypted_message = receiver_public_key.encrypt(message_text.encode()).decode()
        # fernet = Fernet(key_pair.encryption_key)
        # encrypted_message = fernet.encrypt(message_text.encode())
        # Save the message in Inbox model
        message = Inbox(
            sender=request.user,
            receiver=receiver_user,
            message=message_text,
            images=message_image,
        )
        message.save()

        messages.success(request, "Message sent successfully!")

        # Redirect to the send_message view for the receiver
        return redirect(
            reverse(
                "message:send_message",
                kwargs={"receiver_username": receiver_username},
            )
        )
