# Notes from the build

[← Profile](README.md) · [Milestones](MILESTONES.md) · [Professional](PROFESSIONAL.md)

Four engineering lessons, linked to the work that prompted them. The “next time” notes below are design takeaways from that evidence.

## 01 — Offline is a workflow

**Project:** [DocuRelay Field](https://github.com/phlppgdfry/docurelay-field)

A field worker should be able to capture a document, see that it is queued, and retry its upload when connectivity returns. This makes persistence and status part of the user experience.

The project uses SQLite for durable local state and a visible upload queue. The local API, outbox and worker give the document a traceable path to completion.

**The awkward case:** an enum `ToString()` expression was translated into a SQLite function that did not exist. Passing the enum value as a query parameter addressed the translation problem. A new Android capture then demonstrated the corrected workflow.

**Next time:** inspect the generated query and exercise the actual runtime path early. A successful build alone cannot establish that a mobile database query works.

[Runtime validation and correction](https://github.com/phlppgdfry/docurelay-field/blob/main/docs/runtime-validation.md) · [Offline sync design](https://github.com/phlppgdfry/docurelay-field/blob/main/docs/offline-sync.md)

## 02 — The archive is part of the product

**Project:** [ClickTrack](https://github.com/phlppgdfry/ClickTrack)

Code, packaging and distribution are separate milestones. The public v1.0.2 download is a notarized legacy Pro build. The newer license-key implementation needs its own signed and notarized archive before it replaces that download.

**The trade-off:** keep a known downloadable artifact available while describing the newer workstream precisely. That means release notes, download links and feature claims must describe the same build.

**Next time:** treat the release artifact and its installation path as acceptance criteria. “Implemented” and “available in the current download” deserve different checkboxes.

[Public release notes](https://github.com/phlppgdfry/ClickTrack/releases/tag/v1.0.2) · [Distribution notes](https://github.com/phlppgdfry/ClickTrack/blob/main/docs/DISTRIBUTION.md)

## 03 — Readiness needs a definition

**Project:** [PortOps AI](https://github.com/phlppgdfry/portops-ai)

A vehicle can be discharged without being ready for pickup. Loading readiness is another decision again. Observations can be stale or contradictory, and a model should not smooth those differences into a reassuring sentence.

**The design choice:** explicit domain rules, separate readiness decisions, source IDs, timestamps and scoped tools. Drafting an action is separate from approving it, and the current delivery adapter is simulated.

**Next time:** define evidence and approval boundaries before adding more conversational features. Test conflicting and missing records, not only the happy path.

[Architecture decisions](https://github.com/phlppgdfry/portops-ai/blob/main/docs/architecture.md) · [Current implementation](https://github.com/phlppgdfry/portops-ai)

## 04 — Let the data story be inspectable

**Project:** [Fabric Data Platform](https://github.com/phlppgdfry/fabric-lottery-data-platform)

A data platform is easier to understand when its raw inputs, transformations and business outputs are distinct. This learning build uses synthetic lottery-style events and a Bronze/Silver/Gold architecture.

**The design choice:** publish the architecture and staged build plan while identifying the repository as an early scaffold. The plan describes the destination; it is not proof that every layer is already complete.

**Next time:** show the data contract, quality checks and lineage alongside the diagram as the implementation develops.

[Architecture, synthetic data and current scope](https://github.com/phlppgdfry/fabric-lottery-data-platform)

---

[Back to the museum](README.md#museum-of-questionable-decisions) · [Browse all projects](PROJECTS.md)
