import base64
import os

_LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
_LOGO_B64 = None


def get_logo_b64() -> str:
    """Return the HeartGuard AI logo as a base64 data URI (cached)."""
    global _LOGO_B64
    if _LOGO_B64 is None:
        with open(_LOGO_PATH, "rb") as f:
            _LOGO_B64 = base64.b64encode(f.read()).decode()
    return _LOGO_B64


def logo_img_tag(width: int = 160, style: str = "") -> str:
    """Return an <img> tag for the logo with optional width and extra style."""
    b64 = get_logo_b64()
    return (
        f'<img src="data:image/png;base64,{b64}" '
        f'width="{width}" style="display:block;{style}" alt="HeartGuard AI logo">'
    )
