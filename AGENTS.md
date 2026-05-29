# AGENTS.md

## Orca Project Instructions

Before project work, read `.agents/workflow-overlay/README.md` and follow the Orca overlay. If required overlay authority is missing or ambiguous, fail visibly and report the missing source instead of substituting defaults.

Keep Orca project facts, constraints, artifact folders, review lanes, validation gates, and safety rules in `.agents/workflow-overlay/`. Do not treat `jb` rules, paths, handoffs, lifecycle mechanics, product policy, or validation habits as Orca authority.

Doctrine-changing Orca work must not finish by updating only the immediate authority document. If the current turn changes product doctrine, architecture doctrine, workflow authority, validation philosophy, review authority, output authority, or lifecycle boundaries, update the controlling Orca source, check downstream source-loaded surfaces, and close with an inline `direction_change_propagation` receipt or explicit blocker under `.agents/workflow-overlay/source-of-truth.md`. Do not create a new skill, registry, standalone receipt file, broad template sweep, or automation for this loop unless a later turn explicitly authorizes it.

Orca is no longer globally docs-first by default. Documentation remains the authority layer for project facts, decisions, prompts, reviews, migration notes, and overlay maintenance, but a later turn may explicitly authorize bounded implementation, automation, packages, tests, generated artifacts, or runtime work. Do not create those from planning, review, or product-method work unless the current turn or an accepted handoff explicitly authorizes that bounded implementation scope.

Do not install, uninstall, rename, rewrite, or shadow global/user/plugin skills unless a later turn explicitly authorizes that workflow-kernel action. Do not edit workflow-kernel source or deployment copies from Orca project work.

Allowed project work by default is documentation, decisions, prompts, reviews, migration notes, and overlay maintenance inside this workspace. Implementation or runtime work requires explicit bounded authorization in the current turn or accepted handoff.
