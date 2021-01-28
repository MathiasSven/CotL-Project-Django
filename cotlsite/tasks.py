from celery import shared_task
import requests
from bs4 import BeautifulSoup

from .models import MemberNation


@shared_task()
def get_member_nations_flag_url():
    for nation in MemberNation.objects.all():
        url = f'https://politicsandwar.com/nation/id={nation.nation_id}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        flag_url = soup.find(id='flagcontainer').img.get('src')

        nation.update(flag_url=flag_url)
