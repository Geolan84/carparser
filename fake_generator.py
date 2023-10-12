from itertools import cycle
from random import shuffle


class FakeGenerator:

    def __init__(self):
        with open('creds/uagents.txt', 'r+') as ua_file:
            agents = ua_file.readlines()
            shuffle(agents)
            self.ua_pool = cycle(agents)

        with open('creds/profiles.txt', 'r+') as profile_file:
            profiles = profile_file.readlines()
            shuffle(profiles)
            self.profile_pool = cycle(profiles)

        with open('creds/addresses.txt', 'r+') as ip_file:
            addresses = ip_file.readlines()
            shuffle(addresses)
            self.ip_pool = cycle(addresses)

    def get_new_ip(self):
        return next(enumerate(self.ip_pool))[1].rstrip().split(':')

    def get_new_profile(self):
        return next(enumerate(self.profile_pool))[1].rstrip().split()

    def get_new_agent(self):
        return next(enumerate(self.ua_pool))[1].rstrip()
