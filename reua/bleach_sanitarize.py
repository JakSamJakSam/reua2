import bleach
# from bleach.css_sanitizer import CSSSanitizer


def bleach_clean(value: str) -> str:
    # css_sanitizer = CSSSanitizer(allowed_css_properties=["color", "font-weight", "text-align", "font-family"])
    return bleach.clean(
        value,
        tags={
            'span', 'font', 'p', 'b', 'i', 'u', 'em',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br',
            'iframe', 'a',
            'table','tbody','tr','td',
            'img',
            'li', 'ul', 'ol', },
        attributes = ['src', 'frameborder', 'width', 'height', 'class', 'href', 'target', 'style'],
        protocols=['http','https','data'],
        # css_sanitizer=css_sanitizer
    )
