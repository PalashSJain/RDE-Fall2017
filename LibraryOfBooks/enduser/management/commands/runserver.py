from django.core.management.commands.runserver import BaseRunserverCommand


class Command(BaseRunserverCommand):
    def inner_run(self, *args, **options):
        self.stdout.write("Hello World!")
        super(Command, self).inner_run(*args, **options)
