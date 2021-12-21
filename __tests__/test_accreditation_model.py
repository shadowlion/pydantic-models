from app.models import Accreditation


def test_instance():
    accreditation = Accreditation(
        annual_income=0,
        net_worth=0,
    )
    assert isinstance(accreditation, Accreditation)
