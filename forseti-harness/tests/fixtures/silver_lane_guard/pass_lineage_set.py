# fixture_expected: pass -- a declared silver_lineage set; no envelope front-door required.
def write(data_root):
    data_root.append_record_set(
        subtree="derived",
        raw_anchor="anchor",
        record_id="r.json",
        members={"silver__cleaning__product_mentions": b"{}\n"},
        completion_lane="silver__cleaning__product_mentions__set",
    )
