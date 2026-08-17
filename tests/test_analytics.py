from analytics import generate_operations_data, add_metrics, bottleneck_summary


def test_generation_reproducible():
    assert generate_operations_data(100, 42).equals(generate_operations_data(100, 42))


def test_metrics_binary_and_nonnegative():
    d = add_metrics(generate_operations_data(100, 42))
    assert set(d.sla_breach.unique()) <= {0, 1}
    assert (d.delay_hours >= 0).all()


def test_summary_has_all_processes():
    s = bottleneck_summary(generate_operations_data(500, 42))
    assert len(s) == 3
    assert s.sla_breach_rate.between(0, 1).all()
