import datetime
import requests
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
import urllib
from .forms import MainForm


class MainPageView(generic.View):
    def get(self, request, *args, **kwargs):
        form = MainForm()
        context = {'form': form}
        return render(request, template_name='app/index.html', context=context)

    @staticmethod
    def make_request(params, method):
        """
        Make request to vk.com based on params and method.
        """
        querystring = urllib.parse.urlencode(params, safe=',')
        url = 'https://api.vk.com/method/' + method + '?' + querystring
        response = requests.get(url).json()
        return response.get('response')

    def filter_users(self, user_ids, token, date) -> list:
        """
        Filter users created 3 posts in period from last_post_date till today.
        """
        chosen_users = []
        for user_id in user_ids:
            params = {'owner_id': user_id, 'count': 1, 'access_token': token, 'v': 5.131, }
            method = 'wall.get'
            data = self.make_request(params, method)
            if data:
                posts = data['items']
                last_post_date = datetime.date.fromtimestamp(posts[0]['date'])
                if last_post_date > date:
                    chosen_users.append(str(user_id))
        return chosen_users

    def get_user_links(self, chosen_users, token):
        """
        Make request to vk api and get screen_name of users.
        screen_name is necessary to get link of vk profile.
        """
        ids = ','.join(chosen_users)
        params = {'user_ids': ids, 'count': 4,
                  'fields': 'screen_name', 'access_token': token, 'v': 5.131}
        users = self.make_request(params, 'users.get')
        screen_names = [user['screen_name'] for user in users]
        return screen_names

    def post(self, request, *args, **kwargs):
        form = MainForm(request.POST, request.FILES)
        if form.is_valid():
            date = form.cleaned_data['date']
            user_list_file = form.cleaned_data['user_list']
            token = '5647f1775647f1775647f177fd5635bc04556475647f1770895ad2ec49b94557826f605'
            f = user_list_file
            user_ids = [user_id.strip().decode('utf-8') for user_id in f.readlines() if user_id.strip()]
            chosen_users = self.filter_users(user_ids, token, date)
            screen_names = self.get_user_links(chosen_users, token)
            context = {'users': screen_names}
            return render(request, template_name="app/users.html", context=context)
        return render(request, template_name="app/index.html", context={'form': form})

