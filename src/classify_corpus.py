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