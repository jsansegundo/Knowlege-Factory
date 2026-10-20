import registry


CORPUS_METADATA = {
    (
        "02- Frontier Accelerate for Security Envisioning "
        "and POC - Engagement Guide.pptx"
    ): {
        "source_authority": "microsoft_program",
        "program": "Frontier Accelerate",
        "document_role": "Engagement Guide",
        "canonical_status": "canonical",
        "fiscal_year": "FY27",
        "language": "en",
        "audience": "partner-only",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current product, licensing, preview "
            "and availability guidance before execution."
        ),
    },

    (
        "03 - Frontier Accelerate for Security "
        "Envisioning and POC - FAQ.docx"
    ): {
        "source_authority": "microsoft_program",
        "program": "Frontier Accelerate",
        "document_role": "FAQ",
        "canonical_status": "canonical",
        "fiscal_year": "FY27",
        "language": "en",
        "audience": "partner-only",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current program and product guidance "
            "before execution."
        ),
    },

    (
        "05 - Frontier Accelerate for Security "
        "Envisioning and POC - Zero Trust Workshop "
        "Delivery Guide for Frontier Accelerate.docx"
    ): {
        "source_authority": "microsoft_program",
        "program": "Zero Trust",
        "document_role": "Master Guide",
        "canonical_status": "canonical",
        "fiscal_year": "FY27",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current Zero Trust assessment, "
            "licensing and product guidance."
        ),
    },

    "DS-00-MasterDeliveryGuide - v8.5.docx": {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Master Guide",
        "canonical_status": "canonical",
        "version": "v8.5",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current Microsoft Purview licensing, "
            "portal paths and feature availability."
        ),
    },

    (
        "00 - Cloud Security Envisioning Workshop "
        "- Delivery Guide.docx"
    ): {
        "source_authority": "microsoft_program",
        "program": "CSEW",
        "document_role": "Master Guide",
        "canonical_status": "canonical",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current Defender for Cloud plans, "
            "pricing, portal paths and previews."
        ),
    },

    (
        "00 - Modern SecOps Envisioning Workshop "
        "- Delivery Guide.docx"
    ): {
        "source_authority": "microsoft_program",
        "program": "MSOEW",
        "document_role": "Master Guide",
        "canonical_status": "canonical",
        "version": "v7.2",
        "release_date": "2026-07",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current Microsoft Sentinel, "
            "Defender XDR, licensing and onboarding guidance."
        ),
    },

    (
        "00 - Threat Protection Envisioning Workshop "
        "- Delivery Guide.docx"
    ): {
        "source_authority": "microsoft_program",
        "program": "TPEW",
        "document_role": "Master Guide",
        "canonical_status": "canonical",
        "version": "v7.2",
        "release_date": "2026-07",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current Defender product compatibility, "
            "licensing and onboarding guidance."
        ),
    },

    (
        "Microsoft Commercial Partner Incentives Guide "
        "- es-ES - 20260702.pdf"
    ): {
        "source_authority": "microsoft_program",
        "program": "Incentives",
        "document_role": "Master Guide",
        "canonical_status": "canonical",
        "release_date": "2026-07-02",
        "language": "es-ES",
        "audience": "partner-only",
        "volatility": "high-change",
        "validation_required": (
            "Confirm that this remains the current incentives "
            "guide before using eligibility or claim rules."
        ),
    },

    # Alias utilizado actualmente por el entorno local.
    "incentives.pdf": {
        "source_authority": "microsoft_program",
        "program": "Incentives",
        "document_role": "Master Guide",
        "canonical_status": "canonical",
        "language": "es-ES",
        "audience": "partner-only",
        "volatility": "high-change",
        "validation_required": (
            "Confirm the exact publication date and that this "
            "remains the current incentives guide."
        ),
    },

    # Adaptación interna de SEIDOR para facilitar la sesión.
    "Preparación sesión Zero Trust Workshop.docx": {
        "source_authority": "seidor_adaptation",
        "program": "Zero Trust",
        "document_role": "Module Guide",
        "canonical_status": "derived",
        "language": "es",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Validate technical, licensing and product guidance "
            "against the current official Zero Trust and product "
            "documentation before customer delivery."
        ),
    },
}

