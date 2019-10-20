

projects = dict()

projects['demo'] = {
    'long_name': 'Demo Project',
}

project_order = sorted(list(projects))


if __name__ == '__main__':

    from pprint import pprint

    print(list(projects))

    pprint(globals())

