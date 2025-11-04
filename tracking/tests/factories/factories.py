import factory
from tracking.models import Website, Session
from accounts.models import Organization


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker('name')
    is_active = True


class WebsiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Website
    organization = factory.SubFactory(OrganizationFactory)
    domain = factory.Sequence(lambda n: f"site{n}.com")
    name = factory.Faker("name")
    is_active = True


class SessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Session

    website = factory.SubFactory(WebsiteFactory)
    session_id = factory.Sequence(lambda n: f"session-{n}")
    user_agent = "Mozilla/5.0 (iPhone)"
    ip_address = "1.2.3.4"
    country = "US"
    browser = "Safari"
    device_type = "mobile"