SECOND_BATCH_METADATA = {
    # ---------------------------------------------------------
    # Frontier Accelerate: supporting communication assets
    # ---------------------------------------------------------
    (
        "01 - Frontier Accelerate for Security Envisioning "
        "and POC - Introduction.pptx"
    ): {
        "source_authority": "microsoft_program",
        "program": "Frontier Accelerate",
        "document_role": "Deck",
        "canonical_status": "subordinate",
        "version": "v1.0",
        "release_date": "2026-07",
        "fiscal_year": "FY27",
        "language": "en",
        "audience": "partner-only",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm that the latest Frontier Accelerate "
            "toolkit version is being used."
        ),
    },

    (
        "04 - Frontier Accelerate for Security Envisioning "
        "and POC - Pre-sales.pptx"
    ): {
        "source_authority": "microsoft_program",
        "program": "Frontier Accelerate",
        "document_role": "Deck",
        "canonical_status": "subordinate",
        "version": "v1.0",
        "release_date": "2026-07",
        "fiscal_year": "FY27",
        "language": "en",
        "audience": "commercial",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current domains, module availability "
            "and product guidance before customer delivery."
        ),
    },

    # ---------------------------------------------------------
    # Zero Trust: SEIDOR delivery adaptations
    # ---------------------------------------------------------
    "Zero Trust Workshop Kickoff FY27.pptx": {
        "source_authority": "seidor_adaptation",
        "program": "Zero Trust",
        "document_role": "Deck",
        "canonical_status": "derived",
        "release_date": "2026-09",
        "fiscal_year": "FY27",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Validate workshop area names, assessment behavior "
            "and deliverables against the official Zero Trust "
            "Workshop Delivery Guide."
        ),
    },

    "Guía técnica Zero Trust Workshop en el tenant del cliente.docx": {
        "source_authority": "seidor_adaptation",
        "program": "Zero Trust",
        "document_role": "Module Guide",
        "canonical_status": "derived",
        "language": "es",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Validate installation, authentication, permissions "
            "and assessment instructions against current official "
            "Zero Trust and product documentation."
        ),
    },

    # ---------------------------------------------------------
    # Data Security: official module delivery guides
    # ---------------------------------------------------------
    "DS-01-Module Delivery Guide-Exchange - v8.5.1.docx": {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Module Guide",
        "canonical_status": "subordinate",
        "version": "v8.5.1",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current Exchange, Purview, eDiscovery "
            "and DLP guidance before execution."
        ),
    },

    "DS-02-Module Delivery Guide-SharePoint - v8.5.docx": {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Module Guide",
        "canonical_status": "subordinate",
        "version": "v8.5",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current SharePoint, OneDrive, Purview "
            "and eDiscovery guidance before execution."
        ),
    },

    "DS-03-Module Delivery Guide-Teams - v8.5.1.docx": {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Module Guide",
        "canonical_status": "subordinate",
        "version": "v8.5.1",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current Teams, Purview, licensing "
            "and policy guidance before execution."
        ),
    },

    (
        "DS-04-Module Delivery Guide-Insider Risk Discovery "
        "- v8.5.1.docx"
    ): {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Module Guide",
        "canonical_status": "subordinate",
        "version": "v8.5.1",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current Insider Risk Management policies, "
            "connectors, indicators and licensing."
        ),
    },

    (
        "DS-05-Module Delivery Guide-Compliance Manager- "
        "v8.5.docx"
    ): {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Module Guide",
        "canonical_status": "subordinate",
        "version": "v8.5",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current Compliance Manager templates, "
            "assessment behavior and licensing."
        ),
    },

    "DS-06-Module Delivery Guide-On-premises - v8.5.docx": {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Module Guide",
        "canonical_status": "subordinate",
        "version": "v8.5",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current scanner prerequisites, supported "
            "repositories and configuration procedures."
        ),
    },

    (
        "DS-07-Module Delivery Guide-Windows Endpoints "
        "- v8.5.1.docx"
    ): {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Module Guide",
        "canonical_status": "subordinate",
        "version": "v8.5.1",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current Endpoint DLP prerequisites, "
            "policy behavior and licensing."
        ),
    },

    (
        "DS-08-Module Delivery Guide-Communication Compliance "
        "- v8.5.docx"
    ): {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Module Guide",
        "canonical_status": "subordinate",
        "version": "v8.5",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current Communication Compliance scenarios, "
            "policy behavior and licensing."
        ),
    },

    (
        "DS-09-Module Delivery Guide-Data security for AI "
        "- v8.5.1.docx"
    ): {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Module Guide",
        "canonical_status": "subordinate",
        "version": "v8.5.1",
        "language": "en",
        "audience": "delivery",
        "volatility": "high-change",
        "validation_required": (
            "Confirm the current DSPM for AI experience because "
            "the documented classic experience may be superseded."
        ),
    },

    # ---------------------------------------------------------
    # Data Security: decks, templates and change history
    # ---------------------------------------------------------
    "DS-12-Pre-sales Call - v8.5.pptx": {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Deck",
        "canonical_status": "subordinate",
        "version": "v8.5",
        "language": "en",
        "audience": "commercial",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current module availability, scope "
            "and licensing before customer delivery."
        ),
    },

    "DS-40-Pre-Engagement and Kickoff deck - v8.5.pptx": {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Deck",
        "canonical_status": "subordinate",
        "version": "v8.5",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Replace customer placeholders and remove or hide "
            "sample and non-delivered module content."
        ),
    },

    "DS-41-Close-out deck - v8.5.pptx": {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Deck",
        "canonical_status": "subordinate",
        "version": "v8.5",
        "language": "en",
        "audience": "customer",
        "volatility": "evergreen",
        "validation_required": (
            "Replace every placeholder and sample illustration "
            "with validated customer findings before delivery."
        ),
    },

    "DS-42-Close-out deck COMPACT - v8.5.pptx": {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Deck",
        "canonical_status": "derived",
        "version": "v8.5",
        "language": "en",
        "audience": "executive",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm that all findings and recommendations come "
            "from validated customer evidence and remove samples."
        ),
    },

    "DS-64-Employee Resignations Simulation Template - v8.5.xlsx": {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Template",
        "canonical_status": "sample",
        "version": "v8.5",
        "language": "en",
        "audience": "delivery",
        "volatility": "stable",
        "validation_required": (
            "Replace all sample identities and dates before use. "
            "Never treat sample rows as customer evidence."
        ),
    },

    "_Changelog version - v8.5.1.pdf": {
        "source_authority": "microsoft_program",
        "program": "DSEW",
        "document_role": "Changelog",
        "canonical_status": "subordinate",
        "version": "v8.5.1",
        "language": "en",
        "audience": "delivery",
        "volatility": "stable",
        "validation_required": (
            "Use the changelog to understand version changes, "
            "not as a substitute for the delivery guides."
        ),
    },

    # ---------------------------------------------------------
    # Cloud Security supporting assets
    # ---------------------------------------------------------
    (
        "01 - Cloud Security Envisioning Workshop "
        "- Pre-engagement Call and Kick-off.pptx"
    ): {
        "source_authority": "microsoft_program",
        "program": "CSEW",
        "document_role": "Deck",
        "canonical_status": "subordinate",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Customize customer scope and confirm current "
            "Defender for Cloud guidance."
        ),
    },

    (
        "02 - Cloud Security Envisioning Workshop "
        "- Results and Next Steps.pptx"
    ): {
        "source_authority": "microsoft_program",
        "program": "CSEW",
        "document_role": "Deck",
        "canonical_status": "subordinate",
        "language": "en",
        "audience": "customer",
        "volatility": "evergreen",
        "validation_required": (
            "Replace placeholders and samples with validated "
            "customer findings before presentation."
        ),
    },

    (
        "03 - Cloud Security Envisioning Workshop "
        "- Engagement Overview.pptx"
    ): {
        "source_authority": "microsoft_program",
        "program": "CSEW",
        "document_role": "Deck",
        "canonical_status": "subordinate",
        "language": "en",
        "audience": "commercial",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm current module scope, product plans "
            "and availability before customer delivery."
        ),
    },

    "05 - Cloud Security Envisioning Workshop - FAQ.docx": {
        "source_authority": "microsoft_program",
        "program": "CSEW",
        "document_role": "FAQ",
        "canonical_status": "subordinate",
        "release_date": "2026-02",
        "language": "en",
        "audience": "delivery",
        "volatility": "high-change",
        "validation_required": (
            "Confirm current trial, pricing, multi-cloud, "
            "regional and government-tenant guidance."
        ),
    },

    # ---------------------------------------------------------
    # Modern SecOps supporting assets
    # ---------------------------------------------------------
    (
        "01 - Modern SecOps Envisioning Workshop "
        "- Pre-engagement Call and Kick-off.pptx"
    ): {
        "source_authority": "microsoft_program",
        "program": "MSOEW",
        "document_role": "Deck",
        "canonical_status": "subordinate",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Customize customer scope and confirm current "
            "Sentinel and Defender XDR guidance."
        ),
    },

    (
        "02 - Modern SecOps Envisioning Workshop "
        "- Results and Next Steps.pptx"
    ): {
        "source_authority": "microsoft_program",
        "program": "MSOEW",
        "document_role": "Deck",
        "canonical_status": "subordinate",
        "language": "en",
        "audience": "customer",
        "volatility": "evergreen",
        "validation_required": (
            "Replace all placeholders and samples with "
            "validated customer findings."
        ),
    },

    (
        "10 - Modern SecOps Envisioning Workshop "
        "- Design Decision Points.xlsx"
    ): {
        "source_authority": "microsoft_program",
        "program": "MSOEW",
        "document_role": "Workbook",
        "canonical_status": "subordinate",
        "version": "v7.2",
        "release_date": "2026-07",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm each decision with the customer and verify "
            "current configuration options before implementation."
        ),
    },

    (
        "12 - Modern SecOps Envisioning Workshop "
        "- Top Threats Document.docx"
    ): {
        "source_authority": "microsoft_program",
        "program": "MSOEW",
        "document_role": "Module Guide",
        "canonical_status": "subordinate",
        "language": "en",
        "audience": "delivery",
        "volatility": "high-change",
        "validation_required": (
            "Validate threat descriptions, product mappings "
            "and mitigation guidance before reuse."
        ),
    },

    # ---------------------------------------------------------
    # Threat Protection supporting assets
    # ---------------------------------------------------------
    (
        "01 - Threat Protection Envisioning Workshop "
        "- Pre-engagement Call and Kick-off.pptx"
    ): {
        "source_authority": "microsoft_program",
        "program": "TPEW",
        "document_role": "Deck",
        "canonical_status": "subordinate",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Customize customer scope and verify current "
            "Defender product guidance."
        ),
    },

    (
        "02 - Threat Protection Envisioning Workshop "
        "- Results and Next Steps.pptx"
    ): {
        "source_authority": "microsoft_program",
        "program": "TPEW",
        "document_role": "Deck",
        "canonical_status": "subordinate",
        "language": "en",
        "audience": "customer",
        "volatility": "evergreen",
        "validation_required": (
            "Replace all placeholders and sample findings "
            "with validated customer evidence."
        ),
    },

    (
        "10 - Threat Protection Envisioning Workshop "
        "- Design Decision Points.xlsx"
    ): {
        "source_authority": "microsoft_program",
        "program": "TPEW",
        "document_role": "Workbook",
        "canonical_status": "subordinate",
        "version": "v7.2",
        "release_date": "2026-07",
        "language": "en",
        "audience": "delivery",
        "volatility": "evergreen",
        "validation_required": (
            "Confirm each decision with the customer and verify "
            "current configuration options before implementation."
        ),
    },

    (
        "12 - Threat Protection Envisioning Workshop "
        "- Top Threats Document.docx"
    ): {
        "source_authority": "microsoft_program",
        "program": "TPEW",
        "document_role": "Module Guide",
        "canonical_status": "subordinate",
        "version": "v7.2",
        "release_date": "2026-07",
        "language": "en",
        "audience": "delivery",
        "volatility": "high-change",
        "validation_required": (
            "Validate threat descriptions, detection coverage, "
            "product mappings and mitigation guidance."
        ),
    },

    # ---------------------------------------------------------
    # SEIDOR commercial and facilitation adaptations
    # ---------------------------------------------------------
    "EL CAMBIO REAL (FY26 → FY27).docx": {
        "source_authority": "seidor_adaptation",
        "program": "Frontier Accelerate",
        "document_role": "Engagement Guide",
        "canonical_status": "derived",
        "fiscal_year": "FY27",
        "language": "es",
        "audience": "commercial",
        "volatility": "evergreen",
        "validation_required": (
            "Validate program, incentive and delivery statements "
            "against current official Microsoft documentation."
        ),
    },

    "Propuesta de escenarios a clientes.docx": {
        "source_authority": "seidor_adaptation",
        "program": "Frontier Accelerate",
        "document_role": "Engagement Guide",
        "canonical_status": "derived",
        "fiscal_year": "FY27",
        "language": "es",
        "audience": "commercial",
        "volatility": "stable",
        "validation_required": (
            "Use as conversation guidance only and validate "
            "technical or program claims against official sources."
        ),
    },

    "FY27 Security Discovery Matrix.xlsx": {
        "source_authority": "seidor_adaptation",
        "program": "Frontier Accelerate",
        "document_role": "Workbook",
        "canonical_status": "derived",
        "fiscal_year": "FY27",
        "language": "en",
        "audience": "commercial",
        "volatility": "evergreen",
        "validation_required": (
            "Validate domain mappings and recommended motions "
            "against the current Engagement Guide."
        ),
    },

    "Cuaderno_FY27_Security.docx": {
        "source_authority": "internal_working",
        "program": "Frontier Accelerate",
        "document_role": "Workbook",
        "canonical_status": "derived",
        "fiscal_year": "FY27",
        "language": "es",
        "audience": "commercial",
        "volatility": "evergreen",
        "validation_required": (
            "Treat as internal working material and validate "
            "all program and technical statements before reuse."
        ),
    },
}


