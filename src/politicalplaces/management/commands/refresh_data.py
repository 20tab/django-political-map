from django.core.management.base import BaseCommand
from politicalplaces.models import PoliticalPlace
from politicalplaces.exceptions import NoResultsException


class Command(BaseCommand):

    help = 'Refresh map data calling the external api'

    def add_arguments(self, parser):
        parser.add_argument(
            'place_id', nargs='*', type=int, default=0,
            help='The id list, separated by space, of the involved PoliticalPlace objects.')

    def handle(self, *args, **options):
        self.stdout.write("Refresh data started.")
        count = 0
        errors = 0
        if options['place_id'] != 0:
            all_places = PoliticalPlace.objects.filter(pk__in=options['place_id'])
        else:
            all_places = PoliticalPlace.objects.all()
        for place in all_places:
            if options['verbosity'] != 0:
                self.stdout.write(
                    "Refreshing data for PoliticalPlace: {} - {}".format(
                        place.pk, place.address
                    ))
            try:
                place.refresh_data()
            except NoResultsException as e:
                errors += 1
                if options['verbosity'] != 0:
                    self.stdout.write(
                        "PoliticalPlace: {} - {}: {}".format(
                            place.pk, place.address, e
                        ))
                else:
                    self.stdout.write("PoliticalPlace {}: {}".format(place.pk, e))
            except Exception as e:
                errors += 1
                if options['verbosity'] != 0:
                    self.stdout.write(
                        "PoliticalPlace: {} - {}: {}".format(
                            place.pk, place.address, e
                        ))
                else:
                    self.stdout.write("PoliticalPlace {}: {}".format(place.pk, e))
            else:
                count += 1
        self.stdout.write(
            "Refresh data completed successfully for {} items, {} errors.".format(
                count, errors)
        )
