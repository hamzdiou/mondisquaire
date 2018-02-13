from django.test import TestCase # Hérite de UnitTest
from django.core.urlresolvers import reverse
from store.models import Album, Artist, Contact, Booking


# Index Page
class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


# Detail Page
class DetailPageTestCase(TestCase):
    # Put the data to be setup before running tests
    def setUp(self):
        impossible = Album.objects.create(title="Transmission Impossible")
        self.album = Album.objects.get(title="Transmission Impossible")

    # test that detail page returns a 200 if the item exists
    def test_detail_page_returns_200(self):
        album_id = self.album.id
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 200)

    # test that detail page returns a 404 if the item doesn't exist
    def test_detail_page_returns_404(self):
        album_id = self.album.id + 1
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 404)


# Booking Page
class BookingPageTestCase(TestCase):

    def setUp(self):
        Contact.objects.create(name="Freddie", email="ferd@queen.forever")
        impossible = Album.objects.create(title="Transmission Impossible")
        journey = Artist.objects.create(name="Journey")
        impossible.artists.add(journey)
        self.contact = Contact.objects.get(name="Freddie")
        self.album = Album.objects.get(title="Transmission Impossible")

    # test that a new booking is made
    def test_new_booking_is_registered(self):
        old_booking = Booking.objects.count()
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(
            reverse('store:detail', args=(album_id,)),
            {
                'name': name,
                'email': email
            }
        )
        new_booking = Booking.objects.count()
        self.assertEqual(new_booking, old_booking + 1)

    # test that a booking belongs to a contact
    def test_booking_belongs_to_contact(self):
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(
            reverse('store:detail', args=(album_id,)),
            {
                'name': name,
                'email': email
            }
        )
        booking = Booking.objects.last()
        self.assertEqual(self.contact, booking.contact)

    # test that a booking belongs to an album
    def test_booking_belongs_to_album(self):
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(
            reverse('store:detail', args=(album_id,)),
            {
                'name': name,
                'email': email
            }
        )
        booking_contact = Booking.objects.last()
        self.assertEqual(booking_contact.album, self.album)

    # test that an album is not available after a booking is made
    def test_album_not_available_after_booking(self):
        old_album_status = self.album.available
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(
            reverse('store:detail', args=(album_id,)),
            {
                'name': name,
                'email': email
            }
        )
        new_album_status = self.album.refresh_from_db()
        self.assertEqual(old_album_status, not new_album_status)

