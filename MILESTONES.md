# Milestones from the public build log

[← Profile](README.md) · [Engineering notes](BUILD_NOTES.md)

These are dated releases, commits and documented validation events. Dates describe the linked public evidence, not an assumed project start or first-ever achievement.

## 7 June 2026 — A public Mac download

**ClickTrack v1.0.2** was published as the notarized legacy Pro build. The release distinguishes it from the newer license-key implementation.

[Release and downloadable artifact](https://github.com/phlppgdfry/ClickTrack/releases/tag/v1.0.2)

## 28 July 2026 — Android runtime evidence

DocuRelay's Android emulator workflow was documented: APK installation, launch, API access and queue interaction.

[Documentation commit](https://github.com/phlppgdfry/docurelay-field/commit/5b7d5e1c9477864c03f202b2b63aed2efa4012cb)

## 29 July 2026 — Fix, rebuild, verify

A fresh DocuRelay runtime check documented the post-fix SQLite query and a document reaching **Completed** through the API, outbox and worker.

[Runtime validation](https://github.com/phlppgdfry/docurelay-field/blob/main/docs/runtime-validation.md) · [Existing recorded walkthrough](assets/docurelay-demo.gif)

## 8 September 2026 — Reviewable operational actions

PortOps added procedure retrieval and durable human-reviewed action proposals. The prototype keeps operational evidence, draft preparation and approval distinct.

[Implementation commit](https://github.com/phlppgdfry/portops-ai/commit/e622656fdd6baf717e5a5c986f9c73382e2f8058)

## 12 October 2026 — Three packages and two public boards

PortOps.Contracts (NuGet), Logistics KPI Utils (npm) and the Shipment Tracking API (container) were published as previews, each with documentation, automated checks and a release. Two public Projects track the work from issue to release.

[NuGet release](https://github.com/phlppgdfry/portops-ai/releases/tag/contracts-v0.1.0) · [npm release](https://github.com/phlppgdfry/logistics-kpi-utils/releases/tag/v0.1.0) · [Container release](https://github.com/phlppgdfry/shipment-tracking-platform/releases/tag/package-v0.1.0) · [Logistics Operations Roadmap](https://github.com/users/phlppgdfry/projects/6)

## 12 October 2026 — Packages working together in Shipment Desk

Version 0.2.0 of all three packages powers one connected demo: create a synthetic shipment, record arrival evidence and a hold, upload a document, release the hold and read the KPIs, through the real API and SQL Server. Customer scope is enforced across queries, caches, documents and replays.

[Demo and recording](https://github.com/phlppgdfry/shipment-tracking-platform/blob/master/docs/DEMO.md) · [Verification and limitations](https://github.com/phlppgdfry/shipment-tracking-platform/blob/master/docs/VERIFICATION.md) · [Repeatable CI run](https://github.com/phlppgdfry/shipment-tracking-platform/actions/runs/38315102599)

## 12 October 2026 — Yard Pulse v1.0.0

The first stable release of a Power Apps code component that draws a whole yard as one live heatmap, shipped as a Dataverse solution with tests and a live demo.

[Release](https://github.com/phlppgdfry/pcf-yard-pulse/releases/tag/v1.0.0) · [Live demo](https://phlppgdfry.github.io/pcf-yard-pulse/)

## 12 October 2026 — Storm Night, a business analysis you can run

A disruption case for a fictional RoRo operator, backed by a simulation of 200 storm nights and 16 executable allocation rules. CI checks that the numbers in the documents match the model.

[Case](https://github.com/phlppgdfry/storm-night-disruption-business-analysis) · [War room tour](https://phlppgdfry.github.io/storm-night-disruption-business-analysis/war-room/?tour)

## 13 October 2026 — An AI mailbox design tested in CI

The logistics AI and automation case compares a naive agent with a guarded design on a 48-email evaluation set. The guarded design (the model reads, the rules decide) passes all 48 with zero harmful replies, and CI enforces it.

[Case](https://github.com/phlppgdfry/logistics-ai-automation-case-study) · [2-minute demo](https://phlppgdfry.github.io/logistics-ai-automation-case-study/demo/?tour)

## What belongs here next?

A real-model evaluation, a validated device build, a published app update, or a completed data pipeline — once there is a release, test report or other evidence to link.
