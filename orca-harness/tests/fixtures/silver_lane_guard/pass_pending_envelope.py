# fixture_expected: pass -- raw write to an envelope lane listed in FRONT_DOOR_PENDING (named baseline).
def write(data_root):
    data_root.append_record(
        subtree="derived",
        raw_anchor="anchor",
        lane="creator_metric_silver",
        record_id="r.json",
        data=b"{}\n",
    )
