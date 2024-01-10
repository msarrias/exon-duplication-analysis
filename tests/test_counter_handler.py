from unittest.mock import Mock
from exonize.counter_handler import CounterHandler
from exonize.blast_searcher import BLASTsearcher
import portion as P

blast_engine = BLASTsearcher(
    data_container=Mock(),
    masking_percentage_threshold=0.8,
    sleep_max_seconds=40,
    self_hit_threshold=0.5,
    min_exon_length=20,
    cds_overlapping_threshold=0.8,
    evalue_threshold=1e-5,
    debug_mode=False,
)
counter_handler = CounterHandler(
    blast_engine=blast_engine,
    cds_overlapping_threshold=0.8,
)


def test_get_candidate_reference_dictionary():
    pass


def test_get_overlapping_clusters():
    # Case 1: Overlapping intervals
    target_coordinates_set_1 = {
        (P.open(0, 50), 0.9),
        (P.open(40, 100), 0.8),
        (P.open(200, 300), 0.7)
    }
    expected_clusters_1 = [
        [(P.open(0, 50), 0.9), (P.open(40, 100), 0.8)],
        [(P.open(200, 300), 0.7)]
    ]

    # Case 2: Non-overlapping intervals
    target_coordinates_set_2 = {
        (P.open(0, 50), 0.9),
        (P.open(60, 110), 0.8),
        (P.open(120, 170), 0.7)
    }
    expected_clusters_2 = [
        [(P.open(0, 50), 0.9)],
        [(P.open(60, 110), 0.8)],
        [(P.open(120, 170), 0.7)]
    ]

    # Test and assert
    assert counter_handler.get_overlapping_clusters(
        target_coordinates_set=target_coordinates_set_1,
        threshold=0
    ) == expected_clusters_1
    assert counter_handler.get_overlapping_clusters(
        target_coordinates_set=target_coordinates_set_2,
        threshold=0.
    ) == expected_clusters_2


def test_build_reference_dictionary():
    cds_candidates_dictionary = {
        'candidates_cds_coordinates':
            [P.open(0, 100),
             P.open(200, 250)]
    }
    clusters_list = [
        [(P.open(0, 50), 0.9), (P.open(40, 90), 0.8)],
        [(P.open(200, 250), 0.7), (P.open(220, 270), 0.6)],
        [(P.open(400, 450), 0.5)]  # Non-overlapping interval
    ]

    expected_output = {
        P.open(0, 50):
            {'reference_coordinate': P.open(0, 50), 'reference_type': 'coding'},
        P.open(40, 90):
            {'reference_coordinate': P.open(40, 90), 'reference_type': 'coding'},
        P.open(200, 250):
            {'reference_coordinate': P.open(200, 250), 'reference_type': 'coding'},
        P.open(220, 270):
            {'reference_coordinate': P.open(220, 270), 'reference_type': 'non_coding'},
        P.open(400, 450):
            {'reference_coordinate': P.open(400, 450), 'reference_type': 'non_coding'}  # Assuming no CDS overlap
    }

    assert counter_handler.build_reference_dictionary(
        cds_candidates_dictionary=cds_candidates_dictionary,
        clusters_list=clusters_list
    ) == expected_output


def test_assign_event_ids():
    pass
