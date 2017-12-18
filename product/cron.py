from django_cron import CronJobBase, Schedule

from product.models import Rating, PopularBooks


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 * 24

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'

    def do(self):
        rating = Rating.objects.all().order_by('number_of_purchases')[:5]
        PopularBooks.objects.all().delete()

        for book in rating:
            PopularBooks.objects.create(book=book)