CORPUS_METADATA.update(SECOND_BATCH_METADATA)

def apply_catalog_to_registry(registry_data):
    """
    Apply known corpus metadata to documents already present in the Registry.

    Documents are matched by their exact file name. Technical properties such
    as status and indexed_at are not changed.

    Returns a summary containing:
    - assigned: documents that received or changed metadata.
    - unchanged: documents that already had the expected metadata.
    - unmatched: Registry documents absent from the classification catalog.
    - catalog_not_registered: catalog entries absent from the Registry.
    """
    assigned = []
    unchanged = []
    unmatched = []

    documents = registry_data.get("documents", [])

    registered_names = {
        document["file_name"]
        for document in documents
    }

    for document in documents:
        file_name = document["file_name"]
        metadata = CORPUS_METADATA.get(file_name)

        if metadata is None:
            unmatched.append(file_name)
            continue

        if document.get("metadata") == metadata:
            unchanged.append(file_name)
            continue

        assigned_successfully = registry.set_document_metadata(
            registry_data,
            file_name,
            metadata,
        )

        if assigned_successfully:
            assigned.append(file_name)

    catalog_not_registered = sorted(
        set(CORPUS_METADATA) - registered_names
    )

    return {
        "assigned": sorted(assigned),
        "unchanged": sorted(unchanged),
        "unmatched": sorted(unmatched),
        "catalog_not_registered": catalog_not_registered,
    }


def print_summary(summary):
    """
    Print a human-readable classification summary.
    """
    print(
        "Metadatos asignados:",
        len(summary["assigned"]),
    )

    for file_name in summary["assigned"]:
        print(f" + {file_name}")

    print(
        "Ya clasificados:",
        len(summary["unchanged"]),
    )

    for file_name in summary["unchanged"]:
        print(f" = {file_name}")

    print(
        "Registrados sin clasificación:",
        len(summary["unmatched"]),
    )

    for file_name in summary["unmatched"]:
        print(f"? {file_name}")

    print(
        "Catálogo aún no registrado:",
        len(summary["catalog_not_registered"]),
    )

    for file_name in summary["catalog_not_registered"]:
        print(f" - {file_name}")


def main():
    """
    Load the Registry, apply the classification catalog and save changes.
    """
    registry_data = registry.load_registry()

    summary = apply_catalog_to_registry(
        registry_data
    )

    if summary["assigned"]:
        registry.save_registry(
            registry_data
        )

    print_summary(summary)


if __name__ == "__main__":
    main()