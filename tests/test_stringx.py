import stringx


def test_map_identifiers():
    identifiers = stringx.map_identifiers(["edin"], 7227)

    assert len(identifiers) == 1

    for id_ in identifiers:
        keys = id_.keys()
        assert "queryIndex" in keys
        assert "queryItem" in keys
        assert "stringId" in keys
        assert "ncbiTaxonId" in keys
        assert "taxonName" in keys
        assert "preferredName" in keys
        assert "annotation" in keys
        assert "annotation" in keys


def test_network():
    network = stringx.network(["edin", "atta", "attc"], 7227)

    assert len(network) == 3

    for id_ in network:
        keys = id_.keys()
        assert "stringId_A" in keys
        assert "stringId_B" in keys
        assert "preferredName_A" in keys
        assert "preferredName_B" in keys
        assert "ncbiTaxonId" in keys
        assert "score" in keys
        assert "nscore" in keys
        assert "fscore" in keys
        assert "pscore" in keys
        assert "ascore" in keys
        assert "escore" in keys
        assert "dscore" in keys
        assert "tscore" in keys


def test_interaction_partners():
    interaction_partners = stringx.interaction_partners(["edin"], 7227)

    assert len(interaction_partners) > 1

    for id_ in interaction_partners:
        keys = id_.keys()
        assert "stringId_A" in keys
        assert "stringId_B" in keys
        assert "preferredName_A" in keys
        assert "preferredName_B" in keys
        assert "ncbiTaxonId" in keys
        assert "score" in keys
        assert "nscore" in keys
        assert "fscore" in keys
        assert "pscore" in keys
        assert "ascore" in keys
        assert "escore" in keys
        assert "dscore" in keys
        assert "tscore" in keys
