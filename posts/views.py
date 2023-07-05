from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from reaction.models import Reaction


class LikePost(LoginRequiredMixin, View):

    def get(self, request, id):

        REACTION_FOR_ID = 8
        REACTION_FROM_ID = 1
        
        reaction_status = "LIKE"
        object_id = id
        user = request.user.id

        is_liked = Reaction.objects.filter(object_id=id).filter(reaction_status=reaction_status).filter(user=user)

        if is_liked.exists():
            is_liked.delete()
            return redirect('core:landing')
        
        new_reaction = Reaction(
            reaction_status=reaction_status,
            object_id=object_id,
            user=user,
            reaction_for_id=REACTION_FOR_ID,
            reaction_from_id=REACTION_FROM_ID,
        )
        new_reaction.save()
        return redirect('core:landing')
    

class DislikePost(LoginRequiredMixin, View):

    def get(self, request, id):

        REACTION_FOR_ID = 8
        REACTION_FROM_ID = 1
        
        reaction_status = "DISLIKE"
        object_id = id
        user = request.user.id

        is_liked = Reaction.objects.filter(object_id=id).filter(reaction_status=reaction_status).filter(user=user)

        if is_liked.exists():
            is_liked.delete()
            return redirect('core:landing')
        
        new_reaction = Reaction(
            reaction_status=reaction_status,
            object_id=object_id,
            user=user,
            reaction_for_id=REACTION_FOR_ID,
            reaction_from_id=REACTION_FROM_ID,
        )
        new_reaction.save()
        return redirect('core:landing')
