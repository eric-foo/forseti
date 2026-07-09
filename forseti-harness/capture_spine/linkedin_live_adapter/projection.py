"""LinkedIn live-adapter -- slice 3b-2 projection (no runtime).

The MINT-PATH from a minimized ``LiveObservation`` to a core ``CandidateRow``.
Mirrors the ``reddit_candidate_intake`` projection/writer pattern (build a frozen
dataclass row -> ``to_dict`` -> ``validate``), so the one exported function
returns ONLY a ``validate_candidate_row``-passing dict; there is no other adapter
door that emits a candidate row. This is the checkable adapter-API invariant (the
architecture mint-path), NOT an unreachable-constructor claim.

It also BINDS the observation to its posture: the projection requires a VALIDATED
``LiveAccessEnvelope`` and a ``RunEnvelope`` whose ids match the observation
(``live_access_id`` + ``run_id``). This closes the slice-3b deferral (F3): the
observation alone is the shape gate; the candidate row is minted only against a
validated access posture.

Inputs the observation does NOT carry are supplied explicitly (mirroring reddit's
explicit-kwarg projection): the run context comes from the ``RunEnvelope``
(declared_theme, run_purpose) and the two operator judgments -- ``candidate_class``
and ``business_relevance_note`` -- are passed in. ``candidate_class`` and the
observed source surface must be DECLARED in the ``RunEnvelope`` (no minting a
class/surface the run did not declare). A field with no ``CandidateRow`` target
(e.g. ``observed_location_or_none``) is dropped, not smuggled.

Closed-enum validity is deferred to ``validate_candidate_row`` (the single gate):
``validate_live_observation`` does not closed-enum-check ``minimization_rule`` /
``person_data_minimized``, so the projection passes those (and the other
enumerated fields) through as STRING values and lets the core validator reject a
bad value with a ``LinkedInLaneError`` code -- pre-converting to enums here would
raise a bare ``ValueError`` of the wrong type.
"""
from __future__ import annotations

from typing import Any

from capture_spine.linkedin_lane.models import (
    CandidateClass,
    CandidateRow,
    EntityType,
    LinkedInLaneError,
    MethodMode,
    PrivacySensitivity,
    RunEnvelope,
    VisibleInfluenceNumbers,
)
from capture_spine.linkedin_lane.shared_validation import validate_visible_influence_value
from capture_spine.linkedin_lane.validation import (
    validate_candidate_row,
    validate_run_envelope,
)
from capture_spine.linkedin_live_adapter.models import (
    LiveAccessEnvelope,
    LiveAccessMode,
    LiveObservation,
)
from capture_spine.linkedin_live_adapter.validation import (
    validate_live_access_envelope,
    validate_live_observation,
)


# LiveAccessMode -> MethodMode. Fail-closed: a mode with no mapping raises rather
# than defaulting to a permissive method_mode.
_ACCESS_MODE_TO_METHOD_MODE: dict[str, str] = {
    LiveAccessMode.ATTENDED_MANUAL.value: MethodMode.MANUAL_OPERATOR_BROWSING.value,
    LiveAccessMode.OWNER_PRESENT_ATTENDED_AUTOMATION.value: (
        MethodMode.OWNER_PRESENT_ATTENDED_AUTOMATION_OPTIONAL_POC_RISK.value
    ),
}

# entity_type -> privacy_sensitivity. A person observation has already cleared the
# public-actor-basis gate (validate_live_observation), so PUBLIC_ACTOR_STRICT is
# the person default; business / organization are BUSINESS_LOW.
_ENTITY_TYPE_TO_PRIVACY_SENSITIVITY: dict[str, str] = {
    EntityType.BUSINESS_ENTITY.value: PrivacySensitivity.BUSINESS_LOW.value,
    EntityType.ORGANIZATION_ENTITY.value: PrivacySensitivity.BUSINESS_LOW.value,
    EntityType.INDIVIDUAL_PERSON.value: PrivacySensitivity.PUBLIC_ACTOR_STRICT.value,
}


