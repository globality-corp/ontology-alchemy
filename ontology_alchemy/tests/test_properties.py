"""Unit-tests for RDF Properties support."""
from unittest import skip

from hamcrest import (
    assert_that,
    calling,
    contains_inanyorder,
    equal_to,
    has_length,
    is_,
    raises,
)
from rdflib import Literal

from ontology_alchemy.tests.fixtures import create_ontology


def test_core_rdfs_properties_for_a_class_instance_constructor_work():
    ontology = create_ontology()
    label = "Acme Inc."
    comment = Literal("Acme Inc. es un fabricante de paneles solares", lang="es")
    instance = ontology.Organization(
        label=label,
        comment=comment
    )

    assert_that(instance.label(lang="en"), contains_inanyorder(label))
    assert_that(instance.comment(lang="es"), contains_inanyorder(comment.value))


def test_primitive_type_assigment_for_property_proxy_works():
    ontology = create_ontology()
    instance = ontology.Organization()
    value = 156.4
    instance.value += value

    assert_that(instance.value, contains_inanyorder(value))


def test_primitive_type_assigment_for_literal_property_proxy_works():
    ontology = create_ontology()
    instance = ontology.Organization()
    label = "label"
    instance.label += label

    assert_that(instance.label, contains_inanyorder(Literal(label, lang="en")))


def test_xsd_type_assigment_for_literal_property_proxy_works():
    ontology = create_ontology()
    instance = ontology.Country()
    currency_code = "USD"
    instance.currencyCode += currency_code

    assert_that(instance.currencyCode, contains_inanyorder(Literal(currency_code, lang="en")))


def test_invalid_properties_for_a_class_instance_constructor_raise_attribute_error():
    ontology = create_ontology()

    assert_that(calling(ontology.Organization).with_args(foo="bar"), raises(AttributeError))


def test_valid_property_assigment_for_a_class_instance_work():
    ontology = create_ontology()
    domain_instance = ontology.Organization(
        label="Acme Inc.",
    )
    range_instance = ontology.Person(
        label="John Doe",
    )
    comment = "test comment"

    domain_instance.comment += comment
    domain_instance.hasEmployee += range_instance

    assert_that(domain_instance.hasEmployee(range_instance), is_(equal_to(True)))
    assert_that(domain_instance.comment(lang="en"), contains_inanyorder(comment))


def test_valid_property_assigment_for_a_subclass_instance_work():
    ontology = create_ontology()
    domain_instance = ontology.GovernmentOrganization(
        label="Acme Inc.",
    )
    range_instance = ontology.Person(
        label="John Doe",
    )
    domain_instance.hasEmployee += range_instance

    assert_that(domain_instance.hasEmployee(range_instance), is_(True))


def test_valid_sub_property_assigment_for_a_subclass_instance_work():
    ontology = create_ontology()
    domain_instance = ontology.GovernmentOrganization(
        label="Acme Inc.",
    )
    range_instance = ontology.Person(
        label="John Doe",
    )
    domain_instance.hasExecutive += range_instance

    assert_that(domain_instance.hasExecutive(range_instance), is_(True))
    # assert_that(domain_instance.hasEmployee(range_instance), is_(True))


@skip("TODO")
def test_direct_assigment_for_a_class_instance_property_raises_value_error():
    ontology = create_ontology()
    domain_instance = ontology.Organization(
        label="Acme Inc.",
    )

    def invalid_assigment_clause():
        domain_instance.hasEmployee = "some-value"

    assert_that(calling(invalid_assigment_clause), raises(ValueError))


def test_invalid_domain_property_assigment_for_a_class_instance_raises_value_error():
    ontology = create_ontology()
    domain_instance = ontology.Organization(
        label="Acme Inc.",
    )
    range_instance = ontology.Country(
        label="UnitedStates",
    )

    def invalid_assigment_clause():
        domain_instance.hasEmployee += range_instance

    assert_that(calling(invalid_assigment_clause), raises(ValueError))


def test_nonexistant_property_language_tag_returns_none():
    ontology = create_ontology()
    instance = ontology.Organization(label="Acme Inc.")

    assert_that(instance.label(lang="foo"), is_(equal_to(None)))


def test_instance_rdf_statements_are_valid():
    ontology = create_ontology()
    instance = ontology.Organization(label="Acme Inc.")

    statements = list(instance.iter_rdf_statements())
    assert_that(statements, has_length(1))
