# fixture_expected: pass -- a dynamic members dict is a coverage note, not a strict failure (record-set producers build members dynamically).
def write(data_root, members):
    data_root.append_record_set(
        subtree="derived",
        raw_anchor="anchor",
        record_id="r.json",
        members=members,
        completion_lane="silver__cleaning__product_mentions__set",
    )
