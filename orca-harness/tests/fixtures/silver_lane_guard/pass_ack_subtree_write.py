# fixture_expected: pass
"""An acknowledgements-subtree write is an ack record (consumption seam), not a
silver derived record: even a silver_envelope lane NAME used as an ack namespace
is exempt when the subtree statically resolves to "acknowledgements"."""

_ACK_SUBTREE = "acknowledgements"


def ack_with_envelope_lane_namespace(data_root, raw_anchor, record_id, data):
    data_root.append_record(
        subtree=_ACK_SUBTREE,
        raw_anchor=raw_anchor,
        lane="creator_metric_silver",
        record_id=record_id,
        data=data,
    )