def project_observation_to_candidate_row(
    *,
    observation: LiveObservation,
    access_envelope: LiveAccessEnvelope,
    run_envelope: RunEnvelope,
    candidate_class: CandidateClass | str,
    business_relevance_note: str,
) -> dict[str, Any]:
    """Mint one validated ``CandidateRow`` dict from a minimized observation.

    Validates the observation (shape gate), the access envelope (posture gate),
    and the run envelope; binds them by matching ``live_access_id`` + ``run_id``;
    then builds, serializes, and validates the candidate row. Returns ONLY a dict
    that has passed ``validate_candidate_row``. Raises ``LinkedInLaneError`` on any
    shape, posture, binding, declaration, mapping, or candidate-row failure.
    """
    # 1. Validate each input under its own gate (no trust without validation).
    validate_live_observation(observation.to_dict())
    validate_live_access_envelope(access_envelope.to_dict())
    validate_run_envelope(run_envelope)

    # 2. Bind the observation to its posture: ids must match a validated envelope.
    if observation.live_access_id != access_envelope.live_access_id:
        raise LinkedInLaneError(
            "live_access_id_mismatch",
            "observation.live_access_id must match the access envelope (posture binding)",
        )
    if not (observation.run_id == access_envelope.run_id == run_envelope.run_id):
        raise LinkedInLaneError(
            "run_id_mismatch",
            "observation / access envelope / run envelope run_id must all match",
        )

    # 3. Resolve the operator judgments against the run's declared envelope (no
    #    minting a class or surface the run did not declare).
    candidate_class_value = str(candidate_class)
    if candidate_class_value not in {str(c) for c in run_envelope.candidate_classes}:
        raise LinkedInLaneError(
            "candidate_class_not_declared",
            "candidate_class must be declared in run_envelope.candidate_classes",
        )
    if observation.observed_source_surface not in {str(s) for s in run_envelope.source_surface_allowlist}:
        raise LinkedInLaneError(
            "source_surface_not_declared",
            "observed_source_surface must be declared in run_envelope.source_surface_allowlist",
        )

    # 4. Map access mode + entity type to their core values (fail-closed).
    method_mode_value = _ACCESS_MODE_TO_METHOD_MODE.get(str(access_envelope.live_access_mode))
    if method_mode_value is None:
        raise LinkedInLaneError(
            "unmappable_live_access_mode",
            "live_access_mode has no method_mode mapping (fail-closed)",
        )
    privacy_sensitivity_value = _ENTITY_TYPE_TO_PRIVACY_SENSITIVITY.get(observation.observed_entity_type)
    if privacy_sensitivity_value is None:
        raise LinkedInLaneError(
            "unmappable_entity_type",
            "observed_entity_type has no privacy_sensitivity mapping (fail-closed)",
        )

    # 5. Carry the minimized visible influence signal when present (counts / coarse
    #    bands only -- the observation never carries a list or free-text body). The
    #    shared count/band guard runs at BOTH the observation gate and here at the
    #    mint-path (defense-in-depth; cross-vendor review F1).
    validate_visible_influence_value(
        "visible_follower_count_or_none", observation.visible_follower_count_or_none
    )
    validate_visible_influence_value(
        "visible_connection_count_band_or_none",
        observation.visible_connection_count_band_or_none,
    )
    influence_numbers = None
    if (
        observation.visible_follower_count_or_none is not None
        or observation.visible_connection_count_band_or_none is not None
    ):
        influence_numbers = VisibleInfluenceNumbers(
            follower_count_or_none=observation.visible_follower_count_or_none.strip()
            if observation.visible_follower_count_or_none is not None
            else None,
            connection_count_band_or_none=observation.visible_connection_count_band_or_none.strip()
            if observation.visible_connection_count_band_or_none is not None
            else None,
        )

    # 6. Build the candidate row. Fixed values (source_family, intake_status,
    #    planning_only, promotion_required) come from the CandidateRow defaults;
    #    the retained/captured flags stay False (already attested False on the
    #    observation). Enumerated fields are passed as strings (step note above).
    row = CandidateRow(
        candidate_id=f"cand:{observation.observation_id}",
        run_id=observation.run_id,
        candidate_class=candidate_class_value,
        entity_type=observation.observed_entity_type,
        display_name=observation.observed_display_name,
        source_surface=observation.observed_source_surface,
        source_policy_posture=access_envelope.source_policy_posture,
        method_mode=method_mode_value,
        declared_theme_or_decision_context=run_envelope.declared_theme_or_decision_context,
        run_purpose=run_envelope.run_purpose,
        business_relevance_note=business_relevance_note,
        privacy_sensitivity=privacy_sensitivity_value,
        minimization_rule=observation.minimization_rule,
        person_data_minimized=observation.person_data_minimized,
        provenance_timestamp=observation.provenance_timestamp,
        optional_poc_risk_mode=access_envelope.optional_poc_risk_mode,
        canonical_locator_or_none=observation.observed_source_locator,
        source_locators=(observation.observed_source_locator,),
        role_or_influence_basis_or_none=observation.observed_public_role_or_title_or_none,
        senior_role_or_public_actor_basis_or_none=observation.senior_role_or_public_actor_basis_or_none,
        visible_influence_numbers_or_none=influence_numbers,
    )

    # 7. Mint-path: serialize + validate; return ONLY a validated dict.
    row_dict = row.to_dict()
    validate_candidate_row(row_dict)
    return row_dict
