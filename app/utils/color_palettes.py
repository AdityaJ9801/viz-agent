"""
Color palette definitions for chart styling.
10 professional schemes with gradient support, 7+ hex colors each.
"""

from __future__ import annotations

PALETTES: dict[str, list[str]] = {
    # ── Business / Professional ──
    "corporate": ["#1B2A4A", "#2563EB", "#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"],
    "executive": ["#0F172A", "#1E40AF", "#7C3AED", "#DB2777", "#F97316", "#14B8A6", "#64748B"],

    # ── Vibrant / Dynamic ──
    "vibrant":   ["#FF006E", "#FB5607", "#FFBE0B", "#8338EC", "#3A86FF", "#06D6A0", "#118AB2"],
    "neon":      ["#00F5FF", "#FF00FF", "#39FF14", "#FFD700", "#FF6B6B", "#4ECDC4", "#A855F7"],

    # ── Soft / Elegant ──
    "pastel":    ["#6C5CE7", "#A29BFE", "#FD79A8", "#FDCB6E", "#55EFC4", "#74B9FF", "#E17055"],
    "ocean":     ["#0077B6", "#00B4D8", "#90E0EF", "#CAF0F8", "#023E8A", "#03045E", "#48CAE4"],

    # ── Dark Mode ──
    "dark":      ["#BB86FC", "#03DAC6", "#CF6679", "#FF7043", "#FFD54F", "#4FC3F7", "#81C784"],
    "midnight":  ["#60A5FA", "#34D399", "#F472B6", "#FBBF24", "#A78BFA", "#FB923C", "#E2E8F0"],

    # ── Monochrome / Minimalist ──
    "monochrome":["#111827", "#374151", "#6B7280", "#9CA3AF", "#D1D5DB", "#E5E7EB", "#F9FAFB"],
    "slate":     ["#0F172A", "#334155", "#475569", "#64748B", "#94A3B8", "#CBD5E1", "#F1F5F9"],
}

# Background configs per scheme
BACKGROUNDS: dict[str, dict[str, str]] = {
    "corporate": {"plot_bg": "#FAFBFC", "paper_bg": "#FFFFFF", "grid": "#E5E7EB", "text": "#1F2937"},
    "executive": {"plot_bg": "#F8FAFC", "paper_bg": "#FFFFFF", "grid": "#E2E8F0", "text": "#0F172A"},
    "vibrant":   {"plot_bg": "#FFFBF5", "paper_bg": "#FFFFFF", "grid": "#FDE8D0", "text": "#1A1A2E"},
    "neon":      {"plot_bg": "#0A0A1A", "paper_bg": "#0D0D24", "grid": "#1A1A3E", "text": "#E0E0FF"},
    "pastel":    {"plot_bg": "#FAFAFE", "paper_bg": "#FFFFFF", "grid": "#E8E5F0", "text": "#2D2D44"},
    "ocean":     {"plot_bg": "#F0F9FF", "paper_bg": "#FFFFFF", "grid": "#BAE6FD", "text": "#0C4A6E"},
    "dark":      {"plot_bg": "#121212", "paper_bg": "#1E1E1E", "grid": "#333333", "text": "#E0E0E0"},
    "midnight":  {"plot_bg": "#0F172A", "paper_bg": "#1E293B", "grid": "#334155", "text": "#E2E8F0"},
    "monochrome":{"plot_bg": "#FAFAFA", "paper_bg": "#FFFFFF", "grid": "#E5E7EB", "text": "#111827"},
    "slate":     {"plot_bg": "#F8FAFC", "paper_bg": "#FFFFFF", "grid": "#CBD5E1", "text": "#0F172A"},
}

SCHEME_NAMES = list(PALETTES.keys())
DEFAULT_SCHEME = "corporate"


def get_palette(scheme: str = DEFAULT_SCHEME) -> list[str]:
    """Return the hex color list for the given scheme. Falls back to corporate."""
    return PALETTES.get(scheme, PALETTES[DEFAULT_SCHEME])


def get_background(scheme: str = DEFAULT_SCHEME) -> dict[str, str]:
    """Return the background/grid/text color config for the given scheme."""
    return BACKGROUNDS.get(scheme, BACKGROUNDS[DEFAULT_SCHEME